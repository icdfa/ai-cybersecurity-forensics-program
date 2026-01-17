#!/usr/bin/env python3
"""
Lab 10: Deepfake Detection System
This script implements a deepfake detection system using machine learning and computer vision techniques.

Author: Manus AI
Date: January 2026
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import argparse
import json
import pickle
import os
from pathlib import Path

class DeepfakeDetector:
    """
    A deepfake detection system that analyzes media files for signs of manipulation.
    """
    
    def __init__(self, model_type='rf'):
        """
        Initialize the deepfake detector.
        
        Args:
            model_type: Type of classifier to use ('rf' for Random Forest)
        """
        self.model_type = model_type
        if model_type == 'rf':
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=20,
                min_samples_split=5,
                random_state=42
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        self.is_trained = False
        self.feature_names = None
    
    def extract_features(self, data):
        """
        Extract features from media data for deepfake detection.
        
        In a real implementation, this would extract features like:
        - Facial landmarks consistency
        - Blinking patterns
        - Lighting inconsistencies
        - Compression artifacts
        - Temporal coherence
        
        Args:
            data: Input data (for this lab, pre-extracted features)
        
        Returns:
            Feature array
        """
        # In this lab, we assume features are already extracted
        return data
    
    def train(self, X_train, y_train):
        """
        Train the deepfake detector.
        
        Args:
            X_train: Training features
            y_train: Training labels (0=real, 1=fake)
        """
        print("[*] Training deepfake detector...")
        print(f"    Training samples: {len(X_train)}")
        print(f"    Real samples: {sum(y_train == 0)}")
        print(f"    Fake samples: {sum(y_train == 1)}")
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        print("[+] Training complete.")
    
    def predict(self, X):
        """
        Predict whether media samples are deepfakes.
        
        Args:
            X: Feature array
        
        Returns:
            Predictions (0=real, 1=fake)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction.")
        
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Get prediction probabilities.
        
        Args:
            X: Feature array
        
        Returns:
            Probability array [P(real), P(fake)]
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction.")
        
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate the detector on test data.
        
        Args:
            X_test: Test features
            y_test: Test labels
        
        Returns:
            Dictionary of evaluation metrics
        """
        print("\n[*] Evaluating deepfake detector...")
        
        y_pred = self.predict(X_test)
        y_proba = self.predict_proba(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0)
        }
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        metrics['true_negatives'] = int(cm[0, 0])
        metrics['false_positives'] = int(cm[0, 1])
        metrics['false_negatives'] = int(cm[1, 0])
        metrics['true_positives'] = int(cm[1, 1])
        
        # Calculate false positive rate and false negative rate
        metrics['false_positive_rate'] = metrics['false_positives'] / (metrics['false_positives'] + metrics['true_negatives']) if (metrics['false_positives'] + metrics['true_negatives']) > 0 else 0
        metrics['false_negative_rate'] = metrics['false_negatives'] / (metrics['false_negatives'] + metrics['true_positives']) if (metrics['false_negatives'] + metrics['true_positives']) > 0 else 0
        
        print("\n=== Evaluation Results ===")
        print(f"Accuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1-Score:  {metrics['f1_score']:.4f}")
        print(f"\nConfusion Matrix:")
        print(f"                Predicted Real  Predicted Fake")
        print(f"Actual Real     {metrics['true_negatives']:14d}  {metrics['false_positives']:14d}")
        print(f"Actual Fake     {metrics['false_negatives']:14d}  {metrics['true_positives']:14d}")
        print(f"\nFalse Positive Rate: {metrics['false_positive_rate']:.4f}")
        print(f"False Negative Rate: {metrics['false_negative_rate']:.4f}")
        
        return metrics
    
    def get_feature_importance(self):
        """
        Get feature importance scores from the trained model.
        
        Returns:
            Array of feature importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance.")
        
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        else:
            return None
    
    def save_model(self, path):
        """
        Save the trained model.
        
        Args:
            path: Path to save the model
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"[+] Model saved to {path}")
    
    def load_model(self, path):
        """
        Load a trained model.
        
        Args:
            path: Path to the saved model
        """
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True
        print(f"[+] Model loaded from {path}")


class DeepfakeAnalyzer:
    """
    Analyzes deepfake detection results and provides insights.
    """
    
    def __init__(self, detector):
        """
        Initialize the analyzer.
        
        Args:
            detector: Trained DeepfakeDetector instance
        """
        self.detector = detector
    
    def analyze_sample(self, sample, label=None):
        """
        Analyze a single sample in detail.
        
        Args:
            sample: Feature array for the sample
            label: True label (optional)
        
        Returns:
            Analysis results dictionary
        """
        sample = sample.reshape(1, -1)
        prediction = self.detector.predict(sample)[0]
        probabilities = self.detector.predict_proba(sample)[0]
        
        analysis = {
            'prediction': 'Fake' if prediction == 1 else 'Real',
            'confidence': float(max(probabilities)),
            'real_probability': float(probabilities[0]),
            'fake_probability': float(probabilities[1])
        }
        
        if label is not None:
            analysis['true_label'] = 'Fake' if label == 1 else 'Real'
            analysis['correct'] = (prediction == label)
        
        return analysis
    
    def identify_suspicious_features(self, sample, top_n=5):
        """
        Identify the most suspicious features in a sample.
        
        Args:
            sample: Feature array
            top_n: Number of top features to return
        
        Returns:
            List of (feature_index, importance_score) tuples
        """
        feature_importance = self.detector.get_feature_importance()
        
        if feature_importance is None:
            return []
        
        # Get indices of top features
        top_indices = np.argsort(feature_importance)[-top_n:][::-1]
        
        suspicious_features = [
            (int(idx), float(feature_importance[idx]))
            for idx in top_indices
        ]
        
        return suspicious_features
    
    def batch_analyze(self, X_test, y_test):
        """
        Analyze multiple samples and generate statistics.
        
        Args:
            X_test: Test features
            y_test: Test labels
        
        Returns:
            Batch analysis results
        """
        print("\n[*] Performing batch analysis...")
        
        predictions = self.detector.predict(X_test)
        probabilities = self.detector.predict_proba(X_test)
        
        # Find high-confidence errors
        confidence = np.max(probabilities, axis=1)
        errors = predictions != y_test
        high_confidence_errors = np.where((errors) & (confidence > 0.9))[0]
        
        # Find low-confidence correct predictions
        correct = predictions == y_test
        low_confidence_correct = np.where((correct) & (confidence < 0.6))[0]
        
        results = {
            'total_samples': len(X_test),
            'high_confidence_errors': len(high_confidence_errors),
            'low_confidence_correct': len(low_confidence_correct),
            'average_confidence': float(np.mean(confidence)),
            'high_confidence_error_indices': high_confidence_errors.tolist()[:10],  # First 10
            'low_confidence_correct_indices': low_confidence_correct.tolist()[:10]   # First 10
        }
        
        print(f"[+] Batch analysis complete:")
        print(f"    Total samples: {results['total_samples']}")
        print(f"    High-confidence errors: {results['high_confidence_errors']}")
        print(f"    Low-confidence correct: {results['low_confidence_correct']}")
        print(f"    Average confidence: {results['average_confidence']:.4f}")
        
        return results


def load_dataset(dataset_path):
    """
    Load the deepfake dataset.
    
    Args:
        dataset_path: Path to the dataset CSV file
    
    Returns:
        Feature array and labels
    """
    print(f"[*] Loading dataset from {dataset_path}")
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    
    # Separate features and labels
    X = df.drop('label', axis=1).values
    y = df['label'].values
    
    print(f"[+] Loaded {len(X)} samples")
    print(f"    - Real samples: {sum(y == 0)}")
    print(f"    - Fake samples: {sum(y == 1)}")
    print(f"    - Features: {X.shape[1]}")
    
    return X, y


def main():
    parser = argparse.ArgumentParser(description="Deepfake Detection Lab - Lab 10")
    parser.add_argument('--dataset', default='data/deepfake_dataset.csv',
                       help='Path to deepfake dataset')
    parser.add_argument('--model-path', default='models/deepfake_detector.pkl',
                       help='Path to save/load trained model')
    parser.add_argument('--output', default='results/detection_results.json',
                       help='Path to save results')
    parser.add_argument('--analyze', action='store_true',
                       help='Perform detailed analysis on test samples')
    
    args = parser.parse_args()
    
    # Create directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Load dataset
    X, y = load_dataset(args.dataset)
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"\n[*] Dataset split:")
    print(f"    Training: {len(X_train)} samples")
    print(f"    Testing:  {len(X_test)} samples")
    
    # Initialize and train detector
    detector = DeepfakeDetector(model_type='rf')
    detector.train(X_train, y_train)
    
    # Evaluate detector
    metrics = detector.evaluate(X_test, y_test)
    
    # Save model
    detector.save_model(args.model_path)
    
    # Perform detailed analysis if requested
    if args.analyze:
        analyzer = DeepfakeAnalyzer(detector)
        
        # Analyze a few samples
        print("\n[*] Analyzing individual samples...")
        for i in range(min(5, len(X_test))):
            sample = X_test[i]
            label = y_test[i]
            analysis = analyzer.analyze_sample(sample, label)
            
            print(f"\n  Sample {i+1}:")
            print(f"    True Label:  {analysis['true_label']}")
            print(f"    Prediction:  {analysis['prediction']}")
            print(f"    Confidence:  {analysis['confidence']:.4f}")
            print(f"    Correct:     {analysis['correct']}")
        
        # Identify important features
        print("\n[*] Top 5 most important features for detection:")
        suspicious_features = analyzer.identify_suspicious_features(X_test[0])
        for idx, (feature_idx, importance) in enumerate(suspicious_features, 1):
            print(f"    {idx}. Feature {feature_idx}: {importance:.4f}")
        
        # Batch analysis
        batch_results = analyzer.batch_analyze(X_test, y_test)
        metrics['batch_analysis'] = batch_results
    
    # Save results
    results_summary = {
        'model_type': 'RandomForest',
        'dataset': args.dataset,
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'metrics': metrics
    }
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"\n[+] Results saved to {args.output}")
    print("\n=== Detection System Summary ===")
    print(f"Model: Random Forest")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"Precision: {metrics['precision']:.2%}")
    print(f"Recall: {metrics['recall']:.2%}")
    print(f"F1-Score: {metrics['f1_score']:.2%}")


if __name__ == "__main__":
    main()
