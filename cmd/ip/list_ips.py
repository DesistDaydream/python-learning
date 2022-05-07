#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ipaddress

# 根据网段生成IP地址
def get_ips(net):
    net = ipaddress.ip_network(net)
    for x in net.hosts():
        print(x)


if __name__ == "__main__":
    get_ips("192.168.1.0/28")
