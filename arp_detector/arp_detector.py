import scapy.all as scapy


def get_mac_address(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    requested_broadcast = broadcast / request
    answer = scapy.srp(requested_broadcast, timeout=1, verbose=False)[0]
    return answer[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=processed_sniff_packets)


def processed_sniff_packets(packet):
    try:
        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            real_mac = get_mac_address(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            packet.show()
            if response_mac != real_mac:
                print('[+] you are under attack!')
    except:
        pass

sniff('wlan0')
