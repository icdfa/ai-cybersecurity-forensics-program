# Lab 8: Bypassing a Malware Classifier with an Evasion Attack

## Quarter 3, Month 7, Weeks 27-28

### Objective

This lab provides hands-on experience with a common type of adversarial attack: the evasion attack. You will take a pre-trained machine learning model for malware classification and craft an adversarial example to bypass it. This lab will demonstrate how attackers can subtly modify malicious files to evade AI-based security defenses.

### Learning Outcomes

Upon completion of this lab, you will be able to:

-   Understand the principles of evasion attacks against machine learning models.
-   Implement the Fast Gradient Sign Method (FGSM) to generate adversarial examples.
-   Evaluate the effectiveness of an evasion attack against a malware classifier.
-   Gain insight into the vulnerabilities of AI-based security systems.

### Prerequisites

-   A strong understanding of machine learning classification models.
-   Familiarity with Python, TensorFlow, and NumPy.
-   Completion of the previous labs in the program.

### Required Tools and Libraries

```bash
pip install tensorflow numpy matplotlib
```

### Part 1: Loading the Pre-Trained Malware Classifier

**Objective:** Load a pre-trained model and a sample malware file.

**Step 1: Set up the Python Script**

Create a file named `evasion_attack.py`.

```python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Load a pre-trained model (for this lab, we'll create a simple one)
# In a real scenario, you would load a more complex model.
def create_simple_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation="relu", input_shape=(2381,)), # EMBER dataset has 2381 features
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

model = create_simple_model()
# In a real lab, you would load weights: model.load_weights("malware_classifier.h5")

# Load a sample malware file (as a feature vector)
# For this lab, we'll generate a random one.
malware_sample = np.random.rand(1, 2381).astype(np.float32)
malware_label = np.array([1]) # 1 for malware

# Convert to TensorFlow tensors
malware_sample = tf.convert_to_tensor(malware_sample)
malware_label = tf.convert_to_tensor(malware_label, dtype=tf.float32)

# Check the model's initial prediction
initial_prediction = model(malware_sample)
print(f"Initial prediction (should be close to 1): {initial_prediction.numpy()[0][0]}")
```

### Part 2: Implementing the FGSM Evasion Attack

**Objective:** Implement the Fast Gradient Sign Method to create an adversarial example.

**Step 1: Add the FGSM Attack Function**

Add the following code to your script:

```python
def create_adversarial_pattern(input_sample, input_label, model):
    loss_object = tf.keras.losses.BinaryCrossentropy()

    with tf.GradientTape() as tape:
        tape.watch(input_sample)
        prediction = model(input_sample)
        loss = loss_object(input_label, prediction)

    # Get the gradients of the loss with respect to the input
    gradient = tape.gradient(loss, input_sample)
    # Get the sign of the gradients
    signed_grad = tf.sign(gradient)
    return signed_grad

# Get the adversarial pattern
perturbations = create_adversarial_pattern(malware_sample, malware_label, model)

# Create the adversarial example by adding the perturbation
epsilon = 0.1 # The strength of the perturbation
adversarial_sample = malware_sample + epsilon * perturbations
# Clip the values to be in the valid range (e.g., 0 to 1 for normalized features)
adversarial_sample = tf.clip_by_value(adversarial_sample, 0, 1)

# Check the model's prediction on the adversarial sample
adversarial_prediction = model(adversarial_sample)
print(f"Adversarial prediction (should be close to 0): {adversarial_prediction.numpy()[0][0]}")
```

### Part 3: Visualizing the Perturbation

**Objective:** Visualize the difference between the original and the adversarial sample.

**Step 1: Add Visualization Code**

```python
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Original Sample")
plt.imshow(malware_sample.numpy().reshape(47, 50), cmap="gray") # Reshape for visualization
plt.subplot(1, 2, 2)
plt.title("Adversarial Sample")
plt.imshow(adversarial_sample.numpy().reshape(47, 50), cmap="gray")
plt.show()
```

### Deliverables

1.  **Python Script:** Submit your complete `evasion_attack.py` script.
2.  **Lab Report:** A 2-3 page report that includes:
    *   An explanation of the FGSM attack and how it works.
    *   The initial and adversarial predictions from your script.
    *   The visualization of the original vs. adversarial sample.
    *   A discussion on the implications of evasion attacks for AI-based security products and potential defense strategies.

### Grading Rubric

| Criterion | Points | Description |
| :--- | :--- | :--- |
| Model and Data Loading | 20 | Correctly loads the pre-trained model and sample data. |
| FGSM Implementation | 40 | Correctly implements the FGSM algorithm to generate perturbations. |
| Adversarial Example Generation | 20 | Successfully creates an adversarial example that fools the classifier. |
| Visualization and Report | 20 | Clear visualization and a well-written report with insightful analysis. |
| **Total** | **100** | |
