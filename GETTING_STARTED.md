# Getting Started Guide

Welcome to the Advanced AI in Cybersecurity and Digital Forensics Program! This guide will help you set up your environment and get started with the labs.

## Prerequisites

Before starting the program, ensure you have:

- **Operating System:** Linux (Ubuntu 20.04+ recommended), macOS, or Windows with WSL2
- **Python:** Version 3.8 or higher
- **RAM:** Minimum 8GB (16GB recommended for machine learning labs)
- **Storage:** At least 50GB free space for datasets
- **Internet Connection:** Required for downloading datasets and packages

## Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/icdfa/ai-cybersecurity-forensics-program.git
cd ai-cybersecurity-forensics-program
```

### Step 2: Set Up Environment

#### Option A: Automatic Setup (Recommended)

```bash
# Run the setup script
bash scripts/setup_environment.sh

# Activate virtual environment
source ~/ai-cyber-env/bin/activate
```

#### Option B: Manual Setup

```bash
# Create virtual environment
python3 -m venv ai-cyber-env
source ai-cyber-env/bin/activate  # On Windows: ai-cyber-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Generate Sample Data

```bash
# Generate sample datasets for labs
python3 scripts/generate_sample_data.py
```

### Step 4: Verify Installation

```bash
# Test Python packages
python3 -c "import numpy, pandas, sklearn, scapy; print('All packages installed successfully!')"
```

## Lab Structure

Each lab follows this structure:

```
labs/qX/monthY/
├── README.md              # Lab overview and instructions
├── labN_name.md          # Detailed lab assignment
├── code/                 # Python scripts and code examples
│   ├── script1.py
│   └── script2.py
├── data/                 # Sample datasets
│   ├── dataset1.csv
│   └── dataset2.json
└── worksheets/           # Lab worksheets and exercises
    └── worksheet.md
```

## Running Your First Lab

### Lab 1: Network Scanning

```bash
# Navigate to Lab 1
cd labs/q1/month1

# Read the lab instructions
cat lab1_network_scanning.md

# Run the network scanner (requires root/admin for some features)
cd code
python3 network_scanner.py --help

# Example: ARP scan
sudo python3 network_scanner.py --arp-scan 192.168.1.0/24
```

### Lab 2: Threat Intelligence Pipeline

```bash
# Navigate to Lab 2
cd labs/q1/month2/code

# Initialize the threat intelligence database
python3 threat_intel_pipeline.py --collect --source otx --count 20

# Query indicators
python3 threat_intel_pipeline.py --query

# Get statistics
python3 threat_intel_pipeline.py --stats
```

### Lab 3: Malware Detection

```bash
# Navigate to Lab 3
cd labs/q1/month3/code

# Train a malware detection model
python3 malware_detector.py --train --data ../data/malware_dataset.csv --model random_forest

# The model will be saved as malware_detector.pkl
```

## Working with Datasets

### Included Sample Data

The repository includes sample datasets for quick start:

- **Lab 1:** Sample PCAP files
- **Lab 2:** Sample threat indicators (200 indicators)
- **Lab 3:** Malware dataset (2,000 samples)
- **Lab 5:** Network logs (1,000 entries)

### Downloading Real Datasets

For production-quality datasets, refer to `resources/datasets/DATASETS.md`:

```bash
# Example: Download EMBER malware dataset
pip install ember
python -c "import ember; ember.create_vectorized_features('labs/q1/month3/data/ember')"
```

## Development Environment

### Recommended IDE Setup

**VS Code:**
```bash
# Install VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

**PyCharm:**
- Open the project directory
- Configure Python interpreter to use the virtual environment
- Install recommended plugins for Jupyter and data science

### Jupyter Notebooks

Some labs include Jupyter notebooks for interactive analysis:

```bash
# Start Jupyter
jupyter notebook

# Navigate to labs/qX/monthY/ and open .ipynb files
```

## Common Issues and Solutions

### Issue: Permission Denied for Network Scanning

**Solution:** Run network scanning scripts with sudo:
```bash
sudo python3 network_scanner.py --arp-scan 192.168.1.0/24
```

### Issue: Module Not Found

**Solution:** Ensure virtual environment is activated and packages are installed:
```bash
source ai-cyber-env/bin/activate
pip install -r requirements.txt
```

### Issue: Out of Memory

**Solution:** Reduce dataset size or use sampling:
```bash
python3 malware_detector.py --train --data dataset.csv --sample-size 1000
```

### Issue: Dataset Download Fails

**Solution:** Check internet connection and try alternative mirrors. See `resources/datasets/DATASETS.md` for mirrors.

## Learning Path

### Beginner Track (Months 1-3)

1. Complete Lab 1: Network Scanning
2. Complete Lab 2: Threat Intelligence
3. Complete Lab 3: Malware Detection
4. Review curriculum materials in `curriculum/`

### Intermediate Track (Months 4-6)

1. Complete Labs 4-6 (Digital Forensics)
2. Work on Q2 mini-project
3. Study assessment materials

### Advanced Track (Months 7-9)

1. Complete Labs 7-12 (Adversarial AI)
2. Work on Q3 mini-project
3. Begin capstone project planning

### Capstone (Months 10-12)

1. Select capstone project topic
2. Implement and test solution
3. Write final report
4. Prepare presentation

## Additional Resources

### Documentation

- **Curriculum:** `curriculum/README.md`
- **Datasets:** `resources/datasets/DATASETS.md`
- **Tools:** `resources/tools/README.md`
- **Research:** `resources/research/README.md`

### Community and Support

- **Issues:** Report bugs or ask questions via GitHub Issues
- **Discussions:** Join discussions in GitHub Discussions
- **Contributing:** See `CONTRIBUTING.md` for contribution guidelines

### Recommended Reading

- NIST Cybersecurity Framework
- MITRE ATT&CK Framework
- OWASP Top 10
- Papers in `resources/research/`

## Tips for Success

1. **Follow the Labs in Order:** Each lab builds on previous knowledge
2. **Read Documentation:** Always read README files and lab instructions carefully
3. **Experiment:** Modify code and try different approaches
4. **Document Your Work:** Keep notes and document your findings
5. **Ask Questions:** Use GitHub Issues or Discussions for help
6. **Practice Regularly:** Consistent practice is key to mastery
7. **Join the Community:** Engage with other learners

## Next Steps

1. Complete environment setup
2. Read the curriculum overview in `curriculum/`
3. Start with Lab 1
4. Join the community discussions

---

**Need Help?**

- Check the FAQ in each lab's README
- Review troubleshooting section above
- Open an issue on GitHub
- Contact instructors (see instructor guides)

**Ready to begin? Start with Lab 1!**

```bash
cd labs/q1/month1
cat README.md
```

---

**Last Updated:** January 2026
