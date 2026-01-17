# Lab 1 Worksheet: Network Scanning and Packet Analysis

**Student Name:** ___________________________  
**Date:** ___________________________  
**Lab Duration:** 4 hours

## Learning Objectives

By the end of this lab, you will be able to:
- Perform network reconnaissance using Scapy
- Analyze network packets and extract meaningful information
- Identify suspicious network activity
- Document findings in a professional manner

---

## Part 1: Environment Setup (30 minutes)

### Task 1.1: Verify Python Environment

Run the following command and record the output:

```bash
python3 --version
```

**Python Version:** ___________________________

### Task 1.2: Install Required Packages

```bash
pip3 install scapy pandas
```

**Installation Status:** ☐ Success ☐ Failed

If failed, describe the error:
___________________________________________________________________________

### Task 1.3: Test Scapy Installation

```bash
python3 -c "from scapy.all import *; print('Scapy installed successfully!')"
```

**Test Result:** ☐ Pass ☐ Fail

---

## Part 2: Network Discovery (60 minutes)

### Task 2.1: ARP Scan

Perform an ARP scan on your local network:

```bash
sudo python3 network_scanner.py --arp-scan 192.168.1.0/24
```

**Number of hosts discovered:** ___________________________

**List the first 5 discovered hosts:**

| IP Address | MAC Address |
|------------|-------------|
| 1. | |
| 2. | |
| 3. | |
| 4. | |
| 5. | |

### Task 2.2: ICMP Ping

Test connectivity to a specific host:

```bash
python3 network_scanner.py --ping 192.168.1.1
```

**Target IP:** ___________________________  
**Result:** ☐ Host is ALIVE ☐ Host is DOWN

---

## Part 3: Port Scanning (60 minutes)

### Task 3.1: TCP Port Scan

Scan common ports on a target system:

```bash
python3 network_scanner.py --tcp-scan 192.168.1.1 --ports 80,443,22,21,25,53
```

**Target IP:** ___________________________

**Record open ports:**

| Port | Service | Status |
|------|---------|--------|
| 80 | HTTP | |
| 443 | HTTPS | |
| 22 | SSH | |
| 21 | FTP | |
| 25 | SMTP | |
| 53 | DNS | |

### Task 3.2: Analysis Questions

1. Which ports are open on the target system?

___________________________________________________________________________

2. What services are likely running based on the open ports?

___________________________________________________________________________

3. Are there any security concerns with the open ports? Explain.

___________________________________________________________________________
___________________________________________________________________________

---

## Part 4: Packet Analysis (90 minutes)

### Task 4.1: Capture Packets

Capture network packets (requires root/admin privileges):

```bash
sudo python3 network_scanner.py --sniff eth0 --count 50
```

**Interface used:** ___________________________  
**Number of packets captured:** ___________________________

### Task 4.2: Analyze PCAP File

Use the packet analyzer to examine a captured PCAP file:

```bash
python3 packet_analyzer.py ../data/sample_capture.pcap
```

**Total packets in PCAP:** ___________________________

**Protocol distribution:**

| Protocol | Count | Percentage |
|----------|-------|------------|
| TCP | | |
| UDP | | |
| ICMP | | |
| Other | | |

### Task 4.3: Top Communicators

**Top 3 source IP addresses:**

1. ___________________________
2. ___________________________
3. ___________________________

**Top 3 destination IP addresses:**

1. ___________________________
2. ___________________________
3. ___________________________

### Task 4.4: Port Analysis

**Top 3 destination ports:**

| Port | Service | Count |
|------|---------|-------|
| 1. | | |
| 2. | | |
| 3. | | |

---

## Part 5: Threat Detection (30 minutes)

### Task 5.1: Identify Suspicious Activity

Review your packet analysis results and identify any suspicious patterns:

**Suspicious Pattern 1:**
___________________________________________________________________________
___________________________________________________________________________

**Suspicious Pattern 2:**
___________________________________________________________________________
___________________________________________________________________________

**Suspicious Pattern 3:**
___________________________________________________________________________
___________________________________________________________________________

### Task 5.2: Recommendations

Based on your findings, what security recommendations would you make?

1. ___________________________________________________________________________

2. ___________________________________________________________________________

3. ___________________________________________________________________________

---

## Part 6: Lab Report (30 minutes)

### Task 6.1: Executive Summary

Write a brief executive summary (3-5 sentences) of your findings:

___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________

### Task 6.2: Technical Details

**Methodology:**
___________________________________________________________________________
___________________________________________________________________________

**Key Findings:**
___________________________________________________________________________
___________________________________________________________________________

**Recommendations:**
___________________________________________________________________________
___________________________________________________________________________

---

## Deliverables Checklist

☐ Completed worksheet with all tasks  
☐ Screenshots of scan results  
☐ Packet analysis report (JSON file)  
☐ Lab report (1-2 pages)  
☐ Code modifications (if any)

---

## Reflection Questions

1. What was the most challenging part of this lab?

___________________________________________________________________________
___________________________________________________________________________

2. What did you learn about network reconnaissance?

___________________________________________________________________________
___________________________________________________________________________

3. How could the techniques learned in this lab be used by attackers?

___________________________________________________________________________
___________________________________________________________________________

4. What defensive measures can organizations implement against these techniques?

___________________________________________________________________________
___________________________________________________________________________

---

## Grading Rubric

| Category | Points | Score |
|----------|--------|-------|
| Environment Setup | 10 | |
| Network Discovery | 20 | |
| Port Scanning | 20 | |
| Packet Analysis | 30 | |
| Threat Detection | 10 | |
| Lab Report | 10 | |
| **Total** | **100** | |

---

**Instructor Signature:** ___________________________  
**Date Graded:** ___________________________

**Comments:**
___________________________________________________________________________
___________________________________________________________________________
___________________________________________________________________________
