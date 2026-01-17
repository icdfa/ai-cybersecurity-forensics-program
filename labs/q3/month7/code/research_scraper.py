#!/usr/bin/env python3
"""
Lab 7: Research on Recent Adversarial Attacks
This script uses the arXiv API to search for and download research papers.

Author: Manus AI
Date: January 2026
"""

import arxiv
import argparse
import os

def search_arxiv(query, max_results=10):
    """Search arXiv for papers matching the query."""
    print(f"[*] Searching arXiv for: '{query}'")
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    results = []
    for result in search.results():
        results.append(result)
    
    print(f"[+] Found {len(results)} results.")
    return results

def download_papers(papers, download_dir='papers'):
    """Download papers to a specified directory."""
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    print(f"[*] Downloading {len(papers)} papers to '{download_dir}'...")
    
    for paper in papers:
        try:
            paper.download_pdf(dirpath=download_dir, filename=f"{paper.entry_id.split('/')[-1]}.pdf")
            print(f"  - Downloaded: {paper.title}")
        except Exception as e:
            print(f"  - [!] Failed to download {paper.title}: {e}")
            
    print("[+] Download complete.")

def main():
    parser = argparse.ArgumentParser(description="arXiv Research Scraper - Lab 7")
    parser.add_argument("query", help="Search query for arXiv (e.g., 'adversarial attacks on large language models')")
    parser.add_argument("--max-results", type=int, default=5, help="Maximum number of papers to download")
    parser.add_argument("--download-dir", default="research_papers", help="Directory to save downloaded papers")
    
    args = parser.parse_args()
    
    papers = search_arxiv(args.query, args.max_results)
    
    if papers:
        download_papers(papers, args.download_dir)

if __name__ == "__main__":
    # Add arxiv to requirements
    with open("../../../../requirements.txt", "a") as f:
        f.write("\narxiv>=1.4.2\n")
    print("Added arxiv to requirements.txt")
    main()
