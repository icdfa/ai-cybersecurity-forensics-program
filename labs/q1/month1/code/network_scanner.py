#!/usr/bin/env python3
"""
Lab 1: Network Scanner
Advanced AI in Cybersecurity and Digital Forensics Program

This script demonstrates network scanning techniques using Scapy.
It includes host discovery, port scanning, and packet analysis.

Author: Manus AI
Date: January 2026
"""

from scapy.all import ARP, Ether, srp, sr1, IP, TCP, ICMP
import argparse
import sys
from datetime import datetime

def print_banner():
    """Print a banner for the network scanner"""
    print("=" * 60)
    print("Network Scanner - Lab 1")
    print("Advanced AI in Cybersecurity and Digital Forensics")
    print("=" * 60)
    print()

def arp_scan(network):
    """
    Perform ARP scan to discover hosts on the local network
    
    Args:
        network (str): Network range in CIDR notation (e.g., '192.168.1.0/24')
    
    Returns:
        list: List of discovered hosts with IP and MAC addresses
    """
    print(f"[*] Scanning network: {network}")
    print("[*] Performing ARP scan...")
    
    # Create ARP request packet
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    
    # Send packet and receive responses
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    hosts = []
    for sent, received in answered_list:
        hosts.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })
    
    print(f"[+] Found {len(hosts)} active hosts")
    print()
    print("IP Address\t\tMAC Address")
    print("-" * 45)
    for host in hosts:
        print(f"{host['ip']}\t\t{host['mac']}")
    print()
    
    return hosts

def tcp_port_scan(target, ports):
    """
    Perform TCP SYN scan on specified ports
    
    Args:
        target (str): Target IP address
        ports (list): List of ports to scan
    
    Returns:
        dict: Dictionary of open ports and their states
    """
    print(f"[*] Scanning {target} for open ports...")
    print(f"[*] Ports to scan: {ports}")
    print()
    
    open_ports = []
    
    for port in ports:
        # Create SYN packet
        syn_packet = IP(dst=target) / TCP(dport=port, flags="S")
        
        # Send packet and wait for response
        response = sr1(syn_packet, timeout=1, verbose=False)
        
        if response is not None:
            if response.haslayer(TCP):
                if response[TCP].flags == 0x12:  # SYN-ACK
                    open_ports.append(port)
                    print(f"[+] Port {port}: OPEN")
                    
                    # Send RST to close connection
                    rst_packet = IP(dst=target) / TCP(dport=port, flags="R")
                    sr1(rst_packet, timeout=1, verbose=False)
                elif response[TCP].flags == 0x14:  # RST-ACK
                    print(f"[-] Port {port}: CLOSED")
        else:
            print(f"[-] Port {port}: FILTERED/NO RESPONSE")
    
    print()
    print(f"[+] Scan complete. {len(open_ports)} open ports found.")
    return open_ports

def icmp_ping(target):
    """
    Perform ICMP ping to check if host is alive
    
    Args:
        target (str): Target IP address
    
    Returns:
        bool: True if host is alive, False otherwise
    """
    print(f"[*] Pinging {target}...")
    
    icmp_packet = IP(dst=target) / ICMP()
    response = sr1(icmp_packet, timeout=2, verbose=False)
    
    if response is not None:
        print(f"[+] Host {target} is ALIVE")
        return True
    else:
        print(f"[-] Host {target} is DOWN or not responding")
        return False

def packet_sniffer(interface, count=10):
    """
    Sniff packets on the specified interface
    
    Args:
        interface (str): Network interface to sniff on
        count (int): Number of packets to capture
    """
    from scapy.all import sniff
    
    print(f"[*] Starting packet capture on {interface}")
    print(f"[*] Capturing {count} packets...")
    print()
    
    def packet_callback(packet):
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            
            print(f"[+] Packet: {src_ip} -> {dst_ip} (Protocol: {protocol})")
            
            if packet.haslayer(TCP):
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                print(f"    TCP: {src_port} -> {dst_port}")
            elif packet.haslayer(ICMP):
                print(f"    ICMP packet")
    
    packets = sniff(iface=interface, count=count, prn=packet_callback, timeout=30)
    print()
    print(f"[+] Captured {len(packets)} packets")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Network Scanner - Lab 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # ARP scan a network
  python network_scanner.py --arp-scan 192.168.1.0/24
  
  # TCP port scan
  python network_scanner.py --tcp-scan 192.168.1.1 --ports 80,443,22,21
  
  # ICMP ping
  python network_scanner.py --ping 192.168.1.1
  
  # Packet sniffing (requires root/admin)
  sudo python network_scanner.py --sniff eth0 --count 20
        """
    )
    
    parser.add_argument('--arp-scan', metavar='NETWORK', 
                       help='Perform ARP scan on network (e.g., 192.168.1.0/24)')
    parser.add_argument('--tcp-scan', metavar='TARGET', 
                       help='Perform TCP port scan on target IP')
    parser.add_argument('--ports', metavar='PORTS', default='80,443,22,21,25,53',
                       help='Comma-separated list of ports to scan (default: 80,443,22,21,25,53)')
    parser.add_argument('--ping', metavar='TARGET', 
                       help='Perform ICMP ping on target IP')
    parser.add_argument('--sniff', metavar='INTERFACE', 
                       help='Sniff packets on specified interface')
    parser.add_argument('--count', type=int, default=10, 
                       help='Number of packets to capture (default: 10)')
    
    args = parser.parse_args()
    
    print_banner()
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if args.arp_scan:
        arp_scan(args.arp_scan)
    
    elif args.tcp_scan:
        ports = [int(p.strip()) for p in args.ports.split(',')]
        tcp_port_scan(args.tcp_scan, ports)
    
    elif args.ping:
        icmp_ping(args.ping)
    
    elif args.sniff:
        packet_sniffer(args.sniff, args.count)
    
    else:
        parser.print_help()
        sys.exit(1)
    
    print()
    print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
