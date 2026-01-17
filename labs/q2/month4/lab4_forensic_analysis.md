_of_compromised_system.md", text='# Lab 4: Forensic Analysis of a Compromised System

## Quarter 2, Month 4, Weeks 13-14

### Objective

In this lab, you will conduct a forensic analysis of a disk image from a compromised Windows system. You will use industry-standard tools to examine the file system, analyze memory, and uncover evidence of an intrusion. This lab provides a practical, hands-on experience in digital forensics.

### Learning Outcomes

Upon completion of this lab, you will be able to:

-   Use Autopsy to perform a detailed analysis of a disk image.
-   Use the Volatility Framework to analyze a system memory dump.
-   Identify and extract artifacts of malicious activity from a compromised system.
-   Correlate findings from disk and memory forensics to reconstruct an attack timeline.

### Prerequisites

-   A foundational understanding of the Windows operating system and file systems (NTFS).
-   Familiarity with the basics of digital forensics and incident response.

### Required Tools and Software

-   **Autopsy:** An open-source digital forensics platform.
-   **The Volatility Framework:** An open-source memory forensics framework.
-   A provided disk image (`compromised_system.dd`) and memory dump (`compromised_system.vmem`).

### Part 1: File System Forensics with Autopsy

**Objective:** Analyze the disk image to find evidence of unauthorized access and malicious files.

**Step 1: Create a New Case in Autopsy**

1.  Launch Autopsy and create a new case.
2.  Add the `compromised_system.dd` disk image as a data source.
3.  Configure the ingest modules to run. Ensure that "Recent Activity," "Keyword Search," and "File Type Identification" are enabled.

**Step 2: Analyze the File System**

-   **Deleted Files:** Examine the "Deleted Files" section to find any recently deleted files that may be related to the intrusion.
-   **Web History:** Look at the web history to see if the user visited any suspicious websites.
-   **Keyword Search:** Search for keywords like "malware," "hacker," "password," and any suspicious file names you discover.
-   **Timeline Analysis:** Use the timeline feature to view system activity around the time of the suspected compromise.

**Step 3: Identify Malicious Files**

-   Look for suspicious executables in common locations like `C:\Users\<user>\AppData\Local\Temp`.
-   Examine the "Interesting Files" section for any files that Autopsy has flagged.

### Part 2: Memory Forensics with Volatility

**Objective:** Analyze the memory dump to find running processes, network connections, and other evidence of malware.

**Step 1: Identify the OS Profile**

Use the `imageinfo` plugin to determine the correct profile for the memory dump.

```bash
volatility -f compromised_system.vmem imageinfo
```

**Step 2: Analyze Running Processes**

Use the `pslist` and `pstree` plugins to view the running processes.

```bash
volatility -f compromised_system.vmem --profile=<profile> pslist
volatility -f compromised_system.vmem --profile=<profile> pstree
```

Look for any suspicious or unfamiliar processes.

**Step 3: Analyze Network Connections**

Use the `netscan` plugin to view active network connections at the time of the memory capture.

```bash
volatility -f compromised_system.vmem --profile=<profile> netscan
```

Look for any connections to known malicious IP addresses.

**Step 4: Look for Evidence of Code Injection**

Use the `malfind` plugin to find hidden or injected code in process memory.

```bash
volatility -f compromised_system.vmem --profile=<profile> malfind
```

### Part 3: Reporting

**Objective:** Compile your findings into a professional forensic report.

**Step 1: Correlate Your Findings**

-   Did you find a suspicious file on the disk that corresponds to a running process in memory?
-   Did the web history show the download of a file that you later identified as malware?

**Step 2: Write the Report**

Your report should include:

-   An executive summary of the incident.
-   A detailed timeline of the attack.
-   A list of all the evidence you found, with explanations.
-   Your conclusions about how the system was compromised and what the attacker did.

### Deliverables

1.  **Forensic Report:** A 3-5 page report detailing your findings.
2.  **Extracted Artifacts:** A ZIP file containing any malicious files or other key evidence you extracted.

### Grading Rubric

| Criterion | Points | Description |
| :--- | :--- | :--- |
| Autopsy Analysis | 30 | Thorough and accurate analysis of the disk image. |
| Volatility Analysis | 30 | Correct use of Volatility to analyze the memory dump and identify key artifacts. |
| Correlation of Evidence | 20 | The ability to connect the findings from disk and memory forensics to tell a coherent story. |
| Forensic Report | 20 | A well-written, professional report that clearly communicates the findings. |
| **Total** | **100** | |
'))"
