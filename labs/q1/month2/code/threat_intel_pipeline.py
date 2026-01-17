#!/usr/bin/env python3
"""
Lab 2: Threat Intelligence Data Pipeline
Advanced AI in Cybersecurity and Digital Forensics Program

This script collects threat intelligence from public APIs and stores it in a database.

Author: Manus AI
Date: January 2026
"""

import requests
import sqlite3
import json
import argparse
from datetime import datetime
import time

class ThreatIntelPipeline:
    """Threat Intelligence Data Pipeline"""
    
    def __init__(self, db_path='threat_intel.db'):
        """
        Initialize the pipeline
        
        Args:
            db_path (str): Path to SQLite database
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        print("[*] Initializing database...")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create indicators table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator_type TEXT NOT NULL,
                indicator_value TEXT NOT NULL UNIQUE,
                description TEXT,
                threat_type TEXT,
                malware_family TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                confidence INTEGER,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create pulses table (for OTX pulses)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pulses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pulse_id TEXT UNIQUE,
                name TEXT,
                description TEXT,
                author TEXT,
                created TIMESTAMP,
                modified TIMESTAMP,
                tags TEXT,
                references TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("[+] Database initialized")
    
    def collect_from_otx(self, api_key=None, pulse_count=10):
        """
        Collect threat intelligence from AlienVault OTX
        
        Args:
            api_key (str): OTX API key (optional for public data)
            pulse_count (int): Number of pulses to fetch
        """
        print(f"[*] Collecting data from AlienVault OTX...")
        
        # Note: This is a simplified example. In production, use actual API key
        base_url = "https://otx.alienvault.com/api/v1"
        headers = {}
        if api_key:
            headers['X-OTX-API-KEY'] = api_key
        
        try:
            # Get subscribed pulses (public endpoint)
            url = f"{base_url}/pulses/subscribed"
            params = {'limit': pulse_count}
            
            print(f"[*] Fetching {pulse_count} pulses...")
            # Note: This is a mock example - actual API call would require authentication
            # For demonstration purposes, we'll create sample data
            
            sample_pulses = self._generate_sample_otx_data(pulse_count)
            
            for pulse in sample_pulses:
                self._store_pulse(pulse)
                
                # Extract and store indicators
                for indicator in pulse.get('indicators', []):
                    self._store_indicator(
                        indicator_type=indicator['type'],
                        indicator_value=indicator['indicator'],
                        description=pulse['name'],
                        threat_type=indicator.get('type', 'unknown'),
                        source='OTX'
                    )
            
            print(f"[+] Successfully collected {len(sample_pulses)} pulses")
            
        except Exception as e:
            print(f"[-] Error collecting from OTX: {e}")
    
    def _generate_sample_otx_data(self, count):
        """Generate sample OTX data for demonstration"""
        sample_pulses = []
        
        sample_indicators = [
            {'type': 'IPv4', 'indicator': '192.0.2.1'},
            {'type': 'IPv4', 'indicator': '198.51.100.1'},
            {'type': 'domain', 'indicator': 'malicious-domain.com'},
            {'type': 'domain', 'indicator': 'phishing-site.net'},
            {'type': 'FileHash-SHA256', 'indicator': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'},
            {'type': 'URL', 'indicator': 'http://malware-download.com/payload.exe'}
        ]
        
        for i in range(count):
            pulse = {
                'id': f'pulse_{i+1}',
                'name': f'Threat Campaign {i+1}',
                'description': f'This is a sample threat intelligence pulse #{i+1}',
                'author': 'Security Researcher',
                'created': datetime.now().isoformat(),
                'modified': datetime.now().isoformat(),
                'tags': ['malware', 'apt', 'phishing'],
                'references': ['https://example.com/analysis'],
                'indicators': sample_indicators[:2]  # Use subset of indicators
            }
            sample_pulses.append(pulse)
        
        return sample_pulses
    
    def _store_pulse(self, pulse):
        """Store pulse in database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO pulses 
                (pulse_id, name, description, author, created, modified, tags, references)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pulse['id'],
                pulse['name'],
                pulse['description'],
                pulse['author'],
                pulse['created'],
                pulse['modified'],
                json.dumps(pulse['tags']),
                json.dumps(pulse['references'])
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # Pulse already exists
    
    def _store_indicator(self, indicator_type, indicator_value, description=None, 
                        threat_type=None, malware_family=None, source=None, confidence=50):
        """Store indicator in database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO indicators 
                (indicator_type, indicator_value, description, threat_type, 
                 malware_family, first_seen, last_seen, confidence, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                indicator_type,
                indicator_value,
                description,
                threat_type,
                malware_family,
                datetime.now(),
                datetime.now(),
                confidence,
                source
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Update last_seen if indicator exists
            self.cursor.execute('''
                UPDATE indicators 
                SET last_seen = ?, description = COALESCE(?, description)
                WHERE indicator_value = ?
            ''', (datetime.now(), description, indicator_value))
            self.conn.commit()
    
    def query_indicators(self, indicator_type=None, limit=100):
        """
        Query indicators from database
        
        Args:
            indicator_type (str): Filter by indicator type
            limit (int): Maximum number of results
        
        Returns:
            list: List of indicators
        """
        if indicator_type:
            self.cursor.execute('''
                SELECT * FROM indicators 
                WHERE indicator_type = ? 
                ORDER BY last_seen DESC 
                LIMIT ?
            ''', (indicator_type, limit))
        else:
            self.cursor.execute('''
                SELECT * FROM indicators 
                ORDER BY last_seen DESC 
                LIMIT ?
            ''', (limit,))
        
        columns = [desc[0] for desc in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    def search_indicator(self, indicator_value):
        """
        Search for a specific indicator
        
        Args:
            indicator_value (str): Indicator to search for
        
        Returns:
            dict: Indicator details or None
        """
        self.cursor.execute('''
            SELECT * FROM indicators WHERE indicator_value = ?
        ''', (indicator_value,))
        
        row = self.cursor.fetchone()
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        return None
    
    def get_statistics(self):
        """Get statistics about the threat intelligence database"""
        stats = {}
        
        # Total indicators
        self.cursor.execute('SELECT COUNT(*) FROM indicators')
        stats['total_indicators'] = self.cursor.fetchone()[0]
        
        # Indicators by type
        self.cursor.execute('''
            SELECT indicator_type, COUNT(*) as count 
            FROM indicators 
            GROUP BY indicator_type
        ''')
        stats['by_type'] = dict(self.cursor.fetchall())
        
        # Total pulses
        self.cursor.execute('SELECT COUNT(*) FROM pulses')
        stats['total_pulses'] = self.cursor.fetchone()[0]
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Threat Intelligence Pipeline - Lab 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect threat intelligence from OTX
  python threat_intel_pipeline.py --collect --source otx --count 20
  
  # Query all indicators
  python threat_intel_pipeline.py --query
  
  # Query specific indicator type
  python threat_intel_pipeline.py --query --type IPv4
  
  # Search for specific indicator
  python threat_intel_pipeline.py --search 192.0.2.1
  
  # Get statistics
  python threat_intel_pipeline.py --stats
        """
    )
    
    parser.add_argument('--db', default='threat_intel.db', 
                       help='Database path (default: threat_intel.db)')
    parser.add_argument('--collect', action='store_true', 
                       help='Collect threat intelligence')
    parser.add_argument('--source', choices=['otx'], default='otx',
                       help='Threat intelligence source')
    parser.add_argument('--count', type=int, default=10,
                       help='Number of items to collect')
    parser.add_argument('--query', action='store_true',
                       help='Query indicators')
    parser.add_argument('--type', help='Filter by indicator type')
    parser.add_argument('--search', metavar='INDICATOR',
                       help='Search for specific indicator')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics')
    parser.add_argument('--api-key', help='API key for threat intelligence source')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = ThreatIntelPipeline(args.db)
    
    try:
        if args.collect:
            if args.source == 'otx':
                pipeline.collect_from_otx(args.api_key, args.count)
        
        elif args.query:
            indicators = pipeline.query_indicators(args.type, limit=50)
            print(f"\n[+] Found {len(indicators)} indicators")
            print("\nIndicator Type\tIndicator Value\t\t\tThreat Type\tSource")
            print("-" * 80)
            for ind in indicators:
                print(f"{ind['indicator_type']}\t\t{ind['indicator_value'][:30]}\t{ind['threat_type']}\t{ind['source']}")
        
        elif args.search:
            result = pipeline.search_indicator(args.search)
            if result:
                print("\n[+] Indicator found:")
                for key, value in result.items():
                    print(f"  {key}: {value}")
            else:
                print(f"\n[-] Indicator not found: {args.search}")
        
        elif args.stats:
            stats = pipeline.get_statistics()
            print("\n" + "=" * 60)
            print("THREAT INTELLIGENCE DATABASE STATISTICS")
            print("=" * 60)
            print(f"\nTotal Indicators: {stats['total_indicators']}")
            print(f"Total Pulses: {stats['total_pulses']}")
            print("\nIndicators by Type:")
            for itype, count in stats['by_type'].items():
                print(f"  {itype}: {count}")
        
        else:
            parser.print_help()
    
    finally:
        pipeline.close()

if __name__ == "__main__":
    main()
