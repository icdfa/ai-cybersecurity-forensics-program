# Datasets Guide

This document provides detailed information about all datasets used in the program, including download links, descriptions, and lab mappings.

## Quick Links

- [Malware Datasets](#malware-datasets)
- [Network Traffic Datasets](#network-traffic-datasets)
- [Digital Forensics Datasets](#digital-forensics-datasets)
- [Deepfake and Multimedia Datasets](#deepfake-and-multimedia-datasets)
- [Lab-Specific Dataset Mapping](#lab-specific-dataset-mapping)

---

## Malware Datasets

### EMBER - Elastic Malware Benchmark for Evaluation and Research

**Description:** EMBER is a labeled benchmark malware dataset containing 1.1 million PE files with extracted features and labels.

**Size:** ~2.2 GB (features only), ~500 GB (full dataset with raw files)

**Download:** https://github.com/elastic/ember

**Format:** JSON, CSV

**Used in Labs:**
- Lab 3: Building an Intelligent Malware Detection System

**Features:**
- 2,381 features extracted from PE files
- Binary classification (malware vs. benign)
- Training set: 900,000 samples
- Test set: 200,000 samples

**How to Download:**
```bash
# Install ember package
pip install ember

# Download dataset (features only)
python -c "import ember; ember.create_vectorized_features('ember_dataset')"
```

---

### Sorel-20M - Sophos-ReversingLabs Malware Dataset

**Description:** Large-scale malware dataset with 20 million samples and rich metadata.

**Size:** ~10 TB (full dataset), ~100 GB (metadata only)

**Download:** https://github.com/sophos-ai/Sorel-20M

**Format:** JSON, Parquet

**Used in Labs:**
- Lab 3: Building an Intelligent Malware Detection System (Advanced)

**Features:**
- File hashes (SHA256)
- Malware family labels
- Detection metadata
- Static analysis features

**How to Download:**
```bash
# Download metadata
wget https://sorel-20m.s3.amazonaws.com/09-DEC-2020/processed-data/lightgbm-features.tar.bz2

# Extract
tar -xjf lightgbm-features.tar.bz2
```

---

### VirusTotal Dataset

**Description:** Real-world malware samples and analysis reports from VirusTotal.

**Access:** Requires VirusTotal API key (free tier available)

**Download:** https://www.virustotal.com/gui/intelligence-overview

**Format:** JSON (API responses)

**Used in Labs:**
- Lab 2: Developing a Threat Intelligence Data Pipeline

**How to Access:**
```python
import requests

api_key = "YOUR_API_KEY"
url = "https://www.virustotal.com/api/v3/files/{file_hash}"
headers = {"x-apikey": api_key}

response = requests.get(url, headers=headers)
```

---

## Network Traffic Datasets

### CTU-13 - Botnet Traffic Dataset

**Description:** Real botnet traffic captured in a controlled environment with labeled normal and botnet traffic.

**Size:** ~32 GB

**Download:** https://www.stratosphereips.org/datasets-ctu-13

**Format:** PCAP, NetFlow

**Used in Labs:**
- Lab 1: Automating Network Scanning and Packet Analysis
- Lab 5: Automated Attack Timeline Generation

**Scenarios:** 13 different botnet scenarios including Neris, Rbot, Virut, and more.

**How to Download:**
```bash
# Download specific scenario
wget https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-42/detailed-bidirectional-flow-labels/capture20110810.binetflow
```

---

### CIC-IDS-2017 - Intrusion Detection Dataset

**Description:** Comprehensive dataset for network intrusion detection with labeled attack traffic.

**Size:** ~7 GB

**Download:** https://www.unb.ca/cic/datasets/ids-2017.html

**Format:** PCAP, CSV

**Used in Labs:**
- Lab 1: Automating Network Scanning and Packet Analysis
- Lab 5: Automated Attack Timeline Generation

**Attack Types:**
- Brute Force
- DoS/DDoS
- Web attacks
- Infiltration
- Botnet

**How to Download:**
```bash
# Download from official source
wget https://www.unb.ca/cic/datasets/ids-2017.html
# Follow download instructions on the page
```

---

### CICIDS2018 - Updated Intrusion Detection Dataset

**Description:** Updated version with more attack scenarios and better labeling.

**Size:** ~6.3 GB

**Download:** https://www.unb.ca/cic/datasets/ids-2018.html

**Format:** CSV

**Used in Labs:**
- Lab 5: Automated Attack Timeline Generation

---

## Digital Forensics Datasets

### Digital Corpora

**Description:** Comprehensive collection of digital forensic artifacts including disk images, memory dumps, and file systems.

**Size:** Varies by artifact (100 MB - 50 GB)

**Download:** https://digitalcorpora.org/

**Format:** Raw disk images, memory dumps, individual files

**Used in Labs:**
- Lab 4: Forensic Analysis of a Compromised System

**Collections:**
- Disk images (Windows, Linux, Mac)
- Memory dumps
- Network packet captures
- Mobile device images

**How to Download:**
```bash
# Example: Download a disk image
wget https://digitalcorpora.s3.amazonaws.com/corpora/disk-images/nps-2009-canon2/nps-2009-canon2-gen6.E01
```

---

### GovDocs - Government Documents Dataset

**Description:** Large collection of documents for file carving and recovery exercises.

**Size:** ~30 GB (1 million files)

**Download:** https://digitalcorpora.org/corpora/govdocs

**Format:** Various (PDF, DOC, XLS, etc.)

**Used in Labs:**
- Lab 4: Forensic Analysis of a Compromised System

---

### CFReDS - Computer Forensics Reference Data Sets

**Description:** Reference datasets for testing forensic tools and techniques.

**Download:** https://www.cfreds.nist.gov/

**Format:** Disk images, file systems

**Used in Labs:**
- Lab 4: Forensic Analysis of a Compromised System

---

## Deepfake and Multimedia Datasets

### Deepfake Detection Challenge (DFDC)

**Description:** Large-scale dataset of deepfake videos from Facebook/Meta.

**Size:** ~470 GB

**Download:** https://www.kaggle.com/c/deepfake-detection-challenge/data

**Format:** MP4 videos, JSON metadata

**Used in Labs:**
- Lab 10: Building and Detecting Deepfake Videos

**Content:**
- 100,000+ videos
- Real and fake videos
- Multiple manipulation techniques

**How to Download:**
```bash
# Requires Kaggle account and API key
kaggle competitions download -c deepfake-detection-challenge
```

---

### FaceForensics++ - Facial Manipulation Dataset

**Description:** Benchmark dataset for facial manipulation detection.

**Size:** ~500 GB (full), ~10 GB (compressed)

**Download:** https://github.com/ondyari/FaceForensics

**Format:** MP4 videos

**Used in Labs:**
- Lab 10: Building and Detecting Deepfake Videos

**Manipulation Methods:**
- Deepfakes
- Face2Face
- FaceSwap
- NeuralTextures

**How to Download:**
```bash
# Clone repository
git clone https://github.com/ondyari/FaceForensics.git

# Run download script
python download-FaceForensics.py
```

---

### Celeb-DF - Celebrity Deepfake Dataset

**Description:** High-quality deepfake dataset with celebrity videos.

**Size:** ~13 GB

**Download:** https://github.com/yuezunli/celeb-deepfakeforensics

**Format:** MP4 videos

**Used in Labs:**
- Lab 10: Building and Detecting Deepfake Videos

---

## Lab-Specific Dataset Mapping

### Lab 1: Automating Network Scanning and Packet Analysis

**Required Datasets:**
- Sample PCAP files (included in `labs/q1/month1/data/`)
- Optional: CTU-13 for advanced analysis

**Download Commands:**
```bash
# Sample data is included in the repository
# For additional data:
cd labs/q1/month1/data
wget https://www.malware-traffic-analysis.net/2021/01/01/2021-01-01-traffic-analysis-exercise.pcap.zip
```

---

### Lab 2: Developing a Threat Intelligence Data Pipeline

**Required Datasets:**
- AlienVault OTX (API access)
- Sample indicators (included in `labs/q1/month2/data/`)

**API Setup:**
```bash
# Sign up at https://otx.alienvault.com/
# Get your API key from account settings
export OTX_API_KEY="your_api_key_here"
```

---

### Lab 3: Building an Intelligent Malware Detection System

**Required Datasets:**
- EMBER dataset (recommended)
- Sample dataset (included in `labs/q1/month3/data/malware_dataset.csv`)

**Download Commands:**
```bash
# Install ember
pip install ember

# Download EMBER dataset
python -c "import ember; ember.create_vectorized_features('labs/q1/month3/data/ember')"
```

---

### Lab 4: Forensic Analysis of a Compromised System

**Required Datasets:**
- Digital Corpora disk images
- Sample forensic artifacts (to be provided)

**Download Commands:**
```bash
cd labs/q2/month4/data
# Download a sample disk image
wget https://digitalcorpora.s3.amazonaws.com/corpora/scenarios/2008-nitroba/nitroba-2008-challenge16.E01
```

---

### Lab 5: Automated Attack Timeline Generation

**Required Datasets:**
- Network logs (included in `labs/q2/month5/data/`)
- Optional: CIC-IDS-2017 for advanced analysis

---

### Lab 10: Building and Detecting Deepfake Videos

**Required Datasets:**
- FaceForensics++ (recommended)
- Sample videos (to be provided)

**Download Commands:**
```bash
cd labs/q3/month8/data
git clone https://github.com/ondyari/FaceForensics.git
cd FaceForensics
python download-FaceForensics.py -d original -c c23
```

---

## Dataset Storage Recommendations

Due to the large size of some datasets, we recommend:

1. **Use External Storage:** Store large datasets on external drives or network storage
2. **Download on Demand:** Only download datasets when needed for specific labs
3. **Use Subsets:** Many datasets offer smaller subsets for learning purposes
4. **Cloud Storage:** Consider using cloud storage (AWS S3, Google Cloud) for team access

---

## Dataset Licenses and Usage

Please respect the licenses and terms of use for each dataset:

- **EMBER:** Apache 2.0 License
- **Sorel-20M:** Research and educational use only
- **CTU-13:** Free for research and educational purposes
- **CIC-IDS-2017/2018:** Free for research and educational purposes
- **Digital Corpora:** Public domain
- **FaceForensics++:** Research use only, requires agreement

Always cite the datasets in your reports and publications.

---

## Troubleshooting

### Download Issues

If you encounter download issues:

1. Check your internet connection
2. Verify the download link is still active
3. Use a download manager for large files
4. Try alternative mirrors if available

### Storage Issues

If you run out of storage:

1. Use dataset subsets
2. Delete unnecessary files after labs
3. Compress datasets when not in use
4. Use cloud storage solutions

### Access Issues

If you cannot access a dataset:

1. Check if registration is required
2. Verify your API keys are correct
3. Ensure you have accepted terms of use
4. Contact dataset maintainers for support

---

## Additional Resources

- **Kaggle Datasets:** https://www.kaggle.com/datasets
- **UCI Machine Learning Repository:** https://archive.ics.uci.edu/ml/
- **AWS Open Data:** https://registry.opendata.aws/
- **Google Dataset Search:** https://datasetsearch.research.google.com/

---

**Last Updated:** January 2026
