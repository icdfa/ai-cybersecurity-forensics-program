# Quarter 1, Month 1: Python for Cybersecurity & Fundamentals of AI/ML

## Overview

This month introduces students to Python programming for cybersecurity applications and the fundamental concepts of artificial intelligence and machine learning.

---

## Lab 1: Automating Network Scanning and Packet Analysis

### Learning Outcomes

Upon completion of this lab, students will be able to:

- Write Python scripts to automate network scanning tasks
- Use Scapy to craft and send custom network packets
- Analyze packet captures to identify network protocols and suspicious activity
- Develop a basic port scanner and host discovery tool
- Document security findings in a professional manner

### Prerequisites

- Python 3.8 or higher installed
- Basic understanding of networking concepts (TCP/IP, ports, protocols)
- Linux/Unix environment or Windows with WSL2
- Root/administrator privileges for packet capture

### Lab Duration

**4 hours** (Weeks 1-2)

---

## Required Tools and Datasets

### Code Files (Included)

- **`code/network_scanner.py`** - Network scanning tool with ARP scan, TCP scan, ICMP ping, and packet sniffing capabilities
- **`code/packet_analyzer.py`** - Packet analysis tool for PCAP file examination

### Sample Data

- **`data/sample_capture.pcap`** - Sample packet capture file (generate using the scanner)

### External Datasets (Optional for Advanced Study)

- **CTU-13 Botnet Traffic Dataset**  
  URL: https://www.stratosphereips.org/datasets-ctu-13  
  Size: ~32 GB  
  Description: Real botnet traffic for advanced analysis

- **CIC-IDS-2017 Intrusion Detection Dataset**  
  URL: https://www.unb.ca/cic/datasets/ids-2017.html  
  Size: ~7 GB  
  Description: Labeled network intrusion traffic

For detailed download instructions, see [DATASETS.md](../../../resources/datasets/DATASETS.md#lab-1-automating-network-scanning-and-packet-analysis)

---

## Lab Structure

```
month1/
├── README.md                    # This file
├── lab1_network_scanning.md     # Detailed lab instructions
├── code/
│   ├── network_scanner.py       # Main scanning tool
│   └── packet_analyzer.py       # Packet analysis tool
├── data/
│   └── (PCAP files generated during lab)
└── worksheets/
    └── lab1_worksheet.md        # Lab worksheet for submission
```

---

## Quick Start Guide

### Step 1: Navigate to Lab Directory

```bash
cd labs/q1/month1
```

### Step 2: Read Lab Instructions

```bash
cat lab1_network_scanning.md
```

### Step 3: Review Code

```bash
# View network scanner help
cd code
python3 network_scanner.py --help

# View packet analyzer help
python3 packet_analyzer.py --help
```

### Step 4: Run Network Scanner

```bash
# ARP scan (discover hosts on local network)
sudo python3 network_scanner.py --arp-scan 192.168.1.0/24

# TCP port scan
sudo python3 network_scanner.py --tcp-scan 192.168.1.1 --ports 80,443,22,21

# ICMP ping
python3 network_scanner.py --ping 192.168.1.1

# Packet sniffing (requires root)
sudo python3 network_scanner.py --sniff eth0 --count 50
```

### Step 5: Analyze Captured Packets

```bash
# Analyze PCAP file
python3 packet_analyzer.py capture.pcap

# Extract HTTP requests
python3 packet_analyzer.py capture.pcap --http

# Save results to JSON
python3 packet_analyzer.py capture.pcap --output results.json
```

---

## Topics Covered

### Week 1: Network Reconnaissance
- Python scripting for network automation
- Scapy library for packet manipulation
- Host discovery with ARP scanning
- ICMP ping sweeps
- TCP/UDP port scanning techniques

### Week 2: Packet Analysis
- Packet capture and sniffing
- Protocol analysis (TCP, UDP, ICMP, HTTP)
- Traffic pattern identification
- Anomaly detection
- Forensic analysis of network traffic

---

## Deliverables

### Required Submissions

1. **Completed Worksheet** (`worksheets/lab1_worksheet.md`)
   - All tasks completed
   - Questions answered
   - Results documented

2. **Network Scan Results**
   - Screenshots of ARP scan
   - Screenshots of port scan
   - Packet capture files (PCAP)

3. **Packet Analysis Report**
   - JSON output from packet analyzer
   - Analysis of protocol distribution
   - Identification of top communicators

4. **Lab Report** (1-2 pages)
   - Executive summary
   - Methodology
   - Key findings
   - Security recommendations

### Submission Format

- Create a folder: `lab1_submission_[YourName]`
- Include all deliverables
- Compress as ZIP file
- Submit via learning management system

---

## Assessment Criteria

### Grading Rubric (100 points total)

| Category | Points | Description |
|----------|--------|-------------|
| Environment Setup | 10 | Successful installation and configuration |
| Network Discovery | 20 | Correct execution of ARP and ICMP scans |
| Port Scanning | 20 | Accurate port scanning and service identification |
| Packet Analysis | 30 | Thorough analysis of captured traffic |
| Threat Detection | 10 | Identification of suspicious patterns |
| Lab Report | 10 | Professional documentation of findings |

### Evaluation Criteria

- **Technical Accuracy:** Correct use of tools and techniques
- **Completeness:** All tasks completed as specified
- **Analysis Quality:** Depth of analysis and insights
- **Documentation:** Clear, professional reporting
- **Security Awareness:** Understanding of security implications

---

## Common Issues and Troubleshooting

### Issue: Permission Denied

**Problem:** Cannot run packet capture or ARP scan

**Solution:**
```bash
# Run with sudo
sudo python3 network_scanner.py --arp-scan 192.168.1.0/24
```

### Issue: Module Not Found

**Problem:** Scapy not installed

**Solution:**
```bash
pip3 install scapy
```

### Issue: No Packets Captured

**Problem:** Wrong network interface

**Solution:**
```bash
# List available interfaces
ip link show  # Linux
ifconfig      # macOS

# Use correct interface name
sudo python3 network_scanner.py --sniff eth0 --count 50
```

### Issue: Timeout Errors

**Problem:** Target host not responding

**Solution:**
- Verify target IP is correct
- Check if target is online
- Adjust timeout values in code
- Check firewall rules

---

## Additional Resources

### Documentation

- **Scapy Documentation:** https://scapy.readthedocs.io/
- **Python Socket Programming:** https://docs.python.org/3/library/socket.html
- **Wireshark User Guide:** https://www.wireshark.org/docs/

### Tools

- **Wireshark:** GUI packet analyzer
- **tcpdump:** Command-line packet analyzer
- **Nmap:** Advanced network scanner

### Reading Materials

- RFC 791 (Internet Protocol)
- RFC 793 (TCP)
- RFC 826 (ARP)
- NIST Cybersecurity Framework

### Video Tutorials

- Scapy Tutorial Series
- Network Protocol Analysis
- Ethical Hacking Basics

---

## Lab Extensions (Optional)

For students who complete the lab early or want additional challenges:

1. **Advanced Port Scanning**
   - Implement UDP scanning
   - Add service version detection
   - Create stealth scanning techniques

2. **Protocol Analysis**
   - Add DNS query analysis
   - Extract HTTP headers
   - Decode SSL/TLS handshakes

3. **Automation**
   - Create scheduled scanning
   - Build alerting system
   - Generate HTML reports

4. **Machine Learning Integration**
   - Train anomaly detection model
   - Classify traffic patterns
   - Predict attack vectors

---

## Safety and Ethics

### Important Reminders

- **Only scan networks you own or have explicit permission to test**
- **Never use these tools on production systems without authorization**
- **Respect privacy and legal boundaries**
- **Follow your organization's security policies**

### Legal Considerations

Unauthorized network scanning may violate:
- Computer Fraud and Abuse Act (CFAA) in the US
- Computer Misuse Act in the UK
- Similar laws in other jurisdictions

Always obtain written permission before conducting security assessments.

---

## Next Steps

After completing this lab:

1. Review your findings with peers
2. Practice on additional networks (with permission)
3. Explore advanced Scapy features
4. Proceed to Lab 2: Threat Intelligence Pipeline

---

**Questions or Issues?**

- Check the FAQ in `lab1_network_scanning.md`
- Review troubleshooting section above
- Ask instructor during office hours
- Post in course discussion forum

---

**Last Updated:** January 2026
