#!/usr/bin/env python3
from ast import For
import sys
import libvirt
from xml.etree import ElementTree

domName = 'Fedora22-x86_64-1'

conn = None
try:
    conn = libvirt.open("qemu:///system")
except libvirt.libvirtError as e:
    print(repr(e), file=sys.stderr)
    exit(1)

dom = conn.lookupByID(38)
if dom == None:
    print('Failed to find the domain '+domName, file=sys.stderr)
    exit(1)

tree = ElementTree.fromstring(dom.XMLDesc())
devices = tree.findall('devices/disk/target')
for d in devices:
    device = d.get("dev")
    deviceStats = dom.blockStats(device)
    print(deviceStats)
    deviceInfo = dom.blockInfo(device)
    print(deviceInfo)

conn.close()
exit(0)
