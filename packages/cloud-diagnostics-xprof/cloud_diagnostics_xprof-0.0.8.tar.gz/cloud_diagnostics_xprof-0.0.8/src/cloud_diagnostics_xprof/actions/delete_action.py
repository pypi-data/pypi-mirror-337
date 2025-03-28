"""A delete command implementation for the xprofiler CLI.

This command is used as part of the xprofiler CLI to delete a hosted TensorBoard
instance. The intention is that this can be used after creation of a new
instance using the `xprofiler create` command (versus using for general instance
deletion).
"""

import argparse
from collections.abc import Mapping, Sequence
from cloud_diagnostics_xprof.actions import action
from cloud_diagnostics_xprof.actions import list_action


class Delete(action.Command):
  """A command to delete a hosted TensorBoard instance."""

  def __init__(self):
    super().__init__(
        name='delete',
        description='Delete a hosted TensorBoard instance.',
    )

  def add_subcommand(
      self,
      subparser: argparse._SubParsersAction,
  ) -> None:
    """Creates a subcommand for `delete`.

    Args:
        subparser: The subparser to add the delete subcommand to.
    """
    delete_parser = subparser.add_parser(
        name='delete',
        help='Delete a hosted TensorBoard instance.',
        formatter_class=argparse.RawTextHelpFormatter,  # Keeps format in help.
    )
    # log-directory is optional.
    delete_parser.add_argument(
        '--log-directory',
        '-l',
        metavar='GS_PATH',
        nargs='+',  # Allow multiple log directories to delete multiple VMs.
        help=(
            'The log directory(s) associated with the VM(s) to delete. '
            'Specify multiple names to delete multiple VMs.'
        ),
    )
    delete_parser.add_argument(
        '--vm-name',
        '-n',
        metavar='VM_NAME',
        nargs='+',  # Allow multiple VM names.
        help=(
            'The name of the VM(s) to delete. '
            'Specify multiple names to delete multiple VMs.'
        ),
    )
    delete_parser.add_argument(
        '--zone',
        '-z',
        metavar='ZONE_NAME',
        required=True,
        help='The GCP zone to delete the instance in.',
    )
    delete_parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Print the command.',
    )

  def _get_vms_from_log_directory(
      self,
      log_directories: Sequence[str],
      zone: str | None,
      verbose: bool = False,
  ) -> Sequence[str]:
    """Gets the VM name(s) from the log directory(s).

    Args:
      log_directories: The log directory(s) associated with the VM(s) to delete.
      zone: The GCP zone to delete the instance in.
      verbose: Whether to print verbose output.

    Returns:
      The VM name(s) from the log directory(s).
    """
    # Use the list action to get the VM name(s).
    list_command = list_action.List()
    list_args = argparse.Namespace(
        zone=zone,
        log_directory=log_directories,
        filter=None,
        verbose=verbose,
    )

    # Each VM name is on a separate line after the header.
    command_output, _ = list_command.run(
        args=list_args,
        verbose=verbose,
    )
    if verbose:
      print(command_output)

    vm_names = (
        command_output
        .strip()  # Removes the extra new line(s) that tends to be at the end.
        .split('\n')[1:]  # Ignores header line.
    )

    vm_names = [vm_name.split()[2] for vm_name in vm_names]

    return vm_names

  def _build_command(
      self,
      args: argparse.Namespace,
      extra_args: Mapping[str, str] | None = None,
      verbose: bool = False,
  ) -> Sequence[str]:
    """Builds the delete command.

    Note this should not be called directly by the user and should be called
    by the run() method in the action module (using the subparser).

    Args:
      args: The arguments parsed from the command line.
      extra_args: Any extra arguments to pass to the command.
      verbose: Whether to print the command and other output.

    Returns:
      The command to delete the VM(s).
    """
    # Check that either VM name or log directory is specified.
    if not args.vm_name and not args.log_directory:
      raise ValueError(
          'Either --vm-name or --log-directory must be specified.'
      )

    vm_names = []

    # If log directory is specified, use that to get the VM name(s)
    if args.log_directory:
      vm_names_from_log_directory = self._get_vms_from_log_directory(
          log_directories=args.log_directory,
          zone=args.zone,
          verbose=verbose,
      )

      if verbose:
        print(f'VM name(s) from log directory: {vm_names_from_log_directory}')

      vm_names.extend(vm_names_from_log_directory)

    # Include the VM name(s) from the command line if specified.
    if args.vm_name:
      if verbose:
        print(f'VM name from command line: {args.vm_name}')
      vm_names.extend(args.vm_name)

    if verbose:
      print(f'Will delete VM(s) w/ name: {vm_names}')

    delete_vm_command = [
        self.GCLOUD_COMMAND,
        'compute',
        'instances',
        'delete',
        '--quiet',  # Don't ask for confirmation or give extra details.
        f'--zone={args.zone}'
    ]

    # Extensions of any other arguments to the main command.
    if extra_args:
      delete_vm_command.extend(
          [f'{arg}={value}' for arg, value in extra_args.items()]
      )

    if not vm_names:
      raise ValueError('No VM(s) to delete.')

    delete_vm_command.extend(vm_names)

    if verbose:
      print(delete_vm_command)

    return delete_vm_command
