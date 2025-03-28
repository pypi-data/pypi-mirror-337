# xprofiler

The `xprofiler` SDK and CLI tool provides abstraction over profile session
locations and infrastructure running the analysis.

This includes allowing users to create and manage VM instances for TensorBoard
instances in regards to profiling workloads for GPU and TPU.

## Quickstart

### Install Dependencies

`xprofiler` relies on using [gcloud](https://cloud.google.com/sdk).

The first step is to follow the documentation to [install](https://cloud.google.com/sdk/docs/install).

Running the initial `gcloud` setup will ensure things like your default project
ID are set.

### Create a VM Instance for TensorBoard

To create a TensorBoard instance, you must provide a path to a GCS bucket.
It is also useful to define your specific zone.

```bash
ZONE=us-central1-a
GCS_PATH="gs://example-bucket/my-profile-data"

xprofiler create -z $ZONE -l $GCS_PATH
```

When the command completes, you will see it return information about the
instance created, similar to below:

```
LOG_PATH                            NAME                                            ZONE
gs://example-bucket/my-profile-data xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef  us-central1-a
```

This will create a VM instance with TensorBoard installed. Note that this
initial startup for TensorBoard will take up to a few minutes (typically less
than 5 minutes) if you want to connect to the VM's TensorBoard.

### List VM Instances

To list the TensorBoard instances created by `xprofiler`, you can simply run
`xprofiler list`. However, it's recommended to specify the zone (though not
required).

```bash
ZONE=us-central1-a

xprofiler list -z $ZONE
```

This will output something like the following if there are instances matching
the list criteria:

```
LOG_PATH                                   NAME                                            ZONE
gs://example-bucket/my-other-profile-data  xprofiler-8187640b-e612-4c47-b4df-59a7fc86b253  us-central1-a
gs://example-bucket/my-profile-data        xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef  us-central1-a
```

Note you can specify the GCS bucket to get just that one associated instance:

```bash
xprofiler list -l $GCS_PATH
```

### Delete VM Instance

To delete an instance, you'll need to specify either the GCS bucket paths or the
VM instances' names. Specifying the zone is required.

```bash
# Delete by associated GCS path
xprofiler delete -z $ZONE -l $GCS_PATH

# Delete by VM instance name
VM_NAME="xprofiler-8187640b-e612-4c47-b4df-59a7fc86b253"
xprofiler delete -z $ZONE --vm-name $VM_NAME
```

## Details on `xprofiler`

### Main Command: `xprofiler`

The `xprofiler` command has additional subcommands that can be invoked to
[create](#subcommand-xprofiler-create) VM instances,
[list](#subcommand-xprofiler-list) VM instances,
[delete](#subcommand-xprofiler-delete) instances, etc.
However, the main `xprofiler` command has some additional options without
invoking a subcommand.

#### `xprofiler --help`

Gives additional information about using the command including flag options and
available subcommands. Also can be called with `xprofiler -h`.

> Note that each subcommand has a `--help` flag that can give information about
> that specific subcommand. For example: `xprofiler list --help`

#### `xprofiler --abbrev ...`

When invoking a subcommand, typically there is output related to VM instances
involved with the subcommand, usually as a detailed table.

In some cases, a user may only want the relevant information (for example a log
directory GCS path or VM name instance). This can be particularly useful in
scripting with `xprofiler` by chaining with other commands.

To assist with this, the `--abbrev` (or equivalent `-a`) flag will simply print
the relevant item (log directory path or VM instance name).

For example, calling `xprofiler list` might give the following output:

```
LOG_PATH                                   NAME                                            ZONE
gs://example-bucket/my-other-profile-data  xprofiler-8187640b-e612-4c47-b4df-59a7fc86b253  us-central1-a
gs://example-bucket/my-profile-data        xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef  us-central1-a
```

But calling with `xprofiler --abbrev list` will instead print out an abbreviated
form of the above output where each item is displayed on a new line:

```
xprofiler-8187640b-e612-4c47-b4df-59a7fc86b253
xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef
```

### Subcommand: `xprofiler create`

This command is used to create a new VM instance for TensorBoard to run with a
given profile log directory GCS path.

Usage details:

```
xprofiler create
  [--help]
  --log-directory GS_PATH
  [--zone ZONE_NAME]
  [--vm-name VM_NAME]
  [--verbose]
```

At the successful completion of this command, the information regarding the
newly created VM instances is printed out like the example below:

```
LOG_PATH                            NAME                                            ZONE
gs://example-bucket/my-profile-data xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef  us-central1-a
```

If the [xprofiler abbreviation flag](#xprofiler-abbrev) is used, then an
abbreviated output is given like so:

```
xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef
```

#### `xprofiler create --help`

This provides the basic usage guide for the `xprofiler create` subcommand.

#### Creating a VM Instance

To create a new VM instance, a user _must_ specify a profile log directory path
(a GCS path) as in `xprofiler create -l gs://example-bucket/my-profile-data`.
This will create a VM instance associated with the log directory. The instance
will also have TensorBoard installed and setup ready for use.

> Note that after the VM creation, it might take a few minutes for the VM
> instance to fully be ready (installing dependencies, launching TensorBoard,
> etc.)

It is recommended to also provide a zone with `--zone` or `-z` but it is
optional.

By default, the VM instance's name will be uniquely created prepended with
`xprofiler-`. However, this can be specified with the `--vm-name` or `-n` flag
to give a specific name to the newly created VM.

Lastly, there is a `--verbose` or `-v` flag that will provide information as the
`xprofiler create` subcommand runs.

### Subcommand: `xprofiler list`

This command is used to list a VM instances created by the xprofiler tool.

Usage details:

```
xprofiler list
  [--help]
  [--zone ZONE_NAME]
  [--log-directory GS_PATH [GS_PATH ...]]
  [--filter FILTER_NAME [FILTER_NAME ...]]
  [--verbose]
```

At the successful completion of this command, the information of matching VM
instances is printed out like the example below:

```
LOG_PATH                                   NAME                                            ZONE
gs://example-bucket/my-other-profile-data  xprofiler-8187640b-e612-4c47-b4df-59a7fc86b253  us-central1-a
gs://example-bucket/my-profile-data        xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef  us-central1-a
```

If the [xprofiler abbreviation flag](#xprofiler-abbrev-) is used, then an
abbreviated output is given like so:

```
xprofiler-8187640b-e612-4c47-b4df-59a7fc86b253
xprofiler-ev86r7c5-3d09-xb9b-a8e5-a495f5996eef
```

#### `xprofiler list --help`

This provides the basic usage guide for the `xprofiler list` subcommand.


#### Listing Specific Subsets

Note that the `xprofiler list` command will default to listing all VM instances
that have the prefix `xprofiler`.

However, a specific subset of VM instances can be returned using different
options.

##### Providing Zone

`xprofiler list -z $ZONE`

Providing the zone is highly recommended since otherwise the command can take a
while to search for all relevant VM instances.

##### Providing GCS Path (Profile Log Directory)

Since `xprofiler list` is meant to look for VM instances created with
`xprofiler`, it is likely the VM instance of interest is associated with a
profile log directory.

To filter for a specific VM instance with an associated log directory, simply
use the command like so:

```bash
xprofiler list -l $GS_PATH
```

You can even use multiple log directory paths to find any VMs associated with
any of these paths:

```bash
xprofiler list -l $GS_PATH_0 $GS_PATH_1 $GS_PATH_2
```
