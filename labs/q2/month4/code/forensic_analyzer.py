#!/usr/bin/env python3
"""
Lab 4: Forensic Analysis of a Compromised System
Advanced AI in Cybersecurity and Digital Forensics Program

This script performs automated forensic analysis on system artifacts.

Author: Manus AI
Date: January 2026
"""

import os
import hashlib
import json
from datetime import datetime
import argparse

class ForensicAnalyzer:
    """Automated Forensic Analysis Tool"""
    
    def __init__(self, evidence_path):
        """Initialize forensic analyzer"""
        self.evidence_path = evidence_path
        self.findings = []
    
    def calculate_hash(self, file_path):
        """Calculate file hashes"""
        hashes = {}
        
        with open(file_path, 'rb') as f:
            data = f.read()
            hashes['md5'] = hashlib.md5(data).hexdigest()
            hashes['sha1'] = hashlib.sha1(data).hexdigest()
            hashes['sha256'] = hashlib.sha256(data).hexdigest()
        
        return hashes
    
    def analyze_file_system(self):
        """Analyze file system artifacts"""
        print("[*] Analyzing file system...")
        
        suspicious_extensions = ['.exe', '.dll', '.bat', '.ps1', '.vbs']
        suspicious_files = []
        
        for root, dirs, files in os.walk(self.evidence_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in suspicious_extensions:
                    file_info = {
                        'path': file_path,
                        'name': file,
                        'size': os.path.getsize(file_path),
                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                        'hashes': self.calculate_hash(file_path)
                    }
                    suspicious_files.append(file_info)
        
        self.findings.append({
            'category': 'file_system',
            'suspicious_files': suspicious_files
        })
        
        print(f"[+] Found {len(suspicious_files)} suspicious files")
        return suspicious_files
    
    def generate_report(self, output_path='forensic_report.json'):
        """Generate forensic analysis report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'evidence_path': self.evidence_path,
            'findings': self.findings
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[+] Report saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Forensic Analyzer - Lab 4")
    parser.add_argument('evidence_path', help='Path to evidence directory')
    parser.add_argument('--output', default='forensic_report.json', help='Output report path')
    
    args = parser.parse_args()
    
    analyzer = ForensicAnalyzer(args.evidence_path)
    analyzer.analyze_file_system()
    analyzer.generate_report(args.output)

if __name__ == "__main__":
    main()
