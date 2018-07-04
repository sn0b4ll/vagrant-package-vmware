#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import tarfile

from os import system as run

parser = argparse.ArgumentParser()
parser.add_argument("vmx", help="path to the vmx-file")
parser.add_argument("vmdk", help="path to the main vmdk")
parser.add_argument("name", help="box-name")
parser.add_argument("version", help="version-identifier")
parser.add_argument(
    "--compression-level", 
    dest='compresslevel',
    type=int, 
    help="compression-level for tar (default=6)", 
    default=6)
parser.add_argument(
    "--dest-dir", 
    dest='dest_dir',
    type=str, 
    help="Specify the destination dir for the box file (default=.)", 
    default=".")
args = parser.parse_args()

# Defrag and shrink the vmdk-files
print("[+] Defragging and shrinking disk.")
# run("vmware-vdiskmanager -d '{}'".format(args.vmdk))
# run("vmware-vdiskmanager -k '{}'".format(args.vmdk))

# Create metadata-file
metadata ="""{
  "provider": "vmware_workstation"
}"""
# metadata_file = open("metadata.json", 'w')
# metadata_file.write(metadata)
# metadata_file.close()

# Build regex to find the currently used vmdk-files to pack
# See specification from vmware http://www.vmware.com/app/vmdk/?src=vmdk
re_access = "(?:RW|RDONLY|NOACCESS)"
re_size = "\d+"
re_type = "(?:FLAT|SPARSE|ZERO|VMFS|VMFSSPARSE|VMFSRDM|VMFSRAW)"
re_name = "\"(.*)\""

re_vmdk = re.compile(
    re_access + "\s" + 
    re_size + "\s" + 
    re_type + "\s" +
    re_name)
    
vmdk_list = re_vmdk.findall(open(args.vmdk).read())

# Add all other files which should be packed into the box
# See vagrant box documentation
# https://www.vagrantup.com/docs/vmware/boxes.html

# Open the tarfile
print("[+] Creating .box-file - hang on, this might take some time.")
box_file = tarfile.open(
    "{}/{}_{}.box".format(args.dest_dir, args.name, args.version),
    'w:gz',
    compresslevel=args.compresslevel
)

# Get the path and append to sub-vmdks
path, filename = os.path.split(args.vmdk)
for vmdk_file in vmdk_list:
    print("[*] Adding vmdk-file {} from {}.".format(
            vmdk_list.index(vmdk_file)+1,
            len(vmdk_list)
        )
    )
    box_file.add(path + "/" + vmdk_file)
    
print("[*] Adding other files, this should be fast.")
box_file.add(args.vmdk)
box_file.add(args.vmx)

vm_name = re.match("(.*)\.vmx", args.vmx).group(1)
box_file.add("{}.nvram".format(vm_name))
box_file.add("{}.vmsd".format(vm_name))
box_file.add("{}.vmxf".format(vm_name))

box_file.addfile(tarfile.TarInfo("metadata.json"), metadata)
    
box_file.close()
