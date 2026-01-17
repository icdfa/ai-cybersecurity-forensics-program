#!/usr/bin/env python3
"""
Lab 9: Data Poisoning Attack on Machine Learning Models
This script implements various data poisoning attack techniques to compromise ML model training.

Author: Manus AI
Date: January 2026
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import argparse
import json
import matplotlib.pyplot as plt
import os

class DataPoisoner:
    """Implements various data poisoning attack techniques."""
    
    def __init__(self, attack_type='label_flip', poison_rate=0.1):
        """
        Initialize the data poisoner.
        
        Args:
            attack_type: Type of poisoning attack ('label_flip', 'feature_manipulation', 'backdoor')
            poison_rate: Percentage of training data to poison (0-1)
        """
        self.attack_type = attack_type
        self.poison_rate = poison_rate
        self.poisoned_indices = []
    
    def label_flip_attack(self, X_train, y_train, target_class=1):
        """
        Perform label flipping attack by changing labels of target class samples.
        
        Args:
            X_train: Training features
            y_train: Training labels
            target_class: Class to target for label flipping
        
        Returns:
            Poisoned training data (X_train, y_train_poisoned)
        """
        print(f"[*] Performing label flip attack on class {target_class}...")
        
        y_train_poisoned = y_train.copy()
        
        # Find indices of target class
        target_indices = np.where(y_train == target_class)[0]
        
        # Calculate number of samples to poison
        num_poison = int(len(target_indices) * self.poison_rate)
        
        # Randomly select samples to poison
        self.poisoned_indices = np.random.choice(target_indices, size=num_poison, replace=False)
        
        # Flip labels
        y_train_poisoned[self.poisoned_indices] = 1 - target_class
        
        print(f"[+] Poisoned {num_poison} samples ({self.poison_rate*100:.1f}% of class {target_class})")
        
        return X_train, y_train_poisoned
    
    def feature_manipulation_attack(self, X_train, y_train, target_class=1, perturbation_size=0.5):
        """
        Perform feature manipulation attack by modifying features of target class.
        
        Args:
            X_train: Training features
            y_train: Training labels
            target_class: Class to target
            perturbation_size: Magnitude of feature perturbation
        
        Returns:
            Poisoned training data (X_train_poisoned, y_train)
        """
        print(f"[*] Performing feature manipulation attack on class {target_class}...")
        
        X_train_poisoned = X_train.copy()
        
        # Find indices of target class
        target_indices = np.where(y_train == target_class)[0]
        
        # Calculate number of samples to poison
        num_poison = int(len(target_indices) * self.poison_rate)
        
        # Randomly select samples to poison
        self.poisoned_indices = np.random.choice(target_indices, size=num_poison, replace=False)
        
        # Add noise to features
        for idx in self.poisoned_indices:
            noise = perturbation_size * np.random.randn(X_train.shape[1])
            X_train_poisoned[idx] += noise
            X_train_poisoned[idx] = np.clip(X_train_poisoned[idx], 0, None)
        
        print(f"[+] Poisoned {num_poison} samples ({self.poison_rate*100:.1f}% of class {target_class})")
        
        return X_train_poisoned, y_train
    
    def backdoor_attack(self, X_train, y_train, trigger_pattern, target_class=1, backdoor_class=0):
        """
        Perform backdoor attack by injecting trigger pattern into samples.
        
        Args:
            X_train: Training features
            y_train: Training labels
            trigger_pattern: Pattern to inject as backdoor trigger
            target_class: Class to inject backdoor into
            backdoor_class: Class to misclassify to when trigger is present
        
        Returns:
            Poisoned training data (X_train_poisoned, y_train_poisoned)
        """
        print(f"[*] Performing backdoor attack...")
        
        X_train_poisoned = X_train.copy()
        y_train_poisoned = y_train.copy()
        
        # Find indices of target class
        target_indices = np.where(y_train == target_class)[0]
        
        # Calculate number of samples to poison
        num_poison = int(len(target_indices) * self.poison_rate)
        
        # Randomly select samples to poison
        self.poisoned_indices = np.random.choice(target_indices, size=num_poison, replace=False)
        
        # Inject trigger pattern and change label
        for idx in self.poisoned_indices:
            # Add trigger pattern to first few features
            trigger_size = min(len(trigger_pattern), X_train.shape[1])
            X_train_poisoned[idx, :trigger_size] = trigger_pattern[:trigger_size]
            y_train_poisoned[idx] = backdoor_class
        
        print(f"[+] Injected backdoor into {num_poison} samples ({self.poison_rate*100:.1f}% of class {target_class})")
        
        return X_train_poisoned, y_train_poisoned
    
    def poison_data(self, X_train, y_train, **kwargs):
        """
        Apply the specified poisoning attack.
        
        Args:
            X_train: Training features
            y_train: Training labels
            **kwargs: Additional arguments for specific attack types
        
        Returns:
            Poisoned training data (X_train_poisoned, y_train_poisoned)
        """
        if self.attack_type == 'label_flip':
            return self.label_flip_attack(X_train, y_train, **kwargs)
        elif self.attack_type == 'feature_manipulation':
            return self.feature_manipulation_attack(X_train, y_train, **kwargs)
        elif self.attack_type == 'backdoor':
            return self.backdoor_attack(X_train, y_train, **kwargs)
        else:
            raise ValueError(f"Unknown attack type: {self.attack_type}")


class PoisoningEvaluator:
    """Evaluates the impact of data poisoning attacks."""
    
    def __init__(self):
        """Initialize the evaluator."""
        self.results = {}
    
    def evaluate_model(self, model, X_test, y_test, model_name="Model"):
        """
        Evaluate a trained model on test data.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            model_name: Name for identification
        
        Returns:
            Dictionary of metrics
        """
        y_pred = model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_test, y_pred, average='weighted', zero_division=0)
        }
        
        return metrics
    
    def compare_models(self, clean_model, poisoned_model, X_test, y_test):
        """
        Compare clean and poisoned models.
        
        Args:
            clean_model: Model trained on clean data
            poisoned_model: Model trained on poisoned data
            X_test: Test features
            y_test: Test labels
        
        Returns:
            Comparison results
        """
        print("\n[*] Evaluating models...")
        
        clean_metrics = self.evaluate_model(clean_model, X_test, y_test, "Clean")
        poisoned_metrics = self.evaluate_model(poisoned_model, X_test, y_test, "Poisoned")
        
        print("\n=== Clean Model Performance ===")
        for metric, value in clean_metrics.items():
            print(f"  {metric.capitalize()}: {value:.4f}")
        
        print("\n=== Poisoned Model Performance ===")
        for metric, value in poisoned_metrics.items():
            print(f"  {metric.capitalize()}: {value:.4f}")
        
        print("\n=== Performance Degradation ===")
        for metric in clean_metrics.keys():
            degradation = clean_metrics[metric] - poisoned_metrics[metric]
            degradation_pct = (degradation / clean_metrics[metric]) * 100 if clean_metrics[metric] > 0 else 0
            print(f"  {metric.capitalize()}: {degradation:.4f} ({degradation_pct:.2f}%)")
        
        return {
            'clean_metrics': clean_metrics,
            'poisoned_metrics': poisoned_metrics
        }
    
    def test_backdoor(self, model, X_test, y_test, trigger_pattern, target_class=1):
        """
        Test backdoor attack success rate.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            trigger_pattern: Backdoor trigger pattern
            target_class: Class to test backdoor on
        
        Returns:
            Backdoor success rate
        """
        print("\n[*] Testing backdoor attack...")
        
        # Find samples of target class
        target_indices = np.where(y_test == target_class)[0]
        
        if len(target_indices) == 0:
            print("[!] No samples of target class found in test set")
            return 0.0
        
        # Create backdoored versions
        X_backdoored = X_test[target_indices].copy()
        trigger_size = min(len(trigger_pattern), X_test.shape[1])
        X_backdoored[:, :trigger_size] = trigger_pattern[:trigger_size]
        
        # Predict on backdoored samples
        y_pred_backdoor = model.predict(X_backdoored)
        
        # Calculate success rate (samples misclassified to class 0)
        success_rate = np.mean(y_pred_backdoor == 0)
        
        print(f"[+] Backdoor success rate: {success_rate:.2%}")
        print(f"    ({int(success_rate * len(target_indices))} out of {len(target_indices)} samples misclassified)")
        
        return success_rate


def load_dataset(dataset_path):
    """Load the dataset."""
    print(f"[*] Loading dataset from {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    X = df.drop('label', axis=1).values
    y = df['label'].values
    
    print(f"[+] Loaded {len(X)} samples")
    print(f"    - Class 0: {sum(y == 0)}")
    print(f"    - Class 1: {sum(y == 1)}")
    
    return X, y


def visualize_results(results, output_path='poisoning_comparison.png'):
    """Visualize the impact of poisoning attacks."""
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    clean_values = [results['clean_metrics'][m] for m in metrics]
    poisoned_values = [results['poisoned_metrics'][m] for m in metrics]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, clean_values, width, label='Clean Model', color='green', alpha=0.7)
    ax.bar(x + width/2, poisoned_values, width, label='Poisoned Model', color='red', alpha=0.7)
    
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Score')
    ax.set_title('Impact of Data Poisoning Attack on Model Performance')
    ax.set_xticks(x)
    ax.set_xticklabels([m.capitalize() for m in metrics])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"[+] Visualization saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Data Poisoning Attack Lab - Lab 9")
    parser.add_argument('--dataset', default='../data/malware_dataset.csv',
                       help='Path to dataset')
    parser.add_argument('--attack-type', choices=['label_flip', 'feature_manipulation', 'backdoor'],
                       default='label_flip', help='Type of poisoning attack')
    parser.add_argument('--poison-rate', type=float, default=0.1,
                       help='Percentage of data to poison (0-1)')
    parser.add_argument('--model-type', choices=['rf', 'lr'], default='rf',
                       help='Model type (rf=RandomForest, lr=LogisticRegression)')
    parser.add_argument('--output', default='poisoning_results.json',
                       help='Path to save results')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs('results', exist_ok=True)
    os.makedirs('../data', exist_ok=True)
    
    # Load dataset
    X, y = load_dataset(args.dataset)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"\n[*] Training set: {len(X_train)} samples")
    print(f"[*] Test set: {len(X_test)} samples")
    
    # Initialize models
    if args.model_type == 'rf':
        clean_model = RandomForestClassifier(n_estimators=100, random_state=42)
        poisoned_model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        clean_model = LogisticRegression(random_state=42, max_iter=1000)
        poisoned_model = LogisticRegression(random_state=42, max_iter=1000)
    
    # Train clean model
    print("\n[*] Training clean model...")
    clean_model.fit(X_train, y_train)
    print("[+] Clean model training complete")
    
    # Poison training data
    poisoner = DataPoisoner(attack_type=args.attack_type, poison_rate=args.poison_rate)
    
    if args.attack_type == 'backdoor':
        # Create trigger pattern for backdoor attack
        trigger_pattern = np.ones(5) * 999  # Distinctive pattern
        X_train_poisoned, y_train_poisoned = poisoner.poison_data(
            X_train, y_train, trigger_pattern=trigger_pattern
        )
    else:
        X_train_poisoned, y_train_poisoned = poisoner.poison_data(X_train, y_train)
    
    # Train poisoned model
    print("\n[*] Training poisoned model...")
    poisoned_model.fit(X_train_poisoned, y_train_poisoned)
    print("[+] Poisoned model training complete")
    
    # Evaluate models
    evaluator = PoisoningEvaluator()
    comparison_results = evaluator.compare_models(clean_model, poisoned_model, X_test, y_test)
    
    # Test backdoor if applicable
    backdoor_success = 0.0
    if args.attack_type == 'backdoor':
        backdoor_success = evaluator.test_backdoor(
            poisoned_model, X_test, y_test, trigger_pattern
        )
    
    # Visualize results
    visualize_results(comparison_results, 'results/poisoning_comparison.png')
    
    # Save results
    results_summary = {
        'attack_type': args.attack_type,
        'poison_rate': args.poison_rate,
        'model_type': args.model_type,
        'num_poisoned_samples': len(poisoner.poisoned_indices),
        'clean_metrics': comparison_results['clean_metrics'],
        'poisoned_metrics': comparison_results['poisoned_metrics'],
        'backdoor_success_rate': backdoor_success
    }
    
    with open(args.output, 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"\n[+] Results saved to {args.output}")
    print("\n=== Attack Summary ===")
    print(f"Attack Type: {args.attack_type}")
    print(f"Poison Rate: {args.poison_rate*100:.1f}%")
    print(f"Poisoned Samples: {len(poisoner.poisoned_indices)}")
    if args.attack_type == 'backdoor':
        print(f"Backdoor Success Rate: {backdoor_success:.2%}")


if __name__ == "__main__":
    main()
