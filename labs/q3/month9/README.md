# Quarter 3, Month 9: Deepfake Detection System

## Lab 10: Detecting AI-Generated Media

---

## Overview

This lab focuses on building a machine learning system to detect deepfakes - AI-generated media that appears authentic but is actually fabricated. Students will train and evaluate a classifier using pre-extracted features from media files.

## Lab Files

- **Lab Manual:** `lab10_deepfake_detection.md`
- **Code:** `code/deepfake_detector.py`
- **Worksheet:** `worksheets/lab10_worksheet.md`
- **Dataset:** `data/deepfake_dataset.csv` (generated)

## Learning Outcomes

By completing this lab, students will:
- Understand the deepfake detection challenge
- Implement a machine learning detection pipeline
- Evaluate model performance with multiple metrics
- Analyze feature importance for detection
- Consider real-world implications

## Prerequisites

- Python 3.8+
- Libraries: scikit-learn, pandas, numpy
- Completion of Labs 1-9

## Quick Start

```bash
# Generate the dataset
cd ../../..
python3 scripts/generate_sample_data.py

# Run the detector
cd labs/q3/month9
python3 code/deepfake_detector.py

# Run with detailed analysis
python3 code/deepfake_detector.py --analyze
```

## Features Analyzed

The system analyzes 10 key features:
- Facial landmark consistency
- Blinking pattern frequency
- Head pose variance
- Lighting inconsistency score
- Compression artifact level
- Temporal coherence error
- Audio sync offset
- Face resolution mismatch
- Color distribution anomaly
- Edge sharpness inconsistency

## Expected Performance

The model should achieve:
- Accuracy: >99%
- Precision: >99%
- Recall: >99%
- Very low false positive rate

---

**Month 9 of 12** | **Quarter 3: Offensive AI**
