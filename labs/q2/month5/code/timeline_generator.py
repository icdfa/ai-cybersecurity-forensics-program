#!/usr/bin/env python3
"""
Lab 5: Automated Attack Timeline Generation
Uses AI to automatically generate attack timelines from logs
"""

import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import json

class TimelineGenerator:
    def __init__(self):
        self.events = []
    
    def load_logs(self, log_file):
        """Load network logs"""
        print(f"[*] Loading logs from: {log_file}")
        df = pd.read_csv(log_file)
        print(f"[+] Loaded {len(df)} log entries")
        return df
    
    def detect_anomalies(self, df):
        """Detect anomalous events"""
        print("[*] Detecting anomalies...")
        
        # Simple anomaly detection based on denied connections
        anomalies = df[df['action'] == 'DENY']
        
        print(f"[+] Found {len(anomalies)} anomalous events")
        return anomalies
    
    def generate_timeline(self, events, output_file='timeline.json'):
        """Generate attack timeline"""
        timeline = []
        
        for idx, event in events.iterrows():
            timeline_event = {
                'timestamp': event['timestamp'],
                'src_ip': event['src_ip'],
                'dst_ip': event['dst_ip'],
                'dst_port': event['dst_port'],
                'action': event['action'],
                'severity': 'high' if event['action'] == 'DENY' else 'low'
            }
            timeline.append(timeline_event)
        
        with open(output_file, 'w') as f:
            json.dump(timeline, f, indent=2)
        
        print(f"[+] Timeline saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Timeline Generator - Lab 5")
    parser.add_argument('log_file', help='Path to network log file')
    parser.add_argument('--output', default='timeline.json', help='Output timeline file')
    
    args = parser.parse_args()
    
    generator = TimelineGenerator()
    df = generator.load_logs(args.log_file)
    anomalies = generator.detect_anomalies(df)
    generator.generate_timeline(anomalies, args.output)

if __name__ == "__main__":
    main()
