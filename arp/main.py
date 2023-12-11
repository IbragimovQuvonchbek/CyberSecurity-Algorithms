#!/usr/bin/env python3

import scapy.all as scapy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--range', dest='range', help='ip address range to scan')
options = parser.parse_args()


def scan(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    requested_broadcast = broadcast / request
    (answered, unanswered) = scapy.srp(requested_broadcast, timeout=1, verbose=False)
    address = []
    for e in answered:
        address.append({'ip': e[1].psrc, 'mac': e[1].src})
    return address


def print_scan(address):
    print("-IP address-----------------Mac address--------")
    for e in address:
        print(f"| {e['ip']}            {e['mac']}    |")
        print('-----------------------------------------------')


print_scan(scan(f"{options.range}"))