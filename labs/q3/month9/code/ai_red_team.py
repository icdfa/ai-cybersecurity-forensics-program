#!/usr/bin/env python3
"""
Lab 11: AI Red Teaming Framework
This script implements a comprehensive red teaming framework for testing AI system security.

Author: Manus AI
Date: January 2026
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import argparse
import json
import os
from datetime import datetime
from enum import Enum

class VulnerabilityCategory(Enum):
    """Categories of AI vulnerabilities"""
    ADVERSARIAL_ROBUSTNESS = "Adversarial Robustness"
    DATA_POISONING = "Data Poisoning"
    MODEL_EXTRACTION = "Model Extraction"
    PRIVACY_LEAKAGE = "Privacy Leakage"
    FAIRNESS_BIAS = "Fairness and Bias"
    PROMPT_INJECTION = "Prompt Injection"
    BACKDOOR = "Backdoor Attack"

class SeverityLevel(Enum):
    """Severity levels for vulnerabilities"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Informational"

class AIRedTeamFramework:
    """
    Comprehensive red teaming framework for AI systems.
    """
    
    def __init__(self, target_model, model_name="Target AI System"):
        """
        Initialize the red team framework.
        
        Args:
            target_model: The AI model to test
            model_name: Name of the target system
        """
        self.target_model = target_model
        self.model_name = model_name
        self.vulnerabilities = []
        self.test_results = []
        self.report_data = {
            'model_name': model_name,
            'test_date': datetime.now().isoformat(),
            'vulnerabilities': [],
            'summary': {}
        }
    
    def test_adversarial_robustness(self, X_test, y_test, epsilon=0.1):
        """
        Test the model's robustness against adversarial examples.
        
        Args:
            X_test: Test data
            y_test: Test labels
            epsilon: Perturbation magnitude
        
        Returns:
            Test results dictionary
        """
        print("\n[*] Testing Adversarial Robustness...")
        
        # Generate adversarial examples
        X_adv = X_test.copy()
        for i in range(len(X_adv)):
            perturbation = epsilon * np.random.randn(X_adv.shape[1])
            X_adv[i] += perturbation
        
        # Test original vs adversarial
        original_pred = self.target_model.predict(X_test)
        adversarial_pred = self.target_model.predict(X_adv)
        
        # Calculate success rate
        misclassified = np.sum(original_pred != adversarial_pred)
        success_rate = misclassified / len(X_test)
        
        # Determine severity
        if success_rate > 0.5:
            severity = SeverityLevel.CRITICAL
        elif success_rate > 0.3:
            severity = SeverityLevel.HIGH
        elif success_rate > 0.1:
            severity = SeverityLevel.MEDIUM
        else:
            severity = SeverityLevel.LOW
        
        result = {
            'category': VulnerabilityCategory.ADVERSARIAL_ROBUSTNESS.value,
            'test_name': 'Adversarial Example Attack',
            'success_rate': float(success_rate),
            'samples_tested': len(X_test),
            'samples_misclassified': int(misclassified),
            'severity': severity.value,
            'description': f'Model misclassified {misclassified}/{len(X_test)} samples under adversarial perturbation',
            'recommendation': 'Implement adversarial training or input validation'
        }
        
        self.test_results.append(result)
        if severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH, SeverityLevel.MEDIUM]:
            self.vulnerabilities.append(result)
        
        print(f"[+] Adversarial Robustness Test Complete")
        print(f"    Success Rate: {success_rate:.2%}")
        print(f"    Severity: {severity.value}")
        
        return result
    
    def test_model_confidence(self, X_test, y_test):
        """
        Test if the model provides appropriate confidence levels.
        
        Args:
            X_test: Test data
            y_test: Test labels
        
        Returns:
            Test results dictionary
        """
        print("\n[*] Testing Model Confidence Calibration...")
        
        if not hasattr(self.target_model, 'predict_proba'):
            print("[!] Model does not support probability predictions")
            return None
        
        predictions = self.target_model.predict(X_test)
        probabilities = self.target_model.predict_proba(X_test)
        
        # Find high-confidence errors
        max_probs = np.max(probabilities, axis=1)
        errors = predictions != y_test
        high_conf_errors = np.sum((max_probs > 0.9) & errors)
        
        # Calculate overconfidence rate
        overconfidence_rate = high_conf_errors / len(X_test)
        
        # Determine severity
        if overconfidence_rate > 0.1:
            severity = SeverityLevel.HIGH
        elif overconfidence_rate > 0.05:
            severity = SeverityLevel.MEDIUM
        else:
            severity = SeverityLevel.LOW
        
        result = {
            'category': 'Model Confidence',
            'test_name': 'Confidence Calibration Test',
            'overconfidence_rate': float(overconfidence_rate),
            'high_confidence_errors': int(high_conf_errors),
            'severity': severity.value,
            'description': f'Model showed high confidence ({high_conf_errors} cases) in incorrect predictions',
            'recommendation': 'Implement confidence calibration or uncertainty quantification'
        }
        
        self.test_results.append(result)
        if severity in [SeverityLevel.HIGH, SeverityLevel.MEDIUM]:
            self.vulnerabilities.append(result)
        
        print(f"[+] Confidence Test Complete")
        print(f"    Overconfidence Rate: {overconfidence_rate:.2%}")
        print(f"    Severity: {severity.value}")
        
        return result
    
    def test_feature_importance_leakage(self, X_test):
        """
        Test if feature importance reveals sensitive information.
        
        Args:
            X_test: Test data
        
        Returns:
            Test results dictionary
        """
        print("\n[*] Testing Feature Importance Leakage...")
        
        if not hasattr(self.target_model, 'feature_importances_'):
            print("[!] Model does not support feature importance extraction")
            return None
        
        feature_importance = self.target_model.feature_importances_
        
        # Check if any features are overwhelmingly important
        max_importance = np.max(feature_importance)
        top_feature_idx = np.argmax(feature_importance)
        
        # Determine if this is a vulnerability
        if max_importance > 0.5:
            severity = SeverityLevel.MEDIUM
            is_vulnerability = True
        elif max_importance > 0.3:
            severity = SeverityLevel.LOW
            is_vulnerability = True
        else:
            severity = SeverityLevel.INFO
            is_vulnerability = False
        
        result = {
            'category': VulnerabilityCategory.PRIVACY_LEAKAGE.value,
            'test_name': 'Feature Importance Analysis',
            'max_feature_importance': float(max_importance),
            'dominant_feature_index': int(top_feature_idx),
            'severity': severity.value,
            'description': f'Feature {top_feature_idx} has importance {max_importance:.2%}, potentially revealing sensitive patterns',
            'recommendation': 'Consider feature engineering or differential privacy techniques'
        }
        
        self.test_results.append(result)
        if is_vulnerability:
            self.vulnerabilities.append(result)
        
        print(f"[+] Feature Importance Test Complete")
        print(f"    Max Feature Importance: {max_importance:.2%}")
        print(f"    Severity: {severity.value}")
        
        return result
    
    def test_input_validation(self, X_test):
        """
        Test if the model properly validates inputs.
        
        Args:
            X_test: Test data
        
        Returns:
            Test results dictionary
        """
        print("\n[*] Testing Input Validation...")
        
        # Test with extreme values
        X_extreme = X_test.copy()
        X_extreme[0] = np.ones(X_test.shape[1]) * 1e6  # Very large values
        X_extreme[1] = np.ones(X_test.shape[1]) * -1e6  # Very small values
        X_extreme[2] = np.nan  # NaN values
        
        validation_passed = True
        error_message = ""
        
        try:
            predictions = self.target_model.predict(X_extreme)
            # If it doesn't crash, check if predictions are reasonable
            if np.any(np.isnan(predictions)) or np.any(np.isinf(predictions)):
                validation_passed = False
                error_message = "Model produced invalid outputs (NaN or Inf)"
        except Exception as e:
            validation_passed = False
            error_message = f"Model crashed on invalid input: {str(e)}"
        
        if not validation_passed:
            severity = SeverityLevel.HIGH
        else:
            severity = SeverityLevel.INFO
        
        result = {
            'category': 'Input Validation',
            'test_name': 'Input Boundary Test',
            'validation_passed': validation_passed,
            'severity': severity.value,
            'description': error_message if not validation_passed else 'Model handles edge cases appropriately',
            'recommendation': 'Implement robust input validation and sanitization' if not validation_passed else 'Continue monitoring'
        }
        
        self.test_results.append(result)
        if not validation_passed:
            self.vulnerabilities.append(result)
        
        print(f"[+] Input Validation Test Complete")
        print(f"    Validation Passed: {validation_passed}")
        print(f"    Severity: {severity.value}")
        
        return result
    
    def test_model_bias(self, X_test, y_test, sensitive_feature_idx=0):
        """
        Test for potential bias in model predictions.
        
        Args:
            X_test: Test data
            y_test: Test labels
            sensitive_feature_idx: Index of sensitive feature to test
        
        Returns:
            Test results dictionary
        """
        print("\n[*] Testing Model Bias...")
        
        # Split data based on sensitive feature
        sensitive_values = X_test[:, sensitive_feature_idx]
        median_value = np.median(sensitive_values)
        
        group_a = X_test[sensitive_values <= median_value]
        group_b = X_test[sensitive_values > median_value]
        
        y_a = y_test[sensitive_values <= median_value]
        y_b = y_test[sensitive_values > median_value]
        
        # Calculate accuracy for each group
        pred_a = self.target_model.predict(group_a)
        pred_b = self.target_model.predict(group_b)
        
        acc_a = np.mean(pred_a == y_a)
        acc_b = np.mean(pred_b == y_b)
        
        # Calculate disparity
        disparity = abs(acc_a - acc_b)
        
        # Determine severity
        if disparity > 0.2:
            severity = SeverityLevel.HIGH
        elif disparity > 0.1:
            severity = SeverityLevel.MEDIUM
        elif disparity > 0.05:
            severity = SeverityLevel.LOW
        else:
            severity = SeverityLevel.INFO
        
        result = {
            'category': VulnerabilityCategory.FAIRNESS_BIAS.value,
            'test_name': 'Bias Detection Test',
            'group_a_accuracy': float(acc_a),
            'group_b_accuracy': float(acc_b),
            'disparity': float(disparity),
            'severity': severity.value,
            'description': f'Performance disparity of {disparity:.2%} detected between groups',
            'recommendation': 'Investigate and mitigate bias through fairness-aware training'
        }
        
        self.test_results.append(result)
        if severity in [SeverityLevel.HIGH, SeverityLevel.MEDIUM]:
            self.vulnerabilities.append(result)
        
        print(f"[+] Bias Test Complete")
        print(f"    Group A Accuracy: {acc_a:.2%}")
        print(f"    Group B Accuracy: {acc_b:.2%}")
        print(f"    Disparity: {disparity:.2%}")
        print(f"    Severity: {severity.value}")
        
        return result
    
    def run_full_assessment(self, X_test, y_test):
        """
        Run a comprehensive security assessment.
        
        Args:
            X_test: Test data
            y_test: Test labels
        
        Returns:
            Complete assessment results
        """
        print("=" * 60)
        print("AI Red Team Assessment")
        print(f"Target: {self.model_name}")
        print(f"Date: {self.report_data['test_date']}")
        print("=" * 60)
        
        # Run all tests
        self.test_adversarial_robustness(X_test, y_test)
        self.test_model_confidence(X_test, y_test)
        self.test_feature_importance_leakage(X_test)
        self.test_input_validation(X_test)
        self.test_model_bias(X_test, y_test)
        
        # Generate summary
        self.generate_summary()
        
        return self.report_data
    
    def generate_summary(self):
        """Generate assessment summary."""
        severity_counts = {
            SeverityLevel.CRITICAL.value: 0,
            SeverityLevel.HIGH.value: 0,
            SeverityLevel.MEDIUM.value: 0,
            SeverityLevel.LOW.value: 0,
            SeverityLevel.INFO.value: 0
        }
        
        for vuln in self.vulnerabilities:
            severity_counts[vuln['severity']] += 1
        
        self.report_data['summary'] = {
            'total_tests': len(self.test_results),
            'vulnerabilities_found': len(self.vulnerabilities),
            'severity_breakdown': severity_counts,
            'risk_score': self.calculate_risk_score()
        }
        
        self.report_data['vulnerabilities'] = self.vulnerabilities
        self.report_data['all_tests'] = self.test_results
    
    def calculate_risk_score(self):
        """
        Calculate overall risk score (0-100).
        
        Returns:
            Risk score
        """
        weights = {
            SeverityLevel.CRITICAL.value: 25,
            SeverityLevel.HIGH.value: 15,
            SeverityLevel.MEDIUM.value: 8,
            SeverityLevel.LOW.value: 3,
            SeverityLevel.INFO.value: 0
        }
        
        score = 0
        for vuln in self.vulnerabilities:
            score += weights.get(vuln['severity'], 0)
        
        return min(100, score)
    
    def save_report(self, output_path):
        """
        Save the assessment report.
        
        Args:
            output_path: Path to save the report
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        
        print(f"\n[+] Report saved to {output_path}")
    
    def print_summary(self):
        """Print assessment summary."""
        print("\n" + "=" * 60)
        print("ASSESSMENT SUMMARY")
        print("=" * 60)
        
        summary = self.report_data['summary']
        print(f"Total Tests Run: {summary['total_tests']}")
        print(f"Vulnerabilities Found: {summary['vulnerabilities_found']}")
        print(f"Risk Score: {summary['risk_score']}/100")
        
        print("\nSeverity Breakdown:")
        for severity, count in summary['severity_breakdown'].items():
            if count > 0:
                print(f"  {severity}: {count}")
        
        print("\n" + "=" * 60)


def load_target_model(model_path):
    """Load the target model for testing."""
    import pickle
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def main():
    parser = argparse.ArgumentParser(description="AI Red Team Framework - Lab 11")
    parser.add_argument('--model', default='../month9/models/deepfake_detector.pkl',
                       help='Path to target model')
    parser.add_argument('--dataset', default='../month9/data/deepfake_dataset.csv',
                       help='Path to test dataset')
    parser.add_argument('--output', default='results/red_team_report.json',
                       help='Path to save report')
    parser.add_argument('--model-name', default='Deepfake Detector',
                       help='Name of the target system')
    
    args = parser.parse_args()
    
    # Create directories
    os.makedirs('results', exist_ok=True)
    
    # Load target model
    print(f"[*] Loading target model from {args.model}")
    target_model = load_target_model(args.model)
    
    # Load test data
    print(f"[*] Loading test dataset from {args.dataset}")
    df = pd.read_csv(args.dataset)
    X = df.drop('label', axis=1).values
    y = df['label'].values
    
    # Use a subset for testing
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    print(f"[+] Loaded {len(X_test)} test samples")
    
    # Initialize red team framework
    red_team = AIRedTeamFramework(target_model, args.model_name)
    
    # Run full assessment
    results = red_team.run_full_assessment(X_test, y_test)
    
    # Save report
    red_team.save_report(args.output)
    
    # Print summary
    red_team.print_summary()


if __name__ == "__main__":
    main()
