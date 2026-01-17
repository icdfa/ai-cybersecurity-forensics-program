#!/usr/bin/env python3
"""
Lab 6: Developing a SOAR Playbook for Automated Response
This script simulates a SOAR playbook for automated incident response.

Author: Manus AI
Date: January 2026
"""

import json
import argparse
from datetime import datetime

class SOARPlaybook:
    """Simulates a SOAR playbook for automated incident response."""

    def __init__(self, playbook_file):
        """Initialize the SOAR playbook."""
        self.playbook = self.load_playbook(playbook_file)
        self.incident_data = None

    def load_playbook(self, playbook_file):
        """Load a playbook from a JSON file."""
        print(f"[*] Loading playbook from: {playbook_file}")
        with open(playbook_file, 'r') as f:
            playbook = json.load(f)
        print("[+] Playbook loaded successfully.")
        return playbook

    def run_playbook(self, incident_file):
        """Run the playbook for a given incident."""
        print(f"[*] Running playbook for incident: {incident_file}")
        self.load_incident(incident_file)

        for step in self.playbook['steps']:
            self.execute_step(step)

        print("[+] Playbook execution complete.")

    def load_incident(self, incident_file):
        """Load incident data from a JSON file."""
        with open(incident_file, 'r') as f:
            self.incident_data = json.load(f)
        print("[+] Incident data loaded.")

    def execute_step(self, step):
        """Execute a single step in the playbook."""
        print(f"\n--- Executing Step: {step['name']} ---")
        action = step['action']
        params = step.get('params', {})

        if action == 'enrich_indicator':
            self.enrich_indicator(params['indicator_type'])
        elif action == 'block_ip':
            self.block_ip(self.incident_data['source_ip'])
        elif action == 'isolate_host':
            self.isolate_host(self.incident_data['hostname'])
        elif action == 'send_notification':
            self.send_notification(params['recipient'])
        else:
            print(f"[!] Unknown action: {action}")

    def enrich_indicator(self, indicator_type):
        """Simulate indicator enrichment."""
        indicator = self.incident_data.get(indicator_type)
        if indicator:
            print(f"[*] Enriching {indicator_type}: {indicator}")
            # In a real scenario, this would query threat intel platforms
            print(f"[+] Enrichment complete. Reputation: High Risk")
        else:
            print(f"[!] Indicator not found in incident data: {indicator_type}")

    def block_ip(self, ip_address):
        """Simulate blocking an IP address on a firewall."""
        print(f"[*] Blocking IP address on firewall: {ip_address}")
        # In a real scenario, this would interact with a firewall API
        print(f"[+] IP address {ip_address} blocked successfully.")

    def isolate_host(self, hostname):
        """Simulate isolating a host from the network."""
        print(f"[*] Isolating host from the network: {hostname}")
        # In a real scenario, this would interact with an EDR or NAC solution
        print(f"[+] Host {hostname} isolated successfully.")

    def send_notification(self, recipient):
        """Simulate sending a notification to the security team."""
        print(f"[*] Sending notification to: {recipient}")
        # In a real scenario, this would use email or a messaging API
        print(f"[+] Notification sent successfully.")

def main():
    parser = argparse.ArgumentParser(description="SOAR Playbook Simulator - Lab 6")
    parser.add_argument('playbook', help='Path to the playbook JSON file')
    parser.add_argument('incident', help='Path to the incident JSON file')
    args = parser.parse_args()

    soar = SOARPlaybook(args.playbook)
    soar.run_playbook(args.incident)

if __name__ == "__main__":
    # Create a sample playbook and incident for testing
    sample_playbook = {
        "name": "Phishing Incident Response",
        "steps": [
            {
                "name": "Enrich URL Indicator",
                "action": "enrich_indicator",
                "params": {"indicator_type": "url"}
            },
            {
                "name": "Block Malicious IP",
                "action": "block_ip"
            },
            {
                "name": "Isolate Affected Host",
                "action": "isolate_host"
            },
            {
                "name": "Notify Security Team",
                "action": "send_notification",
                "params": {"recipient": "soc@icdfa.org"}
            }
        ]
    }
    with open("sample_playbook.json", "w") as f:
        json.dump(sample_playbook, f, indent=2)

    sample_incident = {
        "incident_id": "INC-12345",
        "source_ip": "198.51.100.23",
        "hostname": "workstation-042",
        "url": "http://malicious-site.example.com/phish"
    }
    with open("sample_incident.json", "w") as f:
        json.dump(sample_incident, f, indent=2)

    print("Sample playbook and incident files created.")
    print("Run with: python3 soar_playbook.py sample_playbook.json sample_incident.json")

