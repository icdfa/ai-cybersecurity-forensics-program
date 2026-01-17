#!/usr/bin/env python3
"""
Lab 8: Bypassing a Malware Classifier with Evasion Attacks
This script implements various evasion attack techniques against ML-based malware classifiers.

Author: Manus AI
Date: January 2026
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import argparse
import json
import pickle
import os

class MalwareClassifier:
    """A simple malware classifier for demonstration purposes."""
    
    def __init__(self, model_path=None):
        """Initialize the classifier."""
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.is_trained = False
    
    def train(self, X_train, y_train):
        """Train the malware classifier."""
        print("[*] Training malware classifier...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("[+] Training complete.")
    
    def predict(self, X):
        """Predict whether samples are malware."""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction.")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities."""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction.")
        return self.model.predict_proba(X)
    
    def save_model(self, path):
        """Save the trained model."""
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"[+] Model saved to {path}")
    
    def load_model(self, path):
        """Load a trained model."""
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True
        print(f"[+] Model loaded from {path}")


class EvasionAttacker:
    """Implements various evasion attack techniques."""
    
    def __init__(self, classifier):
        """Initialize the attacker with a target classifier."""
        self.classifier = classifier
        self.attack_history = []
    
    def feature_manipulation_attack(self, malware_sample, feature_indices, perturbation_size=0.1):
        """
        Perform feature manipulation attack by modifying specific features.
        
        Args:
            malware_sample: Original malware sample (numpy array)
            feature_indices: List of feature indices to manipulate
            perturbation_size: Size of perturbation to apply
        
        Returns:
            Adversarial sample
        """
        print("[*] Performing feature manipulation attack...")
        adversarial_sample = malware_sample.copy()
        
        for idx in feature_indices:
            # Add small perturbation to feature
            adversarial_sample[idx] += perturbation_size * np.random.randn()
            # Ensure feature stays in valid range
            adversarial_sample[idx] = np.clip(adversarial_sample[idx], 0, None)
        
        return adversarial_sample
    
    def gradient_based_attack(self, malware_sample, epsilon=0.1, iterations=10):
        """
        Perform gradient-based evasion attack (simplified FGSM-like approach).
        
        Args:
            malware_sample: Original malware sample
            epsilon: Perturbation magnitude
            iterations: Number of attack iterations
        
        Returns:
            Adversarial sample
        """
        print("[*] Performing gradient-based attack...")
        adversarial_sample = malware_sample.copy()
        
        for i in range(iterations):
            # Get current prediction
            pred_proba = self.classifier.predict_proba(adversarial_sample.reshape(1, -1))[0]
            
            # If already misclassified as benign, stop
            if pred_proba[0] > 0.5:  # Assuming class 0 is benign
                print(f"[+] Successfully evaded detection at iteration {i+1}")
                break
            
            # Simulate gradient by random perturbation in direction that reduces malware probability
            perturbation = epsilon * np.random.randn(len(adversarial_sample))
            adversarial_sample += perturbation
            adversarial_sample = np.clip(adversarial_sample, 0, None)
        
        return adversarial_sample
    
    def mimicry_attack(self, malware_sample, benign_samples, blend_ratio=0.3):
        """
        Perform mimicry attack by blending malware features with benign samples.
        
        Args:
            malware_sample: Original malware sample
            benign_samples: Array of benign samples to mimic
            blend_ratio: Ratio of benign features to blend (0-1)
        
        Returns:
            Adversarial sample
        """
        print("[*] Performing mimicry attack...")
        
        # Select a random benign sample to mimic
        benign_sample = benign_samples[np.random.randint(len(benign_samples))]
        
        # Blend malware with benign features
        adversarial_sample = (1 - blend_ratio) * malware_sample + blend_ratio * benign_sample
        
        return adversarial_sample
    
    def evaluate_attack(self, original_sample, adversarial_sample, original_label):
        """
        Evaluate the success of an evasion attack.
        
        Args:
            original_sample: Original malware sample
            adversarial_sample: Adversarial sample after attack
            original_label: True label (1 for malware)
        
        Returns:
            Dictionary with attack results
        """
        # Get predictions
        original_pred = self.classifier.predict(original_sample.reshape(1, -1))[0]
        adversarial_pred = self.classifier.predict(adversarial_sample.reshape(1, -1))[0]
        
        # Get probabilities
        original_proba = self.classifier.predict_proba(original_sample.reshape(1, -1))[0]
        adversarial_proba = self.classifier.predict_proba(adversarial_sample.reshape(1, -1))[0]
        
        # Calculate perturbation magnitude
        perturbation = np.linalg.norm(adversarial_sample - original_sample)
        
        # Determine if attack was successful
        attack_success = (original_pred == 1 and adversarial_pred == 0)
        
        results = {
            'original_prediction': int(original_pred),
            'adversarial_prediction': int(adversarial_pred),
            'original_malware_probability': float(original_proba[1]),
            'adversarial_malware_probability': float(adversarial_proba[1]),
            'perturbation_magnitude': float(perturbation),
            'attack_success': bool(attack_success)
        }
        
        self.attack_history.append(results)
        
        return results


def load_dataset(dataset_path):
    """Load the malware dataset."""
    print(f"[*] Loading dataset from {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    # Separate features and labels
    X = df.drop('label', axis=1).values
    y = df['label'].values
    
    print(f"[+] Loaded {len(X)} samples")
    print(f"    - Malware samples: {sum(y == 1)}")
    print(f"    - Benign samples: {sum(y == 0)}")
    
    return X, y


def main():
    parser = argparse.ArgumentParser(description="Evasion Attack Lab - Lab 8")
    parser.add_argument('--dataset', default='../data/malware_dataset.csv', 
                       help='Path to malware dataset')
    parser.add_argument('--attack-type', choices=['feature', 'gradient', 'mimicry', 'all'],
                       default='all', help='Type of evasion attack to perform')
    parser.add_argument('--model-path', default='models/malware_classifier.pkl',
                       help='Path to save/load trained model')
    parser.add_argument('--output', default='attack_results.json',
                       help='Path to save attack results')
    
    args = parser.parse_args()
    
    # Create directories if they don't exist
    os.makedirs('models', exist_ok=True)
    os.makedirs('../data', exist_ok=True)
    
    # Load dataset
    X, y = load_dataset(args.dataset)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Train classifier
    classifier = MalwareClassifier()
    classifier.train(X_train, y_train)
    
    # Evaluate baseline performance
    y_pred = classifier.predict(X_test)
    baseline_accuracy = accuracy_score(y_test, y_pred)
    print(f"\n[+] Baseline classifier accuracy: {baseline_accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Benign', 'Malware']))
    
    # Save model
    classifier.save_model(args.model_path)
    
    # Initialize attacker
    attacker = EvasionAttacker(classifier)
    
    # Select malware samples for attack
    malware_indices = np.where(y_test == 1)[0]
    benign_samples = X_test[y_test == 0]
    
    print(f"\n[*] Performing evasion attacks on {len(malware_indices)} malware samples...")
    
    attack_results = []
    
    for idx in malware_indices[:10]:  # Attack first 10 malware samples
        original_sample = X_test[idx]
        
        print(f"\n--- Attacking Sample {idx} ---")
        
        if args.attack_type in ['feature', 'all']:
            # Feature manipulation attack
            feature_indices = np.random.choice(X.shape[1], size=5, replace=False)
            adv_sample = attacker.feature_manipulation_attack(original_sample, feature_indices)
            results = attacker.evaluate_attack(original_sample, adv_sample, 1)
            results['attack_type'] = 'feature_manipulation'
            attack_results.append(results)
            print(f"  Feature Manipulation: {'SUCCESS' if results['attack_success'] else 'FAILED'}")
            print(f"    Malware prob: {results['original_malware_probability']:.4f} -> {results['adversarial_malware_probability']:.4f}")
        
        if args.attack_type in ['gradient', 'all']:
            # Gradient-based attack
            adv_sample = attacker.gradient_based_attack(original_sample)
            results = attacker.evaluate_attack(original_sample, adv_sample, 1)
            results['attack_type'] = 'gradient_based'
            attack_results.append(results)
            print(f"  Gradient-Based: {'SUCCESS' if results['attack_success'] else 'FAILED'}")
            print(f"    Malware prob: {results['original_malware_probability']:.4f} -> {results['adversarial_malware_probability']:.4f}")
        
        if args.attack_type in ['mimicry', 'all']:
            # Mimicry attack
            adv_sample = attacker.mimicry_attack(original_sample, benign_samples)
            results = attacker.evaluate_attack(original_sample, adv_sample, 1)
            results['attack_type'] = 'mimicry'
            attack_results.append(results)
            print(f"  Mimicry: {'SUCCESS' if results['attack_success'] else 'FAILED'}")
            print(f"    Malware prob: {results['original_malware_probability']:.4f} -> {results['adversarial_malware_probability']:.4f}")
    
    # Calculate overall attack success rate
    total_attacks = len(attack_results)
    successful_attacks = sum(1 for r in attack_results if r['attack_success'])
    success_rate = successful_attacks / total_attacks if total_attacks > 0 else 0
    
    print(f"\n=== Attack Summary ===")
    print(f"Total attacks: {total_attacks}")
    print(f"Successful attacks: {successful_attacks}")
    print(f"Success rate: {success_rate:.2%}")
    
    # Save results
    summary = {
        'baseline_accuracy': baseline_accuracy,
        'total_attacks': total_attacks,
        'successful_attacks': successful_attacks,
        'success_rate': success_rate,
        'attack_details': attack_results
    }
    
    with open(args.output, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n[+] Results saved to {args.output}")


if __name__ == "__main__":
    main()
