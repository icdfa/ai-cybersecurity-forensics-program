# Lab 11: AI Red Teaming Framework

---

## Overview

This lab introduces a structured framework for AI Red Teaming, a critical practice for proactively identifying and mitigating security vulnerabilities in AI systems. Unlike traditional penetration testing, AI red teaming focuses on the unique attack surfaces of machine learning models, including their data, algorithms, and infrastructure. Students will use a comprehensive Python-based framework to conduct a security assessment of the deepfake detection model built in Lab 10.

## Learning Objectives

Upon completing this lab, students will be able to:

- Understand the principles and methodology of AI red teaming.
- Identify key vulnerability categories specific to AI systems.
- Conduct a structured security assessment using an automated framework.
- Analyze and interpret the results of various security tests, including adversarial robustness and bias detection.
- Generate a professional red team report with risk scores and actionable recommendations.
- Think adversarially about AI systems and propose effective security controls.

## Prerequisites

- Completion of Labs 1-10.
- A trained deepfake detection model from Lab 10.
- Deep understanding of adversarial attacks, model evaluation, and fairness concepts.

## Lab Environment

- **Python Version:** 3.8+
- **Libraries:** scikit-learn, pandas, numpy
- **Setup:** Ensure all dependencies from requirements.txt are installed.

## Lab Files

- **Code:** code/ai_red_team.py - The main script for the red teaming framework.
- **Target Model:** ../month9/models/deepfake_detector.pkl - The model to be tested.
- **Dataset:** ../month9/data/deepfake_dataset.csv - The dataset for testing.
- **Worksheet:** worksheets/lab11_worksheet.md - Questions and exercises.

---

## Part 1: The AI Red Teaming Methodology

AI red teaming is a systematic process. Our framework automates tests across several key vulnerability categories.

| Category                   | Description                                                                 | Test Implemented in this Lab                                    |
| -------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Adversarial Robustness** | The model's resilience to small, malicious input perturbations.             | **Adversarial Example Attack:** Measures misclassification rate.  |
| **Model Confidence**       | The model's ability to provide appropriate confidence scores.               | **Confidence Calibration Test:** Detects high-confidence errors.  |
| **Privacy Leakage**        | The risk of the model leaking sensitive information from its training data. | **Feature Importance Analysis:** Checks for dominant features.    |
| **Input Validation**       | The model's ability to handle unexpected or malicious inputs gracefully.    | **Input Boundary Test:** Tests extreme and invalid values.        |
| **Fairness and Bias**      | The model's tendency to perform differently for different demographic groups. | **Bias Detection Test:** Measures performance disparity.          |

### Severity Levels

The framework assigns a severity level to each finding to prioritize remediation efforts:

- **Critical:** Poses an immediate and severe risk.
- **High:** Poses a significant risk that should be addressed promptly.
- **Medium:** Represents a moderate risk that should be addressed.
- **Low:** A minor issue with low potential for exploitation.
- **Informational:** An observation that does not pose a direct risk.

---

## Part 2: Conducting the Red Team Assessment

The ai_red_team.py script is designed to run a full assessment against the target model.

### Task 2.1: Run the Full Assessment

1.  Navigate to the lab directory:
    ```bash
    cd labs/q3/month9/
    ```

2.  Ensure the model and dataset from Lab 10 are present in the correct locations. The script is configured to find them automatically.

3.  Run the red team script:
    ```bash
    python3 code/ai_red_team.py
    ```

4.  The script will execute five distinct tests and print the results to the console. It will also generate a detailed JSON report in results/red_team_report.json.

### Task 2.2: Analyze the Console Output

Review the output for each of the five tests. In your worksheet, record the key findings for each test:

- **Adversarial Robustness:** What was the success rate of the attack? What severity was assigned?
- **Model Confidence:** What was the overconfidence rate? How many high-confidence errors were found?
- **Feature Importance Leakage:** What was the maximum feature importance? Was a vulnerability identified?
- **Input Validation:** Did the model pass the input validation tests?
- **Model Bias:** What was the performance disparity between the two groups?

---

## Part 3: Interpreting the Red Team Report

Open the generated results/red_team_report.json file. This file contains the full details of the assessment.

### Task 3.1: Understand the Report Structure

Familiarize yourself with the JSON structure. It contains:
- model_name and test_date.
- vulnerabilities: A list of all findings with a severity of Medium or higher.
- all_tests: A complete log of every test performed.
- summary: A high-level overview including the final risk score.

### Task 3.2: Analyze the Summary and Risk Score

1.  What is the final **Risk Score** for the Deepfake Detector model?
2.  Based on the severity_breakdown, what are the most pressing issues?
3.  In your worksheet, write a brief executive summary explaining the overall security posture of the AI system based on this report.

---

## Part 4: Discussion and Recommendations

Answer the following questions in your lab worksheet.

1.  **Prioritizing Remediation:** Based on the report, which vulnerability should be fixed first? Justify your choice based on severity and potential impact.

2.  **Actionable Recommendations:** For the top vulnerability you identified, what specific steps would you recommend to the development team to mitigate the risk?

3.  **Limitations of the Framework:** This framework automates several key tests. What are some potential AI vulnerabilities that are not covered by this automated assessment?

4.  **Continuous Red Teaming:** Why is it important to perform red teaming continuously throughout the AI model's lifecycle, rather than just once before deployment?

5.  **The Red Teamer's Mindset:** What does it mean to have an "adversarial mindset" when it comes to AI security? How does this differ from a standard software testing mindset?

---

## Submission

- Submit your completed worksheets/lab11_worksheet.md file.
- Submit the results/red_team_report.json file generated by the script.
- Include a brief summary of your findings and recommendations for the Deepfake Detector model.

---

## Further Exploration (Optional)

- **Target a Different Model:** Train a different type of model in Lab 10 and run the red team assessment against it. Is it more or less secure? 
- **Expand the Framework:** Add a new test to the AIRedTeamFramework class. For example, implement a basic model extraction test.
- **Visualize the Report:** Write a Python script to parse the red_team_report.json file and generate a more user-friendly HTML or PDF report with charts and graphs.
