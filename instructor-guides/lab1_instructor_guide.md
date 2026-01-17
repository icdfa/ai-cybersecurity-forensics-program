# Instructor Guide: Lab 1 - Automating Network Scanning and Packet Analysis

## 1. Lab Objectives

This lab introduces students to network automation using Python and Scapy. The primary objectives are for students to learn how to:

-   Programmatically discover active hosts on a network.
-   Scan for open ports on a target host.
-   Capture and analyze network packets.

## 2. Preparation

-   **Environment:** Ensure that the lab environment is set up correctly for all students. This includes Python 3.11+, Scapy, and tcpdump.
-   **Network:** For the host discovery part, it is best to have a dedicated lab network with a variety of devices to make the scan interesting. For the port scanning part, have a target machine with a few known open ports (e.g., a web server on port 80, SSH on port 22).
-   **Code:** Have the solution code ready to share with students at the end of the lab.

## 3. Common Issues and Troubleshooting

-   **Permissions:** The packet sniffer script requires `sudo` privileges. Remind students to run it with `sudo`.
-   **Scapy Installation:** Some students may face issues with Scapy installation. Be prepared to help them troubleshoot.
-   **Network Configuration:** If students are on different networks, their host discovery results will vary. This is a good opportunity to discuss network segmentation.
-   **Firewalls:** Firewalls on the target machine or the network may block the port scan. This can be a teachable moment about firewall evasion techniques.

## 4. Discussion Points

-   **Ethical Considerations:** Discuss the ethical implications of network scanning. When is it legal and ethical, and when is it not?
-   **Stealth Scans:** Explain the difference between a full TCP connect scan and a SYN scan (stealth scan) and why the latter is often preferred by attackers.
-   **Limitations of Packet Sniffing:** Discuss the limitations of packet sniffing in a switched network environment (i.e., you can only see traffic to and from your own machine, or broadcast traffic).

## 5. Grading and Feedback

-   **Code Review:** When grading the Python scripts, look for correctness, clarity, and comments.
-   **Report Analysis:** In the lab report, students should not just present the output, but also interpret it. For example, what could the open ports on a machine indicate? What kind of traffic did they observe, and was any of it suspicious?
-   **Encourage Exploration:** Encourage students to go beyond the lab instructions. For example, can they modify the port scanner to scan for UDP ports? Can they add a feature to the packet sniffer to detect a specific type of traffic?
