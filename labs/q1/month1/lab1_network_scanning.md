# Lab 1: Automating Network Scanning and Packet Analysis

## Quarter 1, Month 1, Weeks 1-2

### Objective

This lab will introduce you to the fundamentals of network automation using Python and the Scapy library. You will learn how to programmatically scan a network to discover active hosts and open ports, and how to capture and analyze network packets. This lab provides the foundational skills for building more advanced network security tools.

### Learning Outcomes

Upon completion of this lab, you will be able to:

- Write Python scripts to automate network scanning tasks.
- Use Scapy to craft and send custom network packets.
- Analyze packet captures to identify network protocols and potential anomalies.
- Develop a basic port scanner and host discovery tool.

### Prerequisites

- Basic understanding of computer networking concepts (IP addressing, TCP/IP, ports).
- Python 3.11+ installed.
- Familiarity with the Linux command line.

### Required Tools and Libraries

```bash
sudo apt-get update
sudo apt-get install -y tcpdump
pip install scapy
```

### Part 1: Host Discovery with ARP Scan

**Objective:** Discover active hosts on the local network using ARP requests.

**Step 1: Create the Python Script**

Create a file named `host_discovery.py` and add the following code:

```python
from scapy.all import ARP, Ether, srp

# Define the target network
target_ip = "192.168.1.1/24"

# Create an ARP request packet
arp = ARP(pdst=target_ip)

# Create an Ethernet frame
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# Stack the layers
packet = ether/arp

# Send the packet and receive the response
result = srp(packet, timeout=3, verbose=0)[0]

# Parse the response
clients = []
for sent, received in result:
    clients.append({"ip": received.psrc, "mac": received.hwsrc})

# Print the discovered clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client["ip"], client["mac"]))
```

**Step 2: Run the Script**

Execute the script from your terminal:

```bash
python3 host_discovery.py
```

**Expected Output:** A list of IP and MAC addresses of active devices on your local network.

### Part 2: Port Scanning with TCP SYN Scan

**Objective:** Identify open TCP ports on a target host using a SYN scan (half-open scan).

**Step 1: Create the Python Script**

Create a file named `port_scanner.py` and add the following code:

```python
from scapy.all import sr1, IP, TCP

# Define the target and port range
target = "127.0.0.1"  # Replace with your target IP
ports_to_scan = range(1, 1025)

open_ports = []

# Iterate over the ports and send a SYN packet
for port in ports_to_scan:
    # Craft the packet
    pkt = IP(dst=target)/TCP(sport=1500, dport=port, flags="S")

    # Send the packet and receive the response
    response = sr1(pkt, timeout=1, verbose=0)

    # Check if the port is open
    if response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
        open_ports.append(port)
        # Send a RST packet to close the connection
        sr1(IP(dst=target)/TCP(sport=1500, dport=port, flags="R"), timeout=1, verbose=0)

# Print the open ports
if open_ports:
    print(f"Open ports on {target}:")
    for port in open_ports:
        print(port)
else:
    print(f"No open ports found on {target}.")
```

**Step 2: Run the Script**

Execute the script from your terminal:

```bash
python3 port_scanner.py
```

**Expected Output:** A list of open TCP ports on the target host.

### Part 3: Packet Sniffing and Analysis

**Objective:** Capture and analyze network traffic to identify protocols and data.

**Step 1: Create the Python Script**

Create a file named `packet_sniffer.py` and add the following code:

```python
from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP

# Define the callback function to process each packet
def packet_callback(packet):
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        print(f"[+] New Packet: {ip_layer.src} -> {ip_layer.dst}")

    if packet.haslayer(TCP):
        tcp_layer = packet.getlayer(TCP)
        print(f"    [*] Protocol: TCP, Port: {tcp_layer.dport}")

    if packet.haslayer(UDP):
        udp_layer = packet.getlayer(UDP)
        print(f"    [*] Protocol: UDP, Port: {udp_layer.dport}")

# Start sniffing
print("Starting packet sniffer...")
sniff(filter="ip", prn=packet_callback, store=0, count=20) # Sniff 20 packets
print("\nPacket sniffing complete.")
```

**Step 2: Run the Script**

Execute the script with sudo privileges:

```bash
sudo python3 packet_sniffer.py
```

**Expected Output:** A real-time display of captured packets, showing source and destination IPs, protocols, and ports.

### Deliverables

1.  **Python Scripts:** Submit your `host_discovery.py`, `port_scanner.py`, and `packet_sniffer.py` scripts.
2.  **Lab Report:** A 1-2 page report that includes:
    *   Screenshots of the output from each script.
    *   A brief explanation of how each script works.
    *   A discussion on the potential security implications of the information gathered from these tools.

### Grading Rubric

| Criterion | Points | Description |
| :--- | :--- | :--- |
| Host Discovery Script | 30 | Correctly implements ARP scan and discovers hosts. |
| Port Scanner Script | 40 | Correctly implements TCP SYN scan and identifies open ports. |
| Packet Sniffer Script | 20 | Correctly captures and analyzes network packets. |
| Lab Report | 10 | Clear, concise, and well-documented report with all required elements. |
| **Total** | **100** | |
