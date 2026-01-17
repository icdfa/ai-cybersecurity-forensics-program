# Lab 5: Automated Attack Timeline Generation

## Quarter 2, Month 5, Weeks 17-18

### Objective

This lab focuses on using AI techniques to automatically reconstruct an attack timeline from various log sources. You will learn how to parse and correlate events from different logs (e.g., web server, firewall, and system logs) to build a coherent and chronological view of a security incident.

### Learning Outcomes

Upon completion of this lab, you will be able to:

-   Parse and normalize log data from multiple sources.
-   Correlate events across different log files based on timestamps and other indicators.
-   Use graph-based analysis to visualize the attack path.
-   Develop a Python script to automate the generation of an attack timeline.

### Prerequisites

-   Completion of Lab 4: Forensic Analysis of a Compromised System.
-   Strong understanding of common log formats (e.g., Apache, syslog).
-   Familiarity with Python, Pandas, and the NetworkX library.

### Required Tools and Libraries

```bash
pip install pandas networkx matplotlib
```

### Part 1: Log Parsing and Normalization

**Objective:** Parse and normalize logs from different sources into a structured format.

**Step 1: Create the Python Script**

Create a file named `timeline_generator.py` and add the following code to parse and combine different log files.

```python
import pandas as pd
import re

# Function to parse Apache access logs
def parse_apache_log(log_file):
    log_pattern = re.compile(r'("S+)"s("S+)"s("S+)"s"[("S+)"s"S+]"s"("d{3})"s("d+)"s"("[^"]*")"s"("[^"]*")')
    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            match = log_pattern.match(line)
            if match:
                logs.append(match.groups())
    df = pd.DataFrame(logs, columns=['ip', 'ident', 'user', 'timestamp', 'status', 'size', 'referer', 'user_agent'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S')
    return df

# Function to parse syslog files
def parse_syslog(log_file):
    log_pattern = re.compile(r'("S{3})"s+("d{1,2})"s("d{2}:"d{2}:"d{2})"s("S+)"s("S+)"s:(.*)')
    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            match = log_pattern.match(line)
            if match:
                # This is a simplified parser. A real-world parser would be more complex.
                logs.append(match.groups())
    df = pd.DataFrame(logs, columns=['month', 'day', 'time', 'hostname', 'process', 'message'])
    # Combine date and time columns and convert to datetime objects (simplified)
    df['timestamp'] = pd.to_datetime(df['month'] + ' ' + df['day'] + ' ' + df['time'], format='%b %d %H:%M:%S')
    return df

# Load and parse logs
apache_logs = parse_apache_log('access.log') # Provide a sample access.log
syslog_logs = parse_syslog('syslog.log') # Provide a sample syslog.log

# Combine and sort logs by timestamp
all_logs = pd.concat([apache_logs, syslog_logs]).sort_values(by='timestamp')

print("Combined and sorted logs:")
print(all_logs.head())
```

**Step 2: Prepare Sample Log Files**

You will need to create sample `access.log` and `syslog.log` files for this lab. You can find examples of these log formats online.

### Part 2: Event Correlation and Timeline Generation

**Objective:** Correlate events and generate a chronological timeline of the attack.

**Step 1: Add Event Correlation Logic**

Add the following code to your script to correlate events based on IP addresses and timestamps.

```python
# Simple event correlation logic
def generate_timeline(logs_df):
    timeline = []
    for index, row in logs_df.iterrows():
        # Example correlation: look for a failed login followed by a successful one from the same IP
        if 'Failed password' in str(row['message']):
            ip_address = re.search(r'for"s+("S+)"s+from', str(row['message']))
            if ip_address:
                # Search for a subsequent successful login from the same IP
                pass # Add more complex correlation logic here
        timeline.append(f"{row['timestamp']}: {row['message'] if 'message' in row else row['ip'] + ' ' + row['status']}")
    return timeline

timeline = generate_timeline(all_logs)

print("\nAttack Timeline:")
for event in timeline[:10]:
    print(event)
```

### Part 3: Visualizing the Attack Path

**Objective:** Use a graph to visualize the relationships between different entities in the attack.

**Step 1: Add Graph Visualization Code**

```python
import networkx as nx
import matplotlib.pyplot as plt

def visualize_attack_path(logs_df):
    G = nx.Graph()
    for index, row in logs_df.iterrows():
        if 'ip' in row and 'user_agent' in row:
            G.add_node(row['ip'], type='ip')
            G.add_node(row['user_agent'], type='user_agent')
            G.add_edge(row['ip'], row['user_agent'])

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=8)
    plt.title("Attack Path Visualization")
    plt.show()

visualize_attack_path(apache_logs)
```

### Deliverables

1.  **Python Script:** Submit your complete `timeline_generator.py` script.
2.  **Sample Log Files:** Submit the `access.log` and `syslog.log` files you used.
3.  **Lab Report:** A 2-3 page report that includes:
    *   The generated attack timeline.
    *   The attack path visualization graph.
    *   An analysis of the attack scenario based on the timeline and graph.
    *   A discussion on the challenges and limitations of automated timeline generation.

### Grading Rubric

| Criterion | Points | Description |
| :--- | :--- | :--- |
| Log Parsing | 30 | Correctly parses and normalizes different log formats. |
| Timeline Generation | 40 | Implements effective event correlation and generates a coherent timeline. |
| Attack Visualization | 20 | Creates a clear and informative graph visualization of the attack path. |
| Lab Report | 10 | Well-written report with all required elements and insightful analysis. |
| **Total** | **100** | |
