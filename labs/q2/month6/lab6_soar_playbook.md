# Lab 6: Developing a SOAR Playbook for Automated Response

## Quarter 2, Month 6, Weeks 23-24

### Objective

This lab will guide you through the process of designing and implementing a simple Security Orchestration, Automation, and Response (SOAR) playbook. You will automate the response to a simulated phishing email report, integrating external tools for analysis and taking automated remediation actions.

### Learning Outcomes

Upon completion of this lab, you will be able to:

-   Design a workflow for an automated incident response playbook.
-   Integrate external security tools and APIs into a playbook.
-   Extract and analyze observables from security alerts.
-   Develop a Python script to simulate the execution of a SOAR playbook.

### Prerequisites

-   Completion of previous labs in the program.
-   A strong understanding of Python, APIs, and JSON.
-   Familiarity with the basics of incident response.

### Required Tools and Libraries

```bash
pip install requests
```

### Part 1: Designing the Phishing Response Playbook

**Objective:** Design a clear, step-by-step workflow for handling a phishing email report.

**Workflow Steps:**

1.  **Ingest Alert:** Receive a phishing email report, including the email's sender, subject, and body.
2.  **Extract Observables:** Parse the email to extract key observables, such as URLs, IP addresses, and file hashes.
3.  **Enrich Observables:** Use external threat intelligence services to analyze the extracted observables.
    *   Scan any URLs using a service like URLScan.io.
    *   Check IP addresses against blacklists.
4.  **Make a Decision:** Based on the enrichment data, determine if the email is malicious.
5.  **Take Action:** If the email is malicious, perform automated remediation actions:
    *   Block the sender's email address (simulated).
    *   Block the malicious URL at the firewall (simulated).
    *   Create a ticket in a ticketing system (simulated).
6.  **Generate Report:** Create a summary report of the incident, analysis, and actions taken.

### Part 2: Implementing the Playbook in Python

**Objective:** Write a Python script to implement the designed playbook.

**Step 1: Set up the Python Script**

Create a file named `soar_playbook.py`.

```python
import requests
import json

# --- Configuration ---
URLSCAN_API_KEY = "YOUR_URLSCAN_API_KEY" # Get a free API key from https://urlscan.io/

# --- Simulated Phishing Email ---
simulated_phishing_email = {
    "sender": "attacker@evil.com",
    "subject": "Urgent: Your account has been compromised!",
    "body": "Please click this link to reset your password: http://malicious-link.com/reset-password"
}

# --- Playbook Functions ---

def extract_observables(email):
    # A simple URL extractor. A real-world scenario would be more robust.
    url_pattern = re.compile(r'https?://[^"]+')
    urls = url_pattern.findall(email["body"])
    return {"urls": urls}

def analyze_url_with_urlscan(url):
    if not URLSCAN_API_KEY:
        print("URLScan.io API key not configured. Skipping analysis.")
        return None

    headers = {"API-Key": URLSCAN_API_KEY, "Content-Type": "application/json"}
    data = {"url": url, "visibility": "public"}
    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print(f"Successfully submitted {url} to URLScan.io.")
        # In a real playbook, you would poll the result URL.
        return response.json()
    else:
        print(f"Error submitting {url} to URLScan.io: {response.text}")
        return None

def make_decision(analysis_results):
    # Simple decision logic. In a real scenario, this would be more complex.
    if analysis_results and analysis_results.get("message") == "Submission successful":
        return "malicious"
    return "benign"

def take_action(decision, observables):
    if decision == "malicious":
        print("\n--- Taking Remediation Actions ---")
        for url in observables["urls"]:
            print(f"[ACTION] Blocking URL at firewall: {url}")
        print(f"[ACTION] Blocking sender: {simulated_phishing_email['sender']}")
        print("[ACTION] Creating a high-priority ticket in Jira.")
    else:
        print("\n--- No Malicious Activity Detected ---")

# --- Main Playbook Execution ---
if __name__ == "__main__":
    print("--- Starting Phishing Response Playbook ---")
    observables = extract_observables(simulated_phishing_email)
    print(f"Extracted observables: {observables}")

    if observables["urls"]:
        analysis_result = analyze_url_with_urlscan(observables["urls"][0])
        decision = make_decision(analysis_result)
        print(f"Decision: The email is {decision}.")
        take_action(decision, observables)
    else:
        print("No URLs found in the email.")
```

**Step 2: Get a URLScan.io API Key**

1.  Go to [https://urlscan.io/](https://urlscan.io/) and create a free account.
2.  Go to your profile settings to find your API key.
3.  Replace `"YOUR_URLSCAN_API_KEY"` in the script with your actual key.

### Part 3: Testing the Playbook

**Objective:** Test the playbook with a sample phishing email and verify the automated actions.

**Step 1: Run the Playbook**

Execute the script from your terminal:

```bash
python3 soar_playbook.py
```

**Expected Output:**

The script should:
1.  Extract the URL from the simulated email.
2.  Submit the URL to URLScan.io for analysis.
3.  Make a decision based on the analysis result.
4.  Simulate taking remediation actions if the URL is deemed malicious.

**Step 2: Modify the Email**

Change the `simulated_phishing_email` dictionary in the script to test different scenarios (e.g., an email with no URL, an email with a benign URL like `http://google.com`).

### Deliverables

1.  **Python Script:** Submit your complete `soar_playbook.py` script.
2.  **Lab Report:** A 2-3 page report that includes:
    *   A detailed diagram of your phishing response playbook workflow.
    *   Screenshots of the script's output for both malicious and benign scenarios.
    *   A discussion on how this playbook could be expanded with more integrations and more complex logic.
    *   An analysis of the benefits and challenges of using SOAR in a security operations center (SOC).

### Grading Rubric

| Criterion | Points | Description |
| :--- | :--- | :--- |
| Playbook Design | 20 | A clear and logical workflow diagram for the playbook. |
| Observable Extraction | 20 | Correctly extracts observables from the simulated email. |
| API Integration | 30 | Successfully integrates with the URLScan.io API for enrichment. |
| Decision Logic & Actions | 20 | Implements decision-making and simulates appropriate remediation actions. |
| Lab Report | 10 | A well-written report with all required elements and insightful analysis. |
| **Total** | **100** | |
