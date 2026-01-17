# Lab 2: Developing a Threat Intelligence Data Pipeline

## Quarter 1, Month 2, Weeks 5-6

### Objective

In this lab, you will build a data pipeline to collect, process, and store threat intelligence data from various sources. You will use Python to fetch data from public APIs, parse and normalize the data, and store it in a structured format. This lab provides practical experience in building automated systems for threat intelligence gathering.

### Learning Outcomes

Upon completion of this lab, you will be able to:

-   Collect threat intelligence data from public APIs.
-   Parse and normalize data from different sources into a unified format.
-   Store structured data in a local database (SQLite).
-   Build a simple data pipeline for continuous threat intelligence gathering.

### Prerequisites

-   Completion of Lab 1: Automating Network Scanning and Packet Analysis.
-   Strong understanding of Python programming and data structures.
-   Familiarity with REST APIs and JSON data format.

### Required Tools and Libraries

```bash
pip install requests pandas
```

### Part 1: Collecting Data from Threat Intelligence Feeds

**Objective:** Collect Indicators of Compromise (IOCs) from public threat intelligence feeds.

**Step 1: Set up the Python Script**

Create a file named `threat_intel_pipeline.py` and add the following code to fetch data from the AlienVault OTX API.

```python
import requests
import pandas as pd
import sqlite3

# Function to fetch data from AlienVault OTX
def fetch_otx_iocs():
    print("Fetching IOCs from AlienVault OTX...")
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        iocs = []
        for pulse in data["results"]:
            for indicator in pulse["indicators"]:
                iocs.append({
                    "indicator": indicator["indicator"],
                    "type": indicator["type"],
                    "source": "AlienVault OTX",
                    "pulse_name": pulse["name"]
                })
        return iocs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OTX: {e}")
        return []

# Fetch and display a few IOCs
iocs = fetch_otx_iocs()
if iocs:
    print(f"Successfully fetched {len(iocs)} IOCs.")
    print("Sample IOCs:")
    for ioc in iocs[:5]:
        print(ioc)
```

**Step 2: Run the Script**

Execute the script from your terminal:

```bash
python3 threat_intel_pipeline.py
```

**Expected Output:** A list of IOCs fetched from AlienVault OTX, including the indicator, type, and source.

### Part 2: Data Normalization and Storage

**Objective:** Normalize the collected data and store it in a local SQLite database.

**Step 1: Add Data Normalization and Storage Functions**

Add the following functions to your `threat_intel_pipeline.py` script:

```python
# Function to create a database and table
def create_database():
    conn = sqlite3.connect("threat_intelligence.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS iocs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        indicator TEXT NOT NULL,
        type TEXT NOT NULL,
        source TEXT NOT NULL,
        pulse_name TEXT,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# Function to store IOCs in the database
def store_iocs(iocs):
    conn = sqlite3.connect("threat_intelligence.db")
    df = pd.DataFrame(iocs)
    df.to_sql("iocs", conn, if_exists="append", index=False)
    conn.close()
    print(f"Stored {len(iocs)} IOCs in the database.")

# Main execution flow
if __name__ == "__main__":
    create_database()
    iocs = fetch_otx_iocs()
    if iocs:
        store_iocs(iocs)
```

**Step 2: Run the Full Pipeline**

Execute the script again to run the full pipeline:

```bash
python3 threat_intel_pipeline.py
```

**Expected Output:** The script will fetch the IOCs and store them in a new `threat_intelligence.db` file.

### Part 3: Querying and Analyzing the Data

**Objective:** Query the database to retrieve and analyze the stored threat intelligence data.

**Step 1: Add a Query Function**

Add the following function to your script to query the database:

```python
# Function to query IOCs from the database
def query_iocs(indicator_type=None):
    conn = sqlite3.connect("threat_intelligence.db")
    query = "SELECT * FROM iocs"
    if indicator_type:
        query += f" WHERE type = ‘{indicator_type}’"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# In the main execution block, add a query example
if __name__ == "__main__":
    create_database()
    iocs = fetch_otx_iocs()
    if iocs:
        store_iocs(iocs)
    
    print("\nQuerying for IPv4 IOCs:")
    ipv4_iocs = query_iocs(indicator_type="IPv4")
    print(ipv4_iocs.head())
```

**Step 2: Run the Script with the Query**

Execute the script one more time:

```bash
python3 threat_intel_pipeline.py
```

**Expected Output:** The script will print the first few IPv4 IOCs found in the database.

### Deliverables

1.  **Python Script:** Submit your complete `threat_intel_pipeline.py` script.
2.  **Database File:** Submit the `threat_intelligence.db` file created by your script.
3.  **Lab Report:** A 1-2 page report that includes:
    *   A description of the data pipeline you built.
    *   An explanation of the data normalization process.
    *   An analysis of the types of IOCs collected and their potential use in a security operations center (SOC).

### Grading Rubric

| Criterion | Points | Description |
| :--- | :--- | :--- |
| Data Collection | 30 | Correctly fetches data from the OTX API. |
| Data Storage | 40 | Correctly normalizes and stores data in the SQLite database. |
| Data Querying | 20 | Correctly queries and retrieves data from the database. |
| Lab Report | 10 | Clear, concise, and well-documented report with all required elements. |
| **Total** | **100** | |
