#!/usr/bin/env python3
"""
Lab 1: Packet Analyzer
Advanced AI in Cybersecurity and Digital Forensics Program

This script analyzes captured packets from a PCAP file.

Author: Manus AI
Date: January 2026
"""

from scapy.all import rdpcap, IP, TCP, UDP, ICMP, DNS, ARP
import argparse
from collections import Counter
import json

def analyze_pcap(pcap_file):
    """
    Analyze a PCAP file and extract statistics
    
    Args:
        pcap_file (str): Path to PCAP file
    
    Returns:
        dict: Analysis results
    """
    print(f"[*] Reading PCAP file: {pcap_file}")
    packets = rdpcap(pcap_file)
    print(f"[+] Loaded {len(packets)} packets")
    print()
    
    # Initialize counters
    protocol_count = Counter()
    src_ips = Counter()
    dst_ips = Counter()
    src_ports = Counter()
    dst_ports = Counter()
    
    # Analyze packets
    for packet in packets:
        # Protocol analysis
        if packet.haslayer(TCP):
            protocol_count['TCP'] += 1
            src_ports[packet[TCP].sport] += 1
            dst_ports[packet[TCP].dport] += 1
        elif packet.haslayer(UDP):
            protocol_count['UDP'] += 1
            src_ports[packet[UDP].sport] += 1
            dst_ports[packet[UDP].dport] += 1
        elif packet.haslayer(ICMP):
            protocol_count['ICMP'] += 1
        elif packet.haslayer(ARP):
            protocol_count['ARP'] += 1
        
        # IP address analysis
        if packet.haslayer(IP):
            src_ips[packet[IP].src] += 1
            dst_ips[packet[IP].dst] += 1
    
    # Print results
    print("=" * 60)
    print("PACKET ANALYSIS RESULTS")
    print("=" * 60)
    print()
    
    print("Protocol Distribution:")
    print("-" * 30)
    for protocol, count in protocol_count.most_common():
        percentage = (count / len(packets)) * 100
        print(f"{protocol}: {count} packets ({percentage:.2f}%)")
    print()
    
    print("Top 10 Source IP Addresses:")
    print("-" * 30)
    for ip, count in src_ips.most_common(10):
        print(f"{ip}: {count} packets")
    print()
    
    print("Top 10 Destination IP Addresses:")
    print("-" * 30)
    for ip, count in dst_ips.most_common(10):
        print(f"{ip}: {count} packets")
    print()
    
    print("Top 10 Source Ports:")
    print("-" * 30)
    for port, count in src_ports.most_common(10):
        print(f"Port {port}: {count} packets")
    print()
    
    print("Top 10 Destination Ports:")
    print("-" * 30)
    for port, count in dst_ports.most_common(10):
        service = get_service_name(port)
        print(f"Port {port} ({service}): {count} packets")
    print()
    
    # Return results as dictionary
    return {
        'total_packets': len(packets),
        'protocols': dict(protocol_count),
        'top_src_ips': dict(src_ips.most_common(10)),
        'top_dst_ips': dict(dst_ips.most_common(10)),
        'top_src_ports': dict(src_ports.most_common(10)),
        'top_dst_ports': dict(dst_ports.most_common(10))
    }

def get_service_name(port):
    """
    Get common service name for a port number
    
    Args:
        port (int): Port number
    
    Returns:
        str: Service name
    """
    common_ports = {
        20: 'FTP-DATA',
        21: 'FTP',
        22: 'SSH',
        23: 'TELNET',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        8080: 'HTTP-ALT'
    }
    return common_ports.get(port, 'UNKNOWN')

def extract_http_requests(pcap_file):
    """
    Extract HTTP requests from PCAP file
    
    Args:
        pcap_file (str): Path to PCAP file
    """
    print(f"[*] Extracting HTTP requests from: {pcap_file}")
    packets = rdpcap(pcap_file)
    
    http_requests = []
    for packet in packets:
        if packet.haslayer(TCP) and packet.haslayer(IP):
            if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                if packet.haslayer('Raw'):
                    payload = packet['Raw'].load.decode('utf-8', errors='ignore')
                    if payload.startswith('GET') or payload.startswith('POST'):
                        http_requests.append({
                            'src': packet[IP].src,
                            'dst': packet[IP].dst,
                            'method': payload.split()[0],
                            'uri': payload.split()[1] if len(payload.split()) > 1 else 'N/A'
                        })
    
    print(f"[+] Found {len(http_requests)} HTTP requests")
    print()
    
    for i, req in enumerate(http_requests[:10], 1):
        print(f"{i}. {req['method']} {req['uri']}")
        print(f"   {req['src']} -> {req['dst']}")
        print()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Packet Analyzer - Lab 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a PCAP file
  python packet_analyzer.py capture.pcap
  
  # Extract HTTP requests
  python packet_analyzer.py capture.pcap --http
  
  # Save results to JSON
  python packet_analyzer.py capture.pcap --output results.json
        """
    )
    
    parser.add_argument('pcap_file', help='Path to PCAP file')
    parser.add_argument('--http', action='store_true', 
                       help='Extract HTTP requests')
    parser.add_argument('--output', metavar='FILE', 
                       help='Save results to JSON file')
    
    args = parser.parse_args()
    
    # Analyze PCAP
    results = analyze_pcap(args.pcap_file)
    
    # Extract HTTP requests if requested
    if args.http:
        print()
        extract_http_requests(args.pcap_file)
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to: {args.output}")

if __name__ == "__main__":
    main()
