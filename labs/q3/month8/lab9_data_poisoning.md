# Lab 9: Data Poisoning Attacks on Machine Learning Models

---

## Overview

This lab explores data poisoning attacks, a type of adversarial attack where an attacker manipulates the training data to compromise a machine learning model. Students will implement and evaluate several data poisoning techniques to understand their impact on model performance and integrity.

## Learning Objectives

Upon completing this lab, students will be able to:

- Understand the principles of data poisoning attacks.
- Implement label flipping, feature manipulation, and backdoor poisoning attacks.
- Evaluate the impact of poisoned data on model accuracy and performance.
- Analyze the effectiveness of backdoor attacks.
- Propose and discuss potential defenses against data poisoning.

## Prerequisites

- Completion of Labs 1-8.
- Understanding of machine learning training pipelines.
- Proficiency in Python and familiarity with `scikit-learn` and `pandas`.

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

- **Code:** `code/data_poisoning_attack.py` - The main script for implementing and evaluating data poisoning attacks.
- **Dataset:** `data/malware_dataset.csv` - A sample dataset of malware and benign files.
- **Worksheet:** `worksheets/lab9_worksheet.md` - Questions and exercises to be completed by the student.

---

## Part 1: Understanding Data Poisoning

Data poisoning attacks target the training phase of a machine learning model. By injecting malicious data, an attacker can degrade the model's performance, cause it to misclassify specific inputs, or create backdoors for later exploitation.

### Task 1.1: Train and Evaluate the Clean Model

First, we will train a model on clean data to establish a baseline for performance.

1.  Navigate to the lab directory:
    ```bash
    cd labs/q3/month8/
    ```

2.  Run the script with default settings. This will train a Random Forest classifier on a clean dataset.
    ```bash
    python3 code/data_poisoning_attack.py
    ```

3.  **Analyze the output:**
    - The script first trains a "Clean Model". Note its accuracy, precision, recall, and F1-score.
    - This baseline represents the expected performance of the model under normal conditions.

---

## Part 2: Implementing Data Poisoning Attacks

The script implements three types of data poisoning attacks. We will now execute these attacks and observe their impact.

### Task 2.1: Label Flipping Attack

This attack involves flipping the labels of a small percentage of the training data. For example, a malware sample is relabeled as benign.

1.  Run the script with the `label_flip` attack type and a 10% poison rate:
    ```bash
    python3 code/data_poisoning_attack.py --attack-type label_flip --poison-rate 0.1
    ```

2.  **Analyze the output:**
    - The script will train a "Poisoned Model" on the data with flipped labels.
    - Compare the performance of the poisoned model to the clean model. How much did the accuracy degrade?
    - Look at the `poisoning_comparison.png` file. How does the visualization show the impact of the attack?

### Task 2.2: Feature Manipulation Attack

This attack involves adding noise or perturbations to the features of some training samples, making them harder to classify correctly.

1.  Run the script with the `feature_manipulation` attack type:
    ```bash
    python3 code/data_poisoning_attack.py --attack-type feature_manipulation --poison-rate 0.1
    ```

2.  **Analyze the output:**
    - How does the performance degradation from this attack compare to the label flipping attack?
    - Is this attack more or less effective at reducing the model's accuracy? Why?

### Task 2.3: Backdoor Attack

This is a more sophisticated attack where the attacker injects a hidden "trigger" into the training data. The model learns to associate this trigger with a specific (incorrect) class. The model performs normally on clean data but misclassifies any input that contains the trigger.

1.  Run the script with the `backdoor` attack type:
    ```bash
    python3 code/data_poisoning_attack.py --attack-type backdoor --poison-rate 0.05
    ```

2.  **Analyze the output:**
    - Look at the general performance of the poisoned model. Does the accuracy degrade significantly? Often, backdoor attacks have a minimal impact on overall accuracy.
    - Now, look at the "Backdoor success rate". What does this metric represent?
    - A high backdoor success rate means the attacker can reliably cause misclassification by injecting the trigger. Why is this a particularly dangerous type of attack?

---

## Part 3: Analysis and Discussion

Answer the following questions in your lab worksheet (`worksheets/lab9_worksheet.md`).

1.  **Impact on Performance:** Which data poisoning attack had the most significant impact on the model's overall accuracy? Which had the least? Explain your reasoning.

2.  **Backdoor Attacks:** Why are backdoor attacks considered more insidious than simple availability attacks (like label flipping)? Explain the difference in the attacker's goal.

3.  **Poison Rate:** Experiment with different poison rates (e.g., `--poison-rate 0.01`, `0.2`, `0.5`). How does the poison rate affect the success of each attack? Is there a point of diminishing returns?

4.  **Defenses:** Propose two potential defense strategies against data poisoning attacks. Consider both data-level defenses (e.g., data sanitization) and model-level defenses (e.g., robust training methods).

5.  **Real-World Scenarios:** Describe a real-world scenario where a data poisoning attack could be used to compromise a security system. For example, consider a spam filter, a network intrusion detection system, or a biometric authentication system.

---

## Submission

- Submit your completed `worksheets/lab9_worksheet.md` file.
- Submit the `poisoning_results.json` and `poisoning_comparison.png` files for each of the three attack types.
- Include a brief summary of your findings, comparing the different attack types and their impact.

---

## Further Exploration (Optional)

- **Different Models:** The script supports both Random Forest (`--model-type rf`) and Logistic Regression (`--model-type lr`). Compare the vulnerability of these two models to data poisoning. Which is more robust?
- **Implement a Defense:** Try to implement a data sanitization defense. For example, you could use outlier detection to identify and remove potentially poisoned samples from the training set before training the model. Evaluate whether this defense reduces the impact of the attacks.
- **Advanced Poisoning:** Research more advanced data poisoning techniques, such as targeted poisoning attacks that aim to cause misclassification of a *specific* test sample.
- **Transferability:** Investigate whether a poisoned dataset used to train one model type (e.g., Logistic Regression) can also compromise a different model type (e.g., a neural network).
