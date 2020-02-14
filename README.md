# NVIDIA Data Science Stack

Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

## Introduction

NVIDIA Data Science Stack is a tool to make it easy to setup and manage the
software stacks to do GPU accelerated workstations for Data Science.

User can work in containers, or work in a local Conda environment.

------------------------------------------------------------------------------

## Quick Start

Usage:

```bash
data-science-stack help
```

On Ubuntu 18.04:

```bash
data-science-stack setup-system
data-science-stack setup-user
````

On Red Hat Enterprise Linux 7.x or 8.x:

```bash
data-science-stack setup-system
# script will stop, manually install driver ... (instuctions below)
data-science-stack setup-system
data-science-stack setup-user
```

Next, users have a choice to use containers or a local Conda environment:

### In a Container (Recommended for container users)

```bash
data-science-stack build-container
data-science-stack run-container
```

This creates and runs Jupyter in the container. Users can then connect
with the Jupyter notebook running at <http://localhost:8888/>
Control-C to exit.

For information about Docker refer to <https://docs.docker.com/>

### In a Local Conda Environment (Alternative)

```bash
data-science-stack build-conda-env
data-science-stack run-jupyter
```

This creates the local environment and runs Jupyter. Users can then connect
with the Jupyter notebook at the address and token output by Jupyter.
Control-C to exit.

For information about Conda environments refer to
<https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>

To setup multiple users on the machine, they will need to get access to
Docker and setup Conda in the account

```bash
# As the additional user
data-science-stack setup-user
# ... use container or conda commands above
```

------------------------------------------------------------------------------

## Minimum Hardware/Software Compatibility

* NVIDIA GPU - Pascal, Volta, or Turing family GPU(s) including:
  * Quadro P, GV, and RTX series
  * Tesla P, V and T series
  * GeForce 10xx and 20xx
* Operating System:
  * Ubuntu 18.04.x
  * Red Hat Enterprise Linux 7.5+ or 8.0+ (requires license)
  * Other Linux distributions are NOT supported, but may work as long as
    the driver and Docker work.

------------------------------------------------------------------------------

## Operating Systems

Disable "Secure Boot" in the system BIOS/UEFI before installing Linux.

### Ubuntu 18.04

The Data Science stacks are supported on Ubuntu LTS 18.04.1+ with the
4.15+ kernel. Ubuntu can be downloaded from
<https://www.ubuntu.com/download/desktop>

### Red Hat Enterprise Linux (RHEL)

The Data Science stacks are supported on Red Hat Enterprise Linux (RHEL)
version 7.5+ or 8.x.
The RHEL ISO image can be downloaded with the instructions on:
<https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/installation_guide/chap-download-red-hat-enterprise-linux>

#### Red Hat Subscriptions

A Red Hat subscription will be needed to install and use Red Hat Enterprise
Linux. A subscription also lets the system obtain update packages and
additional packages for Red Hat Enterprise Linux. Either purchase a
subscription or obtain a free evaluation subscription from the
Red Hat Software & Download Center -
<https://access.redhat.com/downloads>

Register the system with the RedHat Customer Portal to complete the initial
setup. See the How to Register and Subscribe a system to the Red Hat
Customer Portal using RedHat Subscription-Manager for further information -
<https://access.redhat.com/solutions/253273>

------------------------------------------------------------------------------

## Installing the NVIDIA Accelerated Linux Graphics Driver

It is important that updated NVIDIA drivers are installed on the system.
The minimum version of the NVIDIA driver supported is 440.33.
More recent drivers may be available, but may not have been tested with the
data science stacks.

### Ubuntu 18.04 Driver Install

Driver install for Ubuntu is handled by `data-science-stack setup-system`
so no manual install should be required.

If the driver if too old or the script is having problems, the driver can
be removed (this may have side effects, read the warnings) and reinstalled:

```bash
data-science-stack purge-driver
# reboot
data-science-stack setup-system
# reboot
```

### RedHat Enterprise Linux (RHEL) Driver Install

Before attempting to install the driver, install the base dependencies:

```bash
data-science-stack setup-system
# this will stop one prerequisites are installed
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
sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
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
wget http://us.download.nvidia.com/XFree86/Linux-x86_64/440.44/NVIDIA-Linux-x86_64-440.44.run
sudo sh ./NVIDIA-Linux-x86_64-440.44.run
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

------------------------------------------------------------------------------

## Installing NVIDIA Container SELinux Policy

**This section is only for systems that will use SELinux AND Containers**

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

------------------------------------------------------------------------------

## More Information

* [NVIDIA Accelerated Data Science](https://www.nvidia.com/en-us/deep-learning-ai/solutions/data-science/)
* [RAPIDS - Open GPU Data Science](https://rapids.ai/)
* [NVIDIA Powered Data Science Workstation](https://www.nvidia.com/en-us/deep-learning-ai/solutions/data-science/workstations/)
