# Lab 10 Worksheet: Deepfake Detection System

---

## Student Name: [Your Name]

## Date: [Date]

---

## Part 1: Dataset Exploration

### 1.1 Dataset Analysis

Before running the code, generate the dataset and explore its contents.

```bash
# From the labs/q3/month9/ directory
python3 ../../../scripts/generate_sample_data.py --labs deepfake
```

Now, inspect the `data/deepfake_dataset.csv` file.

- **Number of Features:** [Fill in]
- **Meaning of `label` column:** [Fill in (e.g., 0 = ?, 1 = ?)]
- **Is the dataset balanced?** (Count the number of real vs. fake samples) 
  - **Real Samples:** [Fill in]
  - **Fake Samples:** [Fill in]

---

## Part 2: Baseline Model Evaluation

Run the script without any special flags to train and evaluate the baseline model.

```bash
python3 code/deepfake_detector.py
```

### 2.1 Baseline Performance Metrics

Record the performance from the script's output.

| Metric      | Score     |
| ----------- | --------- |
| Accuracy    | [Fill in] |
| Precision   | [Fill in] |
| Recall      | [Fill in] |
| F1-Score    | [Fill in] |

### 2.2 Confusion Matrix Analysis

Record the values from the confusion matrix.

- **True Negatives (TN):** [Fill in] (Correctly identified as Real)
- **False Positives (FP):** [Fill in] (Incorrectly identified as Fake)
- **False Negatives (FN):** [Fill in] (Incorrectly identified as Real)
- **True Positives (TP):** [Fill in] (Correctly identified as Fake)

**Question:** What are the real-world consequences of a **False Positive** in a deepfake detection system? What about a **False Negative**?

> [Your answer here]

---

## Part 3: In-Depth Analysis

Run the script with the `--analyze` flag.

```bash
python3 code/deepfake_detector.py --analyze
```

### 3.1 Individual Sample Analysis

Review the analysis of the first five test samples.

**Question:** Were there any incorrect predictions among the first five samples? If so, what was the model's confidence in its incorrect prediction? What does a high-confidence error suggest about the model or the data?

> [Your answer here]

### 3.2 Feature Importance

List the top 5 most important features identified by the model.

1.  **Feature:** [Fill in] (Importance: [Fill in])
2.  **Feature:** [Fill in] (Importance: [Fill in])
3.  **Feature:** [Fill in] (Importance: [Fill in])
4.  **Feature:** [Fill in] (Importance: [Fill in])
5.  **Feature:** [Fill in] (Importance: [Fill in])

**Question:** Why do you think these features are the strongest indicators of a deepfake in this dataset?

> [Your answer here]

### 3.3 Batch Analysis Insights

**Question:** The script reports on "high-confidence errors" and "low-confidence correct predictions." Why is it important for a data scientist to analyze these specific cases when evaluating a model's performance and reliability?

> [Your answer here]

---

## Part 4: Discussion and Critical Thinking

### 4.1 Critical Evaluation

**Question 1:** Based on the evaluation metrics, how would you rate the performance of this deepfake detector? Is it reliable enough for real-world use in a high-stakes environment (e.g., for a news organization or a court of law)? Justify your answer.

> [Your answer here]

**Question 2:** The "arms race" in deepfake technology involves a constant back-and-forth between generation and detection. How might a deepfake creator use their knowledge of the features you listed in 3.2 to create a more convincing, harder-to-detect deepfake?

> [Your answer here]

**Question 3:** Beyond security, what are some of the broader societal implications of deepfake technology? Discuss its potential impact on politics, journalism, and personal reputation.

> [Your answer here]

---

## Submission Checklist

- [ ] Completed all sections of this worksheet.
- [ ] Attached the `detection_results.json` file from your `--analyze` run.
- [ ] Included a brief summary of your key takeaways from the lab.

### Summary & Key Takeaways

> [Write your summary here. What was the most surprising or interesting thing you learned in this lab?]
