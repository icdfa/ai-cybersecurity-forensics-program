#!/usr/bin/env python3
"""
Generate Sample Datasets for All Labs
Advanced AI in Cybersecurity and Digital Forensics Program
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random

def generate_malware_dataset(output_path, n_samples=1000):
    """Generate sample malware dataset for Lab 3"""
    print(f"[*] Generating malware dataset ({n_samples} samples)...")
    
    np.random.seed(42)
    
    # Generate features
    data = {
        'file_size': np.random.randint(1000, 10000000, n_samples),
        'entropy': np.random.uniform(0, 8, n_samples),
        'num_sections': np.random.randint(1, 10, n_samples),
        'num_imports': np.random.randint(0, 500, n_samples),
        'num_exports': np.random.randint(0, 100, n_samples),
        'has_debug_info': np.random.choice([0, 1], n_samples),
        'has_signature': np.random.choice([0, 1], n_samples),
        'suspicious_api_calls': np.random.randint(0, 50, n_samples),
        'string_entropy': np.random.uniform(0, 8, n_samples),
        'packed': np.random.choice([0, 1], n_samples),
    }
    
    # Generate labels (50% malware, 50% benign)
    labels = np.random.choice([0, 1], n_samples)
    
    # Adjust features based on labels to make patterns
    for i in range(n_samples):
        if labels[i] == 1:  # Malware
            data['entropy'][i] += np.random.uniform(0, 2)
            data['suspicious_api_calls'][i] += np.random.randint(10, 30)
            data['packed'][i] = 1 if np.random.random() > 0.3 else 0
        else:  # Benign
            data['has_signature'][i] = 1 if np.random.random() > 0.2 else 0
            data['suspicious_api_calls'][i] = max(0, data['suspicious_api_calls'][i] - 20)
    
    df = pd.DataFrame(data)
    df['label'] = labels
    
    df.to_csv(output_path, index=False)
    print(f"[+] Malware dataset saved to: {output_path}")

def generate_network_logs(output_path, n_entries=500):
    """Generate sample network logs for Lab 5"""
    print(f"[*] Generating network logs ({n_entries} entries)...")
    
    start_time = datetime.now() - timedelta(hours=24)
    
    logs = []
    for i in range(n_entries):
        timestamp = start_time + timedelta(seconds=i*10)
        
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'src_ip': f"192.168.1.{random.randint(1, 254)}",
            'dst_ip': f"10.0.0.{random.randint(1, 254)}",
            'src_port': random.randint(1024, 65535),
            'dst_port': random.choice([80, 443, 22, 21, 3389]),
            'protocol': random.choice(['TCP', 'UDP', 'ICMP']),
            'bytes': random.randint(100, 10000),
            'action': random.choice(['ALLOW', 'DENY', 'ALLOW', 'ALLOW'])
        }
        logs.append(log_entry)
    
    df = pd.DataFrame(logs)
    df.to_csv(output_path, index=False)
    print(f"[+] Network logs saved to: {output_path}")

def generate_threat_indicators(output_path, n_indicators=200):
    """Generate sample threat indicators for Lab 2"""
    print(f"[*] Generating threat indicators ({n_indicators} indicators)...")
    
    indicators = []
    
    for i in range(n_indicators):
        indicator_type = random.choice(['IPv4', 'domain', 'FileHash-SHA256', 'URL'])
        
        if indicator_type == 'IPv4':
            value = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        elif indicator_type == 'domain':
            value = f"malicious-domain-{i}.com"
        elif indicator_type == 'FileHash-SHA256':
            value = ''.join(random.choices('0123456789abcdef', k=64))
        else:  # URL
            value = f"http://malicious-site-{i}.com/payload.exe"
        
        indicator = {
            'type': indicator_type,
            'value': value,
            'threat_type': random.choice(['malware', 'phishing', 'c2', 'exploit']),
            'confidence': random.randint(50, 100),
            'first_seen': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
        }
        indicators.append(indicator)
    
    with open(output_path, 'w') as f:
        json.dump(indicators, f, indent=2)
    
    print(f"[+] Threat indicators saved to: {output_path}")

def main():
    """Generate all sample datasets"""
    print("=" * 60)
    print("Sample Data Generator")
    print("Advanced AI in Cybersecurity and Digital Forensics")
    print("=" * 60)
    print()
    
    # Create data directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Lab 2 data
    lab2_data_dir = os.path.join(base_dir, 'labs/q1/month2/data')
    os.makedirs(lab2_data_dir, exist_ok=True)
    generate_threat_indicators(os.path.join(lab2_data_dir, 'sample_indicators.json'))
    
    # Lab 3 data
    lab3_data_dir = os.path.join(base_dir, 'labs/q1/month3/data')
    os.makedirs(lab3_data_dir, exist_ok=True)
    generate_malware_dataset(os.path.join(lab3_data_dir, 'malware_dataset.csv'), n_samples=2000)
    
    # Lab 5 data
    lab5_data_dir = os.path.join(base_dir, 'labs/q2/month5/data')
    os.makedirs(lab5_data_dir, exist_ok=True)
    generate_network_logs(os.path.join(lab5_data_dir, 'network_logs.csv'), n_entries=1000)
    
    print()
    print("[+] All sample datasets generated successfully!")

if __name__ == "__main__":
    main()
