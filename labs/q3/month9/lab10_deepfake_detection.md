# Lab 10: Deepfake Detection System

---

## Overview

This lab provides a comprehensive introduction to building a deepfake detection system. As AI-generated media becomes more sophisticated, the ability to distinguish between real and fake content is a critical skill in cybersecurity and digital forensics. Students will use a machine learning model to classify media samples based on a set of pre-extracted features, simulating a real-world detection pipeline.

## Learning Objectives

Upon completing this lab, students will be able to:

- Understand the challenges and importance of deepfake detection.
- Implement a machine learning pipeline for classification.
- Train and evaluate a deepfake detection model.
- Interpret model performance metrics, including the confusion matrix, precision, and recall.
- Analyze feature importance to understand what indicators the model uses for detection.
- Perform detailed analysis on individual samples to identify high-confidence errors and other anomalies.

## Prerequisites

- Completion of Labs 1-9.
- Strong understanding of machine learning concepts, particularly classification models like Random Forest.
- Proficiency in Python and experience with `scikit-learn`, `pandas`, and `numpy`.

## Lab Environment

- **Python Version:** 3.8+
- **Libraries:** `scikit-learn`, `pandas`, `numpy`, `matplotlib`
- **Setup:**
  ```bash
  # Navigate to the repository root
  cd /path/to/ai-cybersecurity-forensics-program

  # Install dependencies
  pip install -r requirements.txt
  ```

## Lab Files

- **Code:** `code/deepfake_detector.py` - The main script for building, training, and evaluating the detector.
- **Dataset:** `data/deepfake_dataset.csv` - A sample dataset with pre-extracted features from real and fake media.
- **Worksheet:** `worksheets/lab10_worksheet.md` - Questions and exercises for the student.

---

## Part 1: Understanding the Dataset and Features

This lab uses a simulated dataset where features have already been extracted from media files. In a real-world scenario, this feature extraction step would involve complex computer vision and signal processing techniques to identify artifacts unique to deepfakes.

**Simulated Features May Include:**
- **`facial_landmark_consistency`:** Measures the stability of facial landmarks over time.
- **`blinking_pattern_freq`:** Analyzes the frequency and duration of eye blinks, which are often unnatural in deepfakes.
- **`head_pose_variance`:** Measures the natural movement and rotation of the head.
- **`lighting_inconsistency_score`:** Detects unnatural shadows and lighting on the face.
- **`compression_artifact_level`:** Measures artifacts introduced by the deepfake generation process.
- **`temporal_coherence_error`:** Checks for inconsistencies between video frames.
- **`audio_sync_offset`:** Measures the synchronization between video and audio tracks.

### Task 1.1: Explore the Dataset

Before running the code, open the `data/deepfake_dataset.csv` file (you will need to generate it first) and examine its structure. 

1.  How many features are there?
2.  What is the meaning of the `label` column?
3.  Is the dataset balanced between real and fake samples?

---

## Part 2: Building and Training the Detector

The `deepfake_detector.py` script automates the process of training and evaluating a Random Forest classifier for this task.

### Task 2.1: Train and Evaluate the Baseline Model

1.  Navigate to the lab directory:
    ```bash
    cd labs/q3/month9/
    ```

2.  First, you need to generate the sample dataset. The script for this is in the main `scripts` directory.
    ```bash
    # From the lab directory
    python3 ../../../scripts/generate_sample_data.py --labs deepfake
    ```
    This will create the `data/deepfake_dataset.csv` file.

3.  Run the main lab script to train the model and get a baseline evaluation.
    ```bash
    python3 code/deepfake_detector.py
    ```

4.  **Analyze the output:**
    - Record the **Accuracy, Precision, Recall, and F1-Score** in your worksheet.
    - Examine the **Confusion Matrix**. How many false positives and false negatives did the model produce? What are the real-world consequences of each type of error in a deepfake detection context?

---

## Part 3: In-Depth Analysis

The script includes an `analyze` mode that provides deeper insights into the model's behavior.

### Task 3.1: Perform Detailed Analysis

1.  Run the script with the `--analyze` flag:
    ```bash
    python3 code/deepfake_detector.py --analyze
    ```

2.  **Analyze the output:**
    - **Individual Sample Analysis:** The script analyzes the first five test samples. For each, it shows the true label, the model's prediction, and the confidence level. Are there any incorrect predictions? If so, what is the model's confidence in the wrong prediction?
    - **Feature Importance:** The script lists the top 5 most important features the model used to make its decisions. What are these features? Why do you think they are strong indicators of a deepfake?
    - **Batch Analysis:** The script reports on high-confidence errors and low-confidence correct predictions. Why is it important to analyze these specific cases when evaluating a model?

---

## Part 4: Discussion and Critical Thinking

Answer the following questions in your lab worksheet (`worksheets/lab10_worksheet.md`).

1.  **Model Performance:** Based on the evaluation metrics, how would you rate the performance of this deepfake detector? Is it reliable enough for real-world use? Justify your answer.

2.  **Error Analysis:** Discuss the difference between a false positive and a false negative in the context of deepfake detection. Which error type is more dangerous and why?

3.  **Feature Engineering:** The lab used pre-extracted features. If you had to design a feature extraction pipeline from scratch for video files, what are three key features you would prioritize extracting and why?

4.  **The Arms Race:** Deepfake detection is often described as an "arms race" between creators and detectors. Explain what this means. How might a deepfake creator use their knowledge of detection techniques to create more convincing fakes?

5.  **Ethical and Societal Impact:** Beyond security, what are some of the broader societal implications of deepfake technology? Discuss its potential impact on politics, journalism, and personal reputation.

---

## Submission

- Submit your completed `worksheets/lab10_worksheet.md` file.
- Submit the `detection_results.json` file generated from your `--analyze` run.
- Include a brief summary of your findings and key takeaways from the lab.

---

## Further Exploration (Optional)

- **Use a Different Model:** Modify the script to use a different classifier (e.g., `GradientBoostingClassifier`, `SVC`). Does it perform better or worse? 
- **Adversarial Attacks:** How might the evasion attack techniques from Lab 8 be applied to this deepfake detector? Outline a strategy for an attack.
- **Real-World Datasets:** Research and find a public deepfake detection dataset (e.g., FaceForensics++, Celeb-DF). Download a small portion of it and try to adapt the lab script to work with real image or video data (this is a significant challenge).
- **Explainability (XAI):** Use a library like SHAP or LIME to generate more detailed explanations for individual predictions. What new insights can you gain?
