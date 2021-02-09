# NVIDIA Data Science Stack

NVIDIA Data Science Stack is a tool to make it easy to setup a machine and
manage the software stacks for GPU accelerated Data Science.
This includes laptops, desktops, workstations, and cloud virtual machines.

Users can work with containers, or in a local environment.

* Code repo: <https://github.com/NVIDIA/data-science-stack>
* Releases: <https://github.com/NVIDIA/data-science-stack/releases>
* Report issues: <https://github.com/NVIDIA/data-science-stack/issues>
* Release planning: <https://github.com/NVIDIA/data-science-stack/projects>
* Subscribe to release notifications - watch the
<https://github.com/NVIDIA/data-science-stack> repository.
We suggest "Releases Only", if you haven't subscribed before check the
[help for watching and unwatching repositories](https://help.github.com/en/github/receiving-notifications-about-activity-on-github/watching-and-unwatching-repositories).

## Contents

* [Quick Start](#quick-start)
* [Minimum Hardware and Software](#minimum-hardware-and-software)
* [Operating System Setup](#operating-system-setup)
* [Installing the NVIDIA GPU Driver](#installing-the-nvidia-gpu-driver)
* [Installing NVIDIA Container SELinux Policy](#installing-nvidia-container-selinux-policy)
* [Laptop Power and Integrated GPU Configuration](#laptop-power-and-integrated-gpu-configuration)
* [More Information](#more-information)

## Quick Start

_For usage and command documentation: `./data-science-stack help` at any time._

_Note: The script is designed to run as the user, and ask for sudo password
when needed. Do not run it with `sudo ...`

On Ubuntu 18.04 or 20.04:

```bash
git clone https://github.com/NVIDIA/data-science-stack
cd data-science-stack
./data-science-stack setup-system
````

On Red Hat Enterprise Linux (RHEL) Workstation 7.x or 8.x:

```bash
git clone https://github.com/NVIDIA/data-science-stack
cd data-science-stack
./data-science-stack setup-system
# script will stop, manually install driver ... (instructions below)
./data-science-stack setup-system
```

On Windows Subsystem for Linux (WSL):
_Note: This functionality is alpha only until WSL v2 becomes production ready_
Follow the [install instructions](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) to install WSL v2 with CUDA support.
Then, create a a Ubuntu or RHEL VM, open a terminal, and follow OS-specific instructions above.

Next, users have a choice to use containers or a local Conda environment:

### Option 1 - In a Container (Recommended for container users)

```bash
./data-science-stack list
./data-science-stack build-container
./data-science-stack run-container
```

This creates and runs Jupyter in the container. Users can then connect
with the Jupyter notebook running at <http://localhost:8888/>
Control-C to exit.

To mount data or code into your contianer, see
[How do I mount data into containers?](#How-do-i-mount-data-into-containers)
below.

The reverse of `build-container` is `purge-container`.

For information about Docker refer to <https://docs.docker.com/>

### Option 2 - In a Local Conda Environment (Recommended for initial development work)

```bash
./data-science-stack list
./data-science-stack build-conda-env
./data-science-stack run-jupyter
```

This creates the local environment and runs Jupyter. Users can then connect
with the Jupyter notebook at the address and token output by Jupyter.
Control-C to exit.

The reverse of `build-conda-env` is `purge-conda-env`.

For information about Conda environments refer to
<https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>

### Multiple Users

To setup multiple users on the machine, they will need to get access to
Docker and setup Conda in the account

```bash
# As the additional user
./data-science-stack setup-user
# ... use container or conda commands above
```

### Upgrading

The script is designed to detect old versions of dependencies and upgrade
them, and create new environments/containers.

To upgrade automatically:
```bash
./data-science-stack upgrade
```
If a newer version of data science stack is available, the script will retrieve it and perform the upgrade.

To upgrade manually, get the new version of the script and environment configs with
`git pull` or with a new release .zip, and run the install steps again -
most likely `setup-system` and one of the `build-...` commands.

New environments and containers will be tagged with the version of the
script, so the old ones will not be modified.

Environments and containers are large, to clean up old ones use:

* Containers - `docker images` and `docker rmi ...`
* Local Conda environments - `conda env list` and `conda env remove ...`

### Testing

Once Jupyter is up and running (with `run-container` or `run-jupyter`)
navigate in the left panel to any of the sample notebooks and run them.
The sample notebooks come from the RAPIDS notebooks repo
<https://github.com/rapidsai/notebooks>

From the command line in your environment, or inside the container, the
`run-notebook <notebook-file>` command can also be used. Expect warnings
since the notebooks can depend on functions only available when using
Jupyter's web UI.

### Creating Custom Stacks

Creating custom environments is covered in the
[Custom Data Science Stack Environments](environments/README.md) README.

## Minimum Hardware and Software

* NVIDIA GPU - Pascal, Volta, or Turing family GPU(s) including:
  * Quadro P, GV, and RTX series
  * Tesla P, V and T series
  * GeForce 10xx and 20xx
* Operating System:
  * Ubuntu 18.04 or 20.04
  * Red Hat Enterprise Linux Workstation 7.5+ or 8.0+ (requires license)
  * Other Linux distributions are NOT supported, but may work as long as
    the driver and Docker work.

## Operating System Setup

Disable "Secure Boot" in the system BIOS/UEFI before installing Linux.

### Ubuntu

The Data Science stacks are supported on Ubuntu LTS 18.04.1+ or 20.04
with the 4.15+ kernel. Ubuntu can be downloaded from
<https://www.ubuntu.com/download/desktop>

### Red Hat Enterprise Linux Workstation (RHEL)

The Data Science stacks are supported on Red Hat Enterprise Linux Workstation(RHEL) version 7.5+ or 8.x.
The RHEL ISO image can be downloaded with the instructions on:
<https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/installation_guide/chap-download-red-hat-enterprise-linux>

#### Red Hat Subscriptions

A Red Hat subscription will be needed to install and use Red Hat Enterprise
Linux. A subscription also lets the system obtain update packages and
additional packages for Red Hat Enterprise Linux. Either purchase a
subscription or obtain a free evaluation subscription from the
Red Hat Software & Download Center -
<https://access.redhat.com/downloads>

Register the system with the Red Hat Customer Portal to complete the initial
setup. See the How to Register and Subscribe a system to the Red Hat
Customer Portal using Red Hat Subscription-Manager for further information -
<https://access.redhat.com/solutions/253273>

### Windows Subsystem for Linux (WSL v2)
_Note: This functionality is alpha only until WSL v2 becomes production ready_

Follow the [install instructions](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) for WSL v2 with CUDA support.
Then, create a a Ubuntu or RHEL VM, open a terminal, and follow OS-specific instructions above.

## Installing the NVIDIA GPU Driver

It is important that updated NVIDIA drivers are installed on the system.
The minimum version of the NVIDIA driver supported is 455.23.04.
More recent drivers may be available, but may not have been tested with the
data science stacks.

### Ubuntu Driver Install

Driver install for Ubuntu is handled by `data-science-stack setup-system`
so no manual install should be required.

If the driver if too old or the script is having problems, the driver can
be removed (this may have side effects, read the warnings) and reinstalled:

```bash
./data-science-stack purge-driver
# reboot
./data-science-stack setup-system
# reboot
```

### Red Hat Enterprise Linux Workstation (RHEL) Driver Install

Before attempting to install the driver check that the system does not
have `/usr/bin/nvidia-uninstall` which is left by an old driver .run file.
If it exists, run it with `sudo /usr/bin/nvidia-uninstall` to remove the
old driver first.

Install the base dependencies:

```bash
./data-science-stack setup-system
# this will stop once prerequisites are installed
```

Upgrade the kernel and reboot:

```bash
sudo yum upgrade -y kernel
sudo reboot
```

> **Note**: You may find that yum lock was acquired by "PackageKit" process
> on fresh install.
> To free the lock, kill the PackageKit process:
> (/usr/share/PackageKit/helpers/yum/yumBackend.> py)
>
> ```bash
> ps aux | grep yum
> kill <PackageKit_ProcessID>
> ```
>
> Now you should be able to run `yum upgrade kernel`

```bash
sudo yum install -y kernel-devel kernel-headers gcc dkms acpid libglvnd
```

Next, disable nouveau and reboot:

```bash
sudo cat <<EOF | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
blacklist nouveau
options nouveau modeset=0
EOF

sudo cp /etc/sysconfig/grub /etc/sysconfig/grub.bak
sudo vim /etc/sysconfig/grub
```

While editing the grub file:
Change the line containing
`GRUB_CMDLINE_LINUX="crashkernel=auto ... quiet"`
to
`GRUB_CMDLINE_LINUX="crashkernel=auto ... quiet rd.driver.blacklist=grub.nouveau"`.
Save, and close vim (with ":wq" ).

```bash
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r)-nouveau.img
sudo dracut /boot/initramfs-$(uname -r).img $(uname -r)
sudo reboot
```

Once nouveau has been disabled, change to runlevel 3:

```bash
sudo telinit 3
```

> **Note**: If after runlevel change, the screen is stuck on a blinking
cursor, hit Ctrl + Alt + F3

Check that nouveau is not loaded:

```bash
lsmod | grep nouveau
```

Download and install the driver:

```bash
# Check for the latest before using - https://www.nvidia.com/Download/index.aspx
wget http://us.download.nvidia.com/XFree86/Linux-x86_64/455.23.04/NVIDIA-Linux-x86_64-455.23.04.run
sudo sh ./NVIDIA-Linux-x86_64-455.23.04.run
```

> **Note**: In some cases the following prompts will occur:
>
> * If prompted to add to DKMS select YES.
> * If prompted that the "The distribution-provided pre-install script failed!
>   Are you sure you want to continue", select Continue.
> * If prompted to install the 32-bit compatibility libraries, select YES.
> * If prompted to update or overwrite existing libglvnd installation,
>   select DO NOT Overwrite.

One of the last installation steps will offer to update the X configuration
file. Either accept that offer (suggested), edit the X configuration file
manually so that the NVIDIA X driver will be used, or run nvidia-xconfig.

Once the NVIDIA driver install has completed, reboot.

```bash
sudo reboot
```

### Windows Subsystem for Linux (WSL v2) Driver Install
There is no need to install the driver inside WSL VMs as they use the driver installed in Windows. Data Science Stack scripts will detect WSL and not install the driver again. 

## Installing NVIDIA Container SELinux Policy

> **Note**: This section is only for systems that will use SELinux AND Containers

NVIDIA publishes an SELinux policy that enables using GPUs within containers
on NVIDIA DGX Servers on GitHub at:
<https://github.com/NVIDIA/dgx-selinux>

This policy has been validated on NVIDIA DGX servers running RHEL 7.5 and 7.6.
It is expected that users/admins will use the DGX SELinux policy as a
reference and will modify it as needed to fit their servers.

Actions performed by the script below:

* Install the dependencies required to build the DGX SELinux policy
* Clone the DGX SELinux policy git project
* << CUSTOMIZE THE POLICY >>
* Build the SELinux policy
* Install the SELinux policy

> **Note**: To accommodate SELinux, nvidia-container-selinux is required to
> allow containers to use NVIDIA GPUs. The --security-opt option in the
> command sets the label type that is created by the package so that the
> specified container uses the NVIDIA GPUs. If SELinux is removed or
> disabled, then the --security-opt option is not needed.

```bash
sudo yum install -y git selinux-policy selinux-policy-devel \
  selinux-policy-base libselinux-utils policycoreutils policycoreutils-python
git clone https://github.com/NVIDIA/dgx-selinux.git
cd dgx-selinux/src/nvidia-container-selinux

<<< CUSTOMIZE YOUR SELINUX POLICY >>>

make -f /usr/share/selinux/devel/Makefile
sudo semodule -i nvidia-container.pp
sudo reboot
```

> **Note**: You may encounter error messages while building the SELinux
> policy such as
> `“/usr/share/selinux/devel/include/contrib/container.if:33: Error:
> duplicate definition of container_runtime_exec().
> Original definition on 60.`. These may be safely ignored if the
> nvidia-container.pp file was generated, and
> installed successfully. For reference, see
> <https://bugzilla.redhat.com/show_bug.cgi?id=1567980>

## Laptop Power and Integrated GPU Configuration

On Laptop systems GPU selection and power settings may need
additional configuration.

> **Note**: On some systems, the external display connectors are driven by the
> NVIDIA GPU, so restricting graphics to the Intel IGP will prevent the use
> of external displays. If the use of external displays is desired on such
> a system, the NVIDIA GPU will need to be shared between graphics and
> compute tasks.

For best performance, it is recommended that X be configured to use the
Intel integrated graphics processor (IGP) to drive the display. This allows
the full resources of the NVIDIA GPU to be dedicated to running compute
workloads. For optimal power savings, it is recommended that the GPU be
powered off when not in use.

### Intel IGP on Ubuntu or RHEL 8.x

When the NVIDIA driver is installed, Ubuntu and RHEL 8 will automatically
configure the NVIDIA GPU to render the desktop environment, and offload the
graphics rendered by the NVIDIA GPU for display on the Intel IGP using PRIME
display offloading. For systems which drive external displays through the
NVIDIA GPU, where use of external displays is desired, no further
configuration is needed. For other systems, the X server will require
additional configuration in order to dedicate the NVIDIA GPU for compute
tasks only.

In order to configure the X server properly, determine the PCI bus ID of
the Intel IGP. Run the command:

```bash
lspci -d 8086::0300
```

to list all Intel VGA devices, which should display a line like:

```
00:02.0 VGA compatible controller: Intel Corporation Device 3e9b (rev 02)
```

Make a note of the bus ID that appears at the beginning of the line
("00:02.0" in this example), and adapt this bus ID in order to use it in an
X configuration file. lspci lists bus IDs using hexadecimal numbers in the
form `[<domain>:]<bus>:<device>.<function>`. On systems where the only PCI
domain is domain 0, the domain will typically be omitted. The X configuration
file accepts bus IDs using decimal numbers in the form
`PCI:<bus>[@<domain>]:device:function`. If the PCI domain is 0, the
domain may be omitted.

As an example, the lspci bus ID of `00:02.0` listed above would be written
as `PCI:0:2:0` in an X configuration file. As an additional example showing
the domain field populated, unique values for each field, and numbers that
are different in decimal versus hexadecimal, the lspci bus ID `0010:0f:e.d`
would be written as `PCI:15@16:14:13` in an X configuration file.

Once the correct PCI bus ID is determined, populate the file
/etc/X11/xorg.conf with the following contents, creating it if necessary:

```
Section "Device"
    Identifier "Device0"
    BusID "<correctly formatted PCI bus ID for Intel IGP>"
    Driver "modesetting"
EndSection

Section "Screen"
    Identifier "Screen0"
    Device "Device0"
EndSection
```

Replace the text `<correctly formatted PCI bus ID for Intel IGP>` with the
bus ID string formed previously.

> **Note**: While Ubuntu provides tools for simplifying switching between the
> default NVIDIA+Intel PRIME display offloading behavior and an Intel-only
> configuration, the Intel-only profile prevents the use of the NVIDIA driver
> for non-graphical purposes in addition to disabling its use for graphics,
> necessitating the manual X configuration.

### Intel IGP on RHEL 7.x

On versions of RHEL before RHEL 8, the X server will be configured to use
the Intel IGP only for graphics by default, and no further configuration is
needed to ensure that the NVIDIA GPU’s resources remain dedicated for compute
purposes. On systems with the external displays driven by the NVIDIA GPU,
where use of external displays is desired, PRIME display offloading will need
to be manually configured. Manual configuration of PRIME display offloading
is beyond the scope of this documentation.

### Laptop GPU Power Management

The NVIDIA GPU driver supports runtime Power Management (PM). By default,
GPU runtime power management is disabled. To enable GPU runtime PM, please
install an NVIDIA PM udev rules file. This udev file:

* Removes function 2 (USB xHCI Host controller) and function 3 (USB Type-C
  USCI controller) of the GPU, if present. Linux kernel versions before 5.3
  do not have full-fledged support for these functions, which will prevent
  GPU runtime PM.
* Sets 'auto' in the sysfs runtime PM entries for function 0 (VGA display
  controller) and function 1 (Audio controller).

#### Installing the NVIDIA PM udev rules on laptops

Create the file `80-nvidia-pm.rules` with the following contents:

```
# udev rules for Enabling Runtime Power Management for NVIDIA GPU.
#
# The NVIDIA Turing GPU is a multi-function PCI device
# which has the following four functions:
#
#     Function 0 : VGA display controller
#     Function 1 : Audio controller
#     Function 2 : USB xHCI Host controller
#     Function 3 : USB Type-C USCI controller
#
# The NVIDIA GPU driver only manages function 0.
# The remaining functions are managed by other drivers.
# The drivers for function 2 and function 3 in this kernel version
# lack full support for runtime PM, which prevents proper runtime
# PM functionality for function 0.
#
# This udev rules script will remove these functions during
# boot and will allow runtime PM to work for the GPU. It won't
# impact normal USB functionality, which is managed by the
# integrated USB xHCI Host controller.

# Remove NVIDIA USB xHCI Host Controller devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c0330", ATTR{remove}="1"

# Remove NVIDIA USB Type-C UCSI devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c8000", ATTR{remove}="1"

# Enable runtime PM for NVIDIA VGA controller devices
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x030000", TEST=="power/control", ATTR{power/control}="auto"

# Enable runtime PM for NVIDIA Audio controller devices
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x040300", TEST=="power/control", ATTR{power/control}="auto"
```

Copy the downloaded file to /lib/udev/rules.d/

```bash
sudo cp 80-nvidia-pm.rules /lib/udev/rules.d/
```

Reboot the system

```bash
sudo reboot
```

To check if function 2 and 3 have been removed, run following commands,
which should not give any output.

```bash
lspci -d '10de::0c03'
lspci -d '10de::0c80'
```

#### Uninstalling the NVIDIA PM udev rules on laptops

Remove the NVIDIA PM rules file

```bash
sudo rm /lib/udev/rules.d/80-nvidia-pm.rules
```

Reboot the system

```bash
sudo reboot
```


## Troubleshooting and FAQ

### The driver does not install correctly

Try using `purge-driver` followed by `install-driver`, then check with
`diagnostics`. If the driver was previously installed with a.run file the
script will let you know how to remove the old driver.

### How much disk space is needed?

About 30GB free should be enough. A lot of space is needed during
environment/container creation since Conda has a package cache.

### The script is failing after it cannot reach URLs or download files

To setup the Data Science Stack the script needs to update the OS and other
installed packages, install software from NVIDIA, setup Docker and pull
containers, download Conda packages, clone repos from GitHub, and other tasks.
During this process if the network is down, the OS or IT firewalls are
blocking any of those hosts errors will occur. Retrying the command will
work in most cases after the problem/block is resolved.

### How do I mount data into containers?

To mount code or data directories into your running container, add additional
`-v "/host/path/:/mount/location"` parameters to the `docker run ...` command.
 The latest command to run the container is displayed by
`./data-science-stack run-container` when it runs.

For example to mount ~/notebooks and /data directories in as
/notebooks and /data volumes the Docker command would begin with
````bash
docker run -v ~/notebooks:/notebooks -v /data:/data ...
````

For information about Docker mounts refer to
<https://docs.docker.com/storage/bind-mounts/>

## More Information

* [NVIDIA Accelerated Data Science](https://www.nvidia.com/en-us/deep-learning-ai/solutions/data-science/)
* [RAPIDS - Open GPU Data Science](https://rapids.ai/)
  * [RAPIDS Notebooks](https://github.com/rapidsai/notebooks)
* [NVIDIA Powered Data Science Workstation](https://www.nvidia.com/en-us/deep-learning-ai/solutions/data-science/workstations/)
* [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
* [Docker CE](https://docs.docker.com/install/)
  * [Ubuntu](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce)
  * [Red Hat / Cent OS](https://docs.docker.com/install/linux/docker-ce/centos/#install-docker-engine---community)
* [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
* [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/)
