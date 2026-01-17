# Lab 8 Worksheet: Evasion Attacks

---

## Student Name: [Your Name]

## Date: [Date]

---

## Part 1: Baseline Model Analysis

### 1.1 Baseline Performance

After running the script for the first time, record the baseline performance of the malware classifier.

- **Baseline Accuracy:** [Fill in]
- **Malware Recall (Sensitivity):** [Fill in from the classification report]

**Question:** Why is recall a particularly important metric for a malware classifier? What is the risk of having a low recall?

> [Your answer here]

---

## Part 2: Evasion Attack Analysis

Run each of the evasion attacks and record your findings in the table below. You can find the detailed results in the `attack_results.json` file after running the script with `--attack-type all`.

### 2.1 Attack Comparison Table

| Attack Type              | Overall Success Rate (%) | Average Perturbation Magnitude (for successful attacks) |
| ------------------------ | ------------------------ | ------------------------------------------------------- |
| Feature Manipulation     | [Fill in]                | [Fill in]                                               |
| Gradient-Based           | [Fill in]                | [Fill in]                                               |
| Mimicry                  | [Fill in]                | [Fill in]                                               |

**Instructions:** To calculate the average perturbation for successful attacks, you will need to parse the `attack_results.json` file. You can do this manually or write a small script.

### 2.2 Analysis Questions

**Question 1:** Which evasion attack was the most effective against the Random Forest classifier? Based on your understanding of the attack and the model, provide a hypothesis for why it performed the best.

> [Your answer here]

**Question 2:** Does a successful attack always require a large perturbation? Discuss the relationship between perturbation magnitude and attack success based on your results.

> [Your answer here]

---

## Part 3: Defenses and Implications

### 3.1 Defense Strategies

**Question 3:** Propose two potential defense strategies that could make the malware classifier more robust against these evasion attacks. Explain how each defense would work.

- **Defense 1:**
  > [Your proposed defense and explanation]

- **Defense 2:**
  > [Your proposed defense and explanation]

### 3.2 Real-World and Ethical Implications

**Question 4:** Why are evasion attacks a significant threat to AI-powered security systems (e.g., antivirus, intrusion detection systems)? Provide a real-world example scenario.

> [Your answer here]

**Question 5:** What are the ethical responsibilities of researchers who discover and publish new adversarial attack techniques? Discuss the concept of responsible disclosure in this context.

> [Your answer here]

---

## Submission Checklist

- [ ] Completed all sections of this worksheet.
- [ ] Attached the `attack_results.json` file from your `--attack-type all` run.
- [ ] Included a brief summary of your key takeaways from the lab.

### Summary & Key Takeaways

> [Write your summary here]
