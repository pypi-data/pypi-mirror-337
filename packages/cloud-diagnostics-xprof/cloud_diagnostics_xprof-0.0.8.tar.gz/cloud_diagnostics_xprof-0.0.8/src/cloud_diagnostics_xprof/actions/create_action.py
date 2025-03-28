"""A create command implementation for the xprofiler CLI.

This command is used as part of the xprofiler CLI to create a hosted TensorBoard
instance. This will include other metadata such as labels to the log directory
that are specific to the the xprofiler instance.
"""

import argparse
from collections.abc import Mapping, Sequence
import json
import time
import uuid

from cloud_diagnostics_xprof.actions import action


_WAIT_TIME_IN_SECONDS = 20
_MAX_WAIT_TIME_IN_SECONDS = 300

_OUTPUT_MESSAGE = r"""
Instance for {LOG_DIRECTORY} has been created.
You can access it at https://{BACKEND_ID}-dot-{REGION}.notebooks.googleusercontent.com
Instance is hosted at {VM_NAME} VM.
"""

_STARTUP_SCRIPT_STRING = r"""#! /bin/bash
echo \"Starting setup.\"
apt-get update
apt-get install -yq git supervisor python3 python3-pip python3-distutils python3-virtualenv
# Setup tensorboard webserver
echo \"Setup tensorboard webserver.\"
virtualenv -p python3 tensorboardvenv
source tensorboardvenv/bin/activate
tensorboardvenv/bin/pip3 install tensorflow-cpu
tensorboardvenv/bin/pip3 install --upgrade 'cloud-tpu-profiler>=2.3.0'
tensorboardvenv/bin/pip3 install tensorboard_plugin_profile
tensorboardvenv/bin/pip3 install importlib_resources
tensorboardvenv/bin/pip3 install etils
tensorboard --logdir {LOG_DIRECTORY} --host 0.0.0.0 --port 6006 &
# Setup forwarding agent and proxy
echo \"Setup forwarding agent and proxy.\"
# Remove existing docker packages
echo \"Remove existing docker packages.\"
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
# Install docker
echo \"Install docker.\"
sudo apt install docker.io --yes
# Get inverse proxy mapping file.
echo \"Get inverse proxy mapping file.\"
gcloud storage cp gs://dl-platform-public-configs/proxy-agent-config.json .
# Get proxy URL for this region
echo \"Get proxy URL for this region.\"
PROXY_URL=\$(python3 -c \"import json; import sys; data=json.load(sys.stdin); print(data['agent-docker-containers']['latest']['proxy-urls']['{REGION}'][0])\" < proxy-agent-config.json)
# Get VM ID for this proxy url
echo \"Get VM ID for this proxy url.\"
VM_ID=\$(curl -H 'Metadata-Flavor: Google' \"http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?format=full&audience=${PROXY_URL}/request-endpoint\"  2>/dev/null)
# Generate backend and host id
echo \"Generate backend and host id.\"
RESULT_JSON=\$(curl -H \"Authorization: Bearer \$(gcloud auth print-access-token)\" -H \"X-Inverting-Proxy-VM-ID: \${VM_ID}\" -d \"\" \"\${PROXY_URL}/request-endpoint\" 2>/dev/null)
echo -e \"\${RESULT_JSON}\"
# Extract backend id from response
echo \"Extract backend id from response.\"
BACKEND_ID=\$(python3 -c \"import json; import sys; data=json.loads(sys.argv[1]); print(data['backendID'])\" \"\${RESULT_JSON}\")
echo -e \"\${BACKEND_ID}\"
# Extract hostname from response
echo \"Extract hostname from response.\"
HOSTNAME=\$(python3 -c \"import json; import sys; data=json.loads(sys.argv[1]); print(data['hostname'])\" \"\${RESULT_JSON}\")
echo -e \"\${HOSTNAME}\"
# Set container name
CONTAINER_NAME='proxy-agent'
# Set URL for agent container
CONTAINER_URL='gcr.io/inverting-proxy/agent:latest'
# Start agent container
docker run -d \
--env \"BACKEND=\${BACKEND_ID}\" \
--env \"PROXY=\${PROXY_URL}/\" \
--env \"SHIM_WEBSOCKETS=true\" \
--env \"SHIM_PATH=websocket-shim\" \
--env \"PORT=6006\" \
--net=host \
--restart always \
--name \"\${CONTAINER_NAME}\" \
\"\${CONTAINER_URL}\" &
echo \"Setting endpoint info in metadata.\"
gcloud compute instances add-labels {MY_INSTANCE_NAME} --zone={ZONE} --labels tb_backend_id=\"\${BACKEND_ID}\"
echo \"Startup Finished\"
"""

# Used to install dependencies & startup TensorBoard.
# MUST be a raw string otherwise interpreted as file path for startup script.
_STARTUP_ENTRY_STRING: str = r"""#! /bin/bash
python3 -c "print(r'''{STARTUP_SCRIPT_STRING}''')" > startup.sh
chmod 775 startup.sh
. ./startup.sh > startup.log
"""

# Used for creating the VM instance.
_DEFAULT_EXTRA_ARGS: Mapping[str, str] = {
    '--tags': 'default-allow-ssh',
    '--image-family': 'debian-12',
    '--image-project': 'debian-cloud',
    '--machine-type': 'e2-highmem-4',
    '--scopes': 'cloud-platform',
}

_DEFAULT_EXTRA_ARGS_DESCRIBE: Mapping[str, str] = {
    '--format': 'json',
}


class Create(action.Command):
  """A command to delete a hosted TensorBoard instance."""

  def __init__(self):
    super().__init__(
        name='create',
        description='Create a new hosted TensorBoard instance.',
    )
    self.vm_name = f'{self.VM_BASE_NAME}-{uuid.uuid4()}'

  def add_subcommand(
      self,
      subparser: argparse._SubParsersAction,
  ) -> None:
    """Creates a subcommand for `create`.

    Args:
        subparser: The subparser to add the create subcommand to.
    """
    create_parser = subparser.add_parser(
        name='create',
        help='Create a hosted TensorBoard instance.',
        formatter_class=argparse.RawTextHelpFormatter,  # Keeps format in help.
    )
    create_parser.add_argument(
        '--log-directory',
        '-l',
        metavar='GS_PATH',
        required=True,
        help='The GCS path to the log directory.',
    )
    create_parser.add_argument(
        '--zone',
        '-z',
        metavar='ZONE_NAME',
        required=True,
        help='The GCP zone to create the instance in.',
    )
    create_parser.add_argument(
        '--vm-name',
        '-n',
        metavar='VM_NAME',
        help=(
            'The name of the VM to create. '
            'If not specified, a default name will be used.'
        ),
    )
    create_parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Print the command.',
    )

  def _build_command(
      self,
      args: argparse.Namespace,
      extra_args: Mapping[str, str] | None = None,
      verbose: bool = False,
  ) -> Sequence[str]:
    """Builds the create command.

    Note this should not be called directly by the user and should be called
    by the run() method in the action module (using the subparser).

    Args:
      args: The arguments parsed from the command line.
      extra_args: Any extra arguments to pass to the command.
      verbose: Whether to print the command and other output.

    Returns:
      The command to create the VM.
    """
    # Make sure we define this if not already since we'll build from it.
    if extra_args is None:
      extra_args = {}

    # Include our extra args for creation (overwriting any user provided).
    extra_args |= _DEFAULT_EXTRA_ARGS

    labels = {
        'log_directory': args.log_directory,
    }
    extra_args |= {'--labels': self._format_label_string(labels)}

    if verbose:
      print(f'Will create VM w/ name: {self.vm_name}')

    # Create the startup entry script.
    startup_entry_script = startup_script_string(
        args.log_directory, self.vm_name, args.zone
    )

    if verbose:
      print(f'Using startup script:\n{startup_entry_script}')

    extra_args |= {'--metadata': 'startup-script=' + startup_entry_script}

    create_vm_command = [
        self.GCLOUD_COMMAND,
        'compute',
        'instances',
        'create',
        self.vm_name,
    ]
    if args.zone:
      create_vm_command.append(f'--zone={args.zone}')

    # Extensions of any other arguments to the main command.
    if extra_args:
      create_vm_command.extend(
          [f'{arg}={value}' for arg, value in extra_args.items()]
      )

    if verbose:
      print(create_vm_command)

    return create_vm_command

  def _build_describe_command(
      self,
      args: argparse.Namespace,
      extra_args: Mapping[str, str] | None = None,
      verbose: bool = False,
  ) -> Sequence[str]:
    """Builds the describe command.

    Note this should not be called directly by the user and should be called
    by the run() method in the action module (using the subparser).

    Args:
      args: The arguments parsed from the command line.
      extra_args: Any extra arguments to pass to the command.
      verbose: Whether to print the command and other output.

    Returns:
      The command to describe the VM.
    """
    # Make sure we define this if not already since we'll build from it.
    if extra_args is None:
      extra_args = {}

    # Include our extra args for creation (overwriting any user provided).
    extra_args |= _DEFAULT_EXTRA_ARGS_DESCRIBE

    describe_vm_command = [
        self.GCLOUD_COMMAND,
        'compute',
        'instances',
        'describe',
        self.vm_name,
    ]
    if args.zone:
      describe_vm_command.append(f'--zone={args.zone}')

    # Extensions of any other arguments to the main command.
    if extra_args:
      describe_vm_command.extend(
          [f'{arg}={value}' for arg, value in extra_args.items()]
      )

    if verbose:
      print(describe_vm_command)

    return describe_vm_command

  def run(
      self,
      args: argparse.Namespace,
      extra_args: Mapping[str, str] | None = None,
      verbose: bool = False,
  ) -> tuple[str, bool]:
    """Run the command.

    Args:
      args: The arguments parsed from the command line.
      extra_args: Any extra arguments to pass to the command.
      verbose: Whether to print the command and other output.

    Returns:
      The output of the command.
    """
    if args.vm_name:
      self.vm_name = args.vm_name

    command = self._build_command(args, extra_args, verbose)
    if verbose:
      print(f'Command to run: {command}')

    stdout: str = self._run_command(command, verbose=verbose)
    timer = 0
    print('Waiting for instance to be created. It can take a few minutes.')
    while timer < _MAX_WAIT_TIME_IN_SECONDS:
      timer += _WAIT_TIME_IN_SECONDS
      time.sleep(_WAIT_TIME_IN_SECONDS)
      command = self._build_describe_command(args, extra_args, verbose)
      if verbose:
        print(f'Command to run: {command}')
      stdout_describe = self._run_command(command, verbose=verbose)
      json_output = json.loads(stdout_describe)
      if 'labels' in json_output and 'tb_backend_id' in json_output['labels']:
        backend_id = json_output['labels']['tb_backend_id']
        if verbose:
          print(f'Backend id: {backend_id}')
        print(
            _OUTPUT_MESSAGE.format(
                LOG_DIRECTORY=args.log_directory,
                BACKEND_ID=backend_id,
                REGION='-'.join(args.zone.split('-')[:-1]),
                VM_NAME=self.vm_name,
            )
        )
        break
    return stdout, False


def startup_script_string(log_directory: str, vm_name: str, zone: str) -> str:
  """Returns the startup script string."""
  return _STARTUP_ENTRY_STRING.format(
      STARTUP_SCRIPT_STRING=_STARTUP_SCRIPT_STRING.format(
          LOG_DIRECTORY=log_directory,
          MY_INSTANCE_NAME=vm_name,
          ZONE=zone,
          REGION='-'.join(zone.split('-')[:-1]),
          PROXY_URL='{PROXY_URL}',
          VM_ID='{VM_ID}',
          BACKEND_ID='{BACKEND_ID}',
          HOSTNAME='{HOSTNAME}',
          CONTAINER_NAME='{CONTAINER_NAME}',
          CONTAINER_URL='{CONTAINER_URL}',
          RESULT_JSON='{RESULT_JSON}',
      )
  )
