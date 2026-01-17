# Quarter 3, Month 8: Adversarial Machine Learning

## Lab 8: Evasion Attacks
## Lab 9: Data Poisoning Attacks

---

## Overview

This month focuses on adversarial attacks against machine learning models used in cybersecurity. Students will implement and analyze both evasion attacks (targeting inference) and data poisoning attacks (targeting training).

## Lab Files

### Lab 8: Evasion Attacks
- **Lab Manual:** `lab8_evasion_attack.md`
- **Code:** `code/evasion_attack.py`
- **Worksheet:** `worksheets/lab8_worksheet.md`
- **Dataset:** `data/malware_dataset.csv`

### Lab 9: Data Poisoning Attacks
- **Lab Manual:** `lab9_data_poisoning.md`
- **Code:** `code/data_poisoning_attack.py`
- **Worksheet:** `worksheets/lab9_worksheet.md`
- **Dataset:** `data/malware_dataset.csv`

## Learning Outcomes

By completing these labs, students will:
- Understand adversarial attacks on ML models
- Implement evasion and poisoning techniques
- Evaluate attack effectiveness
- Propose defensive strategies

## Prerequisites

- Python 3.8+
- Libraries: scikit-learn, pandas, numpy, matplotlib
- Completion of Labs 1-7

## Quick Start

```bash
# Generate sample data
cd ../../../
python3 scripts/generate_sample_data.py

# Copy data to lab directory
cp labs/q1/month3/data/malware_dataset.csv labs/q3/month8/data/

# Run Lab 8
cd labs/q3/month8
python3 code/evasion_attack.py --dataset data/malware_dataset.csv --attack-type all

# Run Lab 9
python3 code/data_poisoning_attack.py --dataset data/malware_dataset.csv --attack-type label_flip
```

---

**Month 8 of 12** | **Quarter 3: Offensive AI**
