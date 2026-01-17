#!/bin/bash
# Setup Environment for AI in Cybersecurity and Digital Forensics Program
# This script installs all required dependencies

echo "============================================================"
echo "Environment Setup"
echo "Advanced AI in Cybersecurity and Digital Forensics"
echo "============================================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "[!] Please do not run this script as root"
    exit 1
fi

# Update package lists
echo "[*] Updating package lists..."
sudo apt-get update -qq

# Install system dependencies
echo "[*] Installing system dependencies..."
sudo apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpcap-dev \
    tcpdump \
    wireshark-common \
    git \
    curl \
    wget

# Install Python packages
echo "[*] Installing Python packages..."
pip3 install --user --upgrade pip

echo "[*] Installing core packages..."
pip3 install --user \
    numpy \
    pandas \
    scikit-learn \
    matplotlib \
    seaborn \
    jupyter \
    notebook

echo "[*] Installing security packages..."
pip3 install --user \
    scapy \
    requests \
    beautifulsoup4 \
    python-nmap

echo "[*] Installing machine learning packages..."
pip3 install --user \
    tensorflow \
    keras \
    torch \
    torchvision

echo "[*] Installing adversarial ML packages..."
pip3 install --user \
    adversarial-robustness-toolbox

echo "[*] Installing additional utilities..."
pip3 install --user \
    joblib \
    tqdm \
    colorama

# Create virtual environment (optional but recommended)
echo "[*] Creating virtual environment..."
python3 -m venv ~/ai-cyber-env

echo ""
echo "[+] Environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "    source ~/ai-cyber-env/bin/activate"
echo ""
echo "To generate sample datasets, run:"
echo "    python3 scripts/generate_sample_data.py"
echo ""
echo "============================================================"
