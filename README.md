# vagrant-package-vmware
Python3-Script to back a VM from VMWare to a Vagrant Box.

# Usage
```
usage: vagrant-package-vmware.py [-h] [--vmdk VMDK]
                                 [--compression-level COMPRESSLEVEL]
                                 [--dest-dir DEST_DIR]
                                 vmx name version

positional arguments:
  vmx                   path to the vmx-file
  name                  box-name
  version               version-identifier

optional arguments:
  -h, --help            show this help message and exit
  --vmdk VMDK           path to the main vmdk
  --compression-level COMPRESSLEVEL
                        compression-level for tar (default=6)
  --dest-dir DEST_DIR   Specify the destination dir for the box file
                        (default=.)
```
# Issues
Please feel free to open issues in Github.
