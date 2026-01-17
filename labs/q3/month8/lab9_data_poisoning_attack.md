# Lab 9: Executing a Data Poisoning Attack on a Learning Model

## Quarter 3, Month 8, Weeks 29-30

### Objective

This lab will demonstrate the impact of a data poisoning attack on a machine learning model. You will intentionally inject mislabeled data into the training set of a classifier and observe how it degrades the model's performance and integrity. This provides a practical understanding of how attackers can corrupt AI systems at the training phase.

### Learning Outcomes

Upon completion of this lab, you will be able to:

-   Understand the mechanics and impact of a data poisoning attack.
-   Implement a targeted data poisoning attack against a classification model.
-   Measure the degradation in model performance caused by the attack.
-   Gain insight into the importance of data integrity in machine learning.

### Prerequisites

-   A strong understanding of the machine learning pipeline (training, testing, evaluation).
-   Familiarity with Python, Scikit-learn, and Pandas.

### Required Tools and Libraries

```bash
pip install scikit-learn pandas numpy matplotlib
```

### Part 1: Training a Baseline Model

**Objective:** Train a standard classification model on a clean dataset to establish a baseline for performance.

**Step 1: Set up the Python Script**

Create a file named `data_poisoning_attack.py`.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Generate a simple, clean dataset
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=1000, n_features=20, n_informative=10, n_redundant=5, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a baseline model
baseline_model = LogisticRegression()
baseline_model.fit(X_train, y_train)

# Evaluate the baseline model
y_pred_baseline = baseline_model.predict(X_test)
baseline_accuracy = accuracy_score(y_test, y_pred_baseline)
print(f"Baseline model accuracy: {baseline_accuracy:.4f}")
```

### Part 2: Implementing the Data Poisoning Attack

**Objective:** Inject mislabeled data into the training set to poison the model.

**Step 1: Create the Poisoned Dataset**

Add the following code to your script:

```python
# --- Data Poisoning Attack ---

# Percentage of data to poison
poisoning_percentage = 0.1 # 10%
num_poisoned_samples = int(len(X_train) * poisoning_percentage)

# Randomly select samples to poison
poisoned_indices = np.random.choice(len(X_train), num_poisoned_samples, replace=False)

# Create a copy of the training data to poison
X_train_poisoned = np.copy(X_train)
y_train_poisoned = np.copy(y_train)

# Flip the labels of the selected samples
for i in poisoned_indices:
    y_train_poisoned[i] = 1 - y_train_poisoned[i] # Flip 0 to 1, and 1 to 0

print(f"\nPoisoned {num_poisoned_samples} samples in the training data.")
```

**Step 2: Train the Poisoned Model**

Train a new model on the poisoned dataset.

```python
# Train a model on the poisoned data
poisoned_model = LogisticRegression()
poisoned_model.fit(X_train_poisoned, y_train_poisoned)

# Evaluate the poisoned model
y_pred_poisoned = poisoned_model.predict(X_test)
poisoned_accuracy = accuracy_score(y_test, y_pred_poisoned)
print(f"Poisoned model accuracy: {poisoned_accuracy:.4f}")

print(f"\nAccuracy degradation due to poisoning: {baseline_accuracy - poisoned_accuracy:.4f}")
```

### Part 3: Visualizing the Impact

**Objective:** Visualize the decision boundaries of the baseline and poisoned models to see the effect of the attack.

**Step 1: Add Visualization Code**

*Note: This visualization works best with a 2D dataset. We will use PCA to reduce the dimensionality for visualization purposes.*

```python
from sklearn.decomposition import PCA

# Reduce dimensionality for visualization
pca = PCA(n_components=2)
X_train_2d = pca.fit_transform(X_train)
X_train_poisoned_2d = pca.transform(X_train_poisoned)

# Retrain models on 2D data for visualization
baseline_model_2d = LogisticRegression().fit(X_train_2d, y_train)
poisoned_model_2d = LogisticRegression().fit(X_train_poisoned_2d, y_train_poisoned)

# Function to plot decision boundary
def plot_decision_boundary(model, X, y, title):
    h = .02  # step size in the mesh
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.RdYlBu, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu)
    plt.title(title)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plot_decision_boundary(baseline_model_2d, X_train_2d, y_train, "Baseline Model Decision Boundary")
plt.subplot(1, 2, 2)
plot_decision_boundary(poisoned_model_2d, X_train_poisoned_2d, y_train_poisoned, "Poisoned Model Decision Boundary")
plt.show()
```

### Deliverables

1.  **Python Script:** Submit your complete `data_poisoning_attack.py` script.
2.  **Lab Report:** A 2-3 page report that includes:
    *   The baseline and poisoned model accuracies.
    *   The visualization of the decision boundaries.
    *   An analysis of how the data poisoning attack affected the model's performance and decision-making.
    *   A discussion on potential defenses against data poisoning attacks.

### Grading Rubric

| Criterion | Points | Description |
| :--- | :--- | :--- |
| Baseline Model | 20 | Correctly trains and evaluates a baseline model. |
| Data Poisoning Implementation | 40 | Correctly implements the data poisoning attack by flipping labels. |
| Performance Evaluation | 20 | Accurately measures and reports the degradation in model performance. |
| Visualization and Report | 20 | Clear visualization and a well-written report with insightful analysis. |
| **Total** | **100** | |
