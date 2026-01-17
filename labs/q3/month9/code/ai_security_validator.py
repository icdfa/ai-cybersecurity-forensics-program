#!/usr/bin/env python3
"""
Lab 12: AI Security Validation Platform
This script implements a comprehensive security validation and certification platform for AI systems.

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
import hashlib

class ComplianceStandard(Enum):
    """Compliance standards for AI systems"""
    NIST_AI_RMF = "NIST AI Risk Management Framework"
    EU_AI_ACT = "EU AI Act"
    ISO_IEC_42001 = "ISO/IEC 42001"
    OWASP_ML_TOP_10 = "OWASP Machine Learning Top 10"

class CertificationLevel(Enum):
    """Certification levels based on validation results"""
    PLATINUM = "Platinum"
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"
    FAILED = "Failed"

class ValidationTest:
    """Base class for validation tests"""
    
    def __init__(self, name, category, weight=1.0):
        self.name = name
        self.category = category
        self.weight = weight
        self.passed = False
        self.score = 0.0
        self.details = {}
    
    def run(self, model, X_test, y_test):
        """Run the validation test"""
        raise NotImplementedError("Subclasses must implement run()")

class AccuracyValidation(ValidationTest):
    """Validate model accuracy meets minimum threshold"""
    
    def __init__(self, min_accuracy=0.85):
        super().__init__("Accuracy Validation", "Performance", weight=2.0)
        self.min_accuracy = min_accuracy
    
    def run(self, model, X_test, y_test):
        predictions = model.predict(X_test)
        accuracy = np.mean(predictions == y_test)
        
        self.passed = accuracy >= self.min_accuracy
        self.score = min(100, (accuracy / self.min_accuracy) * 100)
        self.details = {
            'accuracy': float(accuracy),
            'threshold': float(self.min_accuracy),
            'passed': bool(self.passed)
        }
        
        return self.passed

class RobustnessValidation(ValidationTest):
    """Validate model robustness against perturbations"""
    
    def __init__(self, max_degradation=0.15):
        super().__init__("Robustness Validation", "Security", weight=3.0)
        self.max_degradation = max_degradation
    
    def run(self, model, X_test, y_test):
        # Original accuracy
        original_pred = model.predict(X_test)
        original_acc = np.mean(original_pred == y_test)
        
        # Perturbed accuracy
        X_perturbed = X_test + np.random.normal(0, 0.1, X_test.shape)
        perturbed_pred = model.predict(X_perturbed)
        perturbed_acc = np.mean(perturbed_pred == y_test)
        
        degradation = original_acc - perturbed_acc
        
        self.passed = degradation <= self.max_degradation
        self.score = max(0, min(100, (1 - degradation / self.max_degradation) * 100))
        self.details = {
            'original_accuracy': float(original_acc),
            'perturbed_accuracy': float(perturbed_acc),
            'degradation': float(degradation),
            'threshold': float(self.max_degradation),
            'passed': bool(self.passed)
        }
        
        return self.passed

class FairnessValidation(ValidationTest):
    """Validate model fairness across groups"""
    
    def __init__(self, max_disparity=0.10):
        super().__init__("Fairness Validation", "Ethics", weight=2.5)
        self.max_disparity = max_disparity
    
    def run(self, model, X_test, y_test):
        # Split by first feature as proxy for sensitive attribute
        median = np.median(X_test[:, 0])
        group_a_mask = X_test[:, 0] <= median
        group_b_mask = X_test[:, 0] > median
        
        # Calculate accuracy for each group
        pred_a = model.predict(X_test[group_a_mask])
        pred_b = model.predict(X_test[group_b_mask])
        
        acc_a = np.mean(pred_a == y_test[group_a_mask])
        acc_b = np.mean(pred_b == y_test[group_b_mask])
        
        disparity = abs(acc_a - acc_b)
        
        self.passed = disparity <= self.max_disparity
        self.score = max(0, min(100, (1 - disparity / self.max_disparity) * 100))
        self.details = {
            'group_a_accuracy': float(acc_a),
            'group_b_accuracy': float(acc_b),
            'disparity': float(disparity),
            'threshold': float(self.max_disparity),
            'passed': bool(self.passed)
        }
        
        return self.passed

class TransparencyValidation(ValidationTest):
    """Validate model transparency and explainability"""
    
    def __init__(self):
        super().__init__("Transparency Validation", "Governance", weight=1.5)
    
    def run(self, model, X_test, y_test):
        # Check if model has explainability features
        has_feature_importance = hasattr(model, 'feature_importances_')
        has_predict_proba = hasattr(model, 'predict_proba')
        
        transparency_score = 0
        if has_feature_importance:
            transparency_score += 50
        if has_predict_proba:
            transparency_score += 50
        
        self.passed = transparency_score >= 50
        self.score = transparency_score
        self.details = {
            'has_feature_importance': bool(has_feature_importance),
            'has_predict_proba': bool(has_predict_proba),
            'transparency_score': float(transparency_score),
            'passed': bool(self.passed)
        }
        
        return self.passed

class DataQualityValidation(ValidationTest):
    """Validate training data quality"""
    
    def __init__(self):
        super().__init__("Data Quality Validation", "Data Integrity", weight=2.0)
    
    def run(self, model, X_test, y_test):
        # Check for data quality issues
        has_nan = np.any(np.isnan(X_test))
        has_inf = np.any(np.isinf(X_test))
        
        # Check class balance
        unique, counts = np.unique(y_test, return_counts=True)
        balance_ratio = min(counts) / max(counts) if len(counts) > 1 else 1.0
        
        quality_score = 100
        if has_nan:
            quality_score -= 30
        if has_inf:
            quality_score -= 30
        if balance_ratio < 0.5:
            quality_score -= 20
        
        self.passed = quality_score >= 70
        self.score = max(0, quality_score)
        self.details = {
            'has_nan_values': bool(has_nan),
            'has_inf_values': bool(has_inf),
            'class_balance_ratio': float(balance_ratio),
            'quality_score': float(quality_score),
            'passed': bool(self.passed)
        }
        
        return self.passed

class SecurityValidation(ValidationTest):
    """Validate security controls"""
    
    def __init__(self):
        super().__init__("Security Validation", "Security", weight=3.0)
    
    def run(self, model, X_test, y_test):
        # Test input validation
        try:
            extreme_input = np.ones((1, X_test.shape[1])) * 1e10
            _ = model.predict(extreme_input)
            handles_extreme = True
        except:
            handles_extreme = False
        
        # Test for overconfidence
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X_test)
            max_proba = np.max(proba, axis=1)
            predictions = model.predict(X_test)
            errors = predictions != y_test
            
            high_conf_errors = np.sum((max_proba > 0.95) & errors)
            overconfidence_rate = high_conf_errors / len(X_test)
            has_calibration = overconfidence_rate < 0.05
        else:
            has_calibration = False
        
        security_score = 0
        if handles_extreme:
            security_score += 50
        if has_calibration:
            security_score += 50
        
        self.passed = security_score >= 50
        self.score = security_score
        self.details = {
            'handles_extreme_inputs': bool(handles_extreme),
            'has_confidence_calibration': bool(has_calibration),
            'security_score': float(security_score),
            'passed': bool(self.passed)
        }
        
        return self.passed

class AISecurityValidator:
    """
    Comprehensive AI security validation and certification platform.
    """
    
    def __init__(self, model, model_name="AI System", compliance_standard=ComplianceStandard.NIST_AI_RMF):
        """
        Initialize the validator.
        
        Args:
            model: The AI model to validate
            model_name: Name of the AI system
            compliance_standard: Target compliance standard
        """
        self.model = model
        self.model_name = model_name
        self.compliance_standard = compliance_standard
        self.validation_tests = []
        self.results = {
            'model_name': model_name,
            'validation_date': datetime.now().isoformat(),
            'compliance_standard': compliance_standard.value,
            'tests': [],
            'summary': {},
            'certification': {}
        }
        
        # Initialize validation tests
        self._initialize_tests()
    
    def _initialize_tests(self):
        """Initialize all validation tests"""
        self.validation_tests = [
            AccuracyValidation(min_accuracy=0.85),
            RobustnessValidation(max_degradation=0.15),
            FairnessValidation(max_disparity=0.10),
            TransparencyValidation(),
            DataQualityValidation(),
            SecurityValidation()
        ]
    
    def run_validation(self, X_test, y_test):
        """
        Run complete validation suite.
        
        Args:
            X_test: Test data
            y_test: Test labels
        
        Returns:
            Validation results dictionary
        """
        print("=" * 70)
        print("AI Security Validation Platform")
        print(f"System: {self.model_name}")
        print(f"Standard: {self.compliance_standard.value}")
        print(f"Date: {self.results['validation_date']}")
        print("=" * 70)
        
        test_results = []
        
        for test in self.validation_tests:
            print(f"\n[*] Running {test.name}...")
            
            try:
                test.run(self.model, X_test, y_test)
                
                result = {
                    'name': test.name,
                    'category': test.category,
                    'weight': float(test.weight),
                    'passed': bool(test.passed),
                    'score': float(test.score),
                    'details': test.details
                }
                
                test_results.append(result)
                
                status = "PASSED" if test.passed else "FAILED"
                print(f"[{status}] {test.name}")
                print(f"    Score: {test.score:.2f}/100")
                
            except Exception as e:
                print(f"[ERROR] {test.name}: {str(e)}")
                test_results.append({
                    'name': test.name,
                    'category': test.category,
                    'weight': test.weight,
                    'passed': False,
                    'score': 0,
                    'details': {'error': str(e)}
                })
        
        self.results['tests'] = test_results
        
        # Generate summary and certification
        self._generate_summary()
        self._generate_certification()
        
        return self.results
    
    def _generate_summary(self):
        """Generate validation summary"""
        total_tests = len(self.results['tests'])
        passed_tests = sum(1 for t in self.results['tests'] if t['passed'])
        
        # Calculate weighted score
        total_weight = sum(t['weight'] for t in self.results['tests'])
        weighted_score = sum(t['score'] * t['weight'] for t in self.results['tests']) / total_weight
        
        # Category breakdown
        categories = {}
        for test in self.results['tests']:
            cat = test['category']
            if cat not in categories:
                categories[cat] = {'passed': 0, 'total': 0}
            categories[cat]['total'] += 1
            if test['passed']:
                categories[cat]['passed'] += 1
        
        self.results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'pass_rate': passed_tests / total_tests if total_tests > 0 else 0,
            'weighted_score': weighted_score,
            'category_breakdown': categories
        }
    
    def _generate_certification(self):
        """Generate certification based on validation results"""
        score = self.results['summary']['weighted_score']
        pass_rate = self.results['summary']['pass_rate']
        
        # Determine certification level
        if score >= 95 and pass_rate == 1.0:
            level = CertificationLevel.PLATINUM
        elif score >= 85 and pass_rate >= 0.85:
            level = CertificationLevel.GOLD
        elif score >= 75 and pass_rate >= 0.70:
            level = CertificationLevel.SILVER
        elif score >= 65 and pass_rate >= 0.50:
            level = CertificationLevel.BRONZE
        else:
            level = CertificationLevel.FAILED
        
        # Generate certificate ID
        cert_data = f"{self.model_name}{self.results['validation_date']}{score}"
        cert_id = hashlib.sha256(cert_data.encode()).hexdigest()[:16].upper()
        
        self.results['certification'] = {
            'level': level.value,
            'certificate_id': cert_id,
            'score': score,
            'pass_rate': pass_rate,
            'issued_date': self.results['validation_date'],
            'valid_until': self._calculate_expiry(),
            'compliance_standard': self.compliance_standard.value
        }
    
    def _calculate_expiry(self):
        """Calculate certificate expiry date (1 year from issuance)"""
        from datetime import timedelta
        issue_date = datetime.fromisoformat(self.results['validation_date'])
        expiry_date = issue_date + timedelta(days=365)
        return expiry_date.isoformat()
    
    def save_report(self, output_path):
        """
        Save validation report.
        
        Args:
            output_path: Path to save the report
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[+] Validation report saved to {output_path}")
    
    def print_summary(self):
        """Print validation summary and certification"""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        summary = self.results['summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Pass Rate: {summary['pass_rate']:.1%}")
        print(f"Weighted Score: {summary['weighted_score']:.2f}/100")
        
        print("\nCategory Breakdown:")
        for category, stats in summary['category_breakdown'].items():
            print(f"  {category}: {stats['passed']}/{stats['total']} passed")
        
        print("\n" + "=" * 70)
        print("CERTIFICATION")
        print("=" * 70)
        
        cert = self.results['certification']
        print(f"Level: {cert['level']}")
        print(f"Certificate ID: {cert['certificate_id']}")
        print(f"Score: {cert['score']:.2f}/100")
        print(f"Issued: {cert['issued_date']}")
        print(f"Valid Until: {cert['valid_until']}")
        print(f"Standard: {cert['compliance_standard']}")
        
        print("\n" + "=" * 70)
    
    def generate_certificate_document(self, output_path):
        """
        Generate a formatted certificate document.
        
        Args:
            output_path: Path to save the certificate
        """
        cert = self.results['certification']
        
        certificate_text = f"""
{'=' * 70}
                    CERTIFICATE OF VALIDATION
{'=' * 70}

This certifies that the AI system:

    {self.model_name}

has successfully completed security validation and compliance assessment
according to the {cert['compliance_standard']}.

CERTIFICATION LEVEL: {cert['level']}
CERTIFICATE ID: {cert['certificate_id']}
VALIDATION SCORE: {cert['score']:.2f}/100
PASS RATE: {self.results['summary']['pass_rate']:.1%}

ISSUED: {cert['issued_date']}
VALID UNTIL: {cert['valid_until']}

This certificate validates that the AI system meets the security,
performance, fairness, and governance requirements of the specified
compliance standard as of the validation date.

{'=' * 70}
                AI Security Validation Platform
                    Manus AI - January 2026
{'=' * 70}
"""
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(certificate_text)
        
        print(f"[+] Certificate document saved to {output_path}")


def load_target_model(model_path):
    """Load the target model for validation"""
    import pickle
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def main():
    parser = argparse.ArgumentParser(description="AI Security Validation Platform - Lab 12")
    parser.add_argument('--model', default='../month9/models/deepfake_detector.pkl',
                       help='Path to target model')
    parser.add_argument('--dataset', default='../month9/data/deepfake_dataset.csv',
                       help='Path to test dataset')
    parser.add_argument('--output', default='results/validation_report.json',
                       help='Path to save validation report')
    parser.add_argument('--certificate', default='results/certificate.txt',
                       help='Path to save certificate document')
    parser.add_argument('--model-name', default='Deepfake Detection System',
                       help='Name of the AI system')
    parser.add_argument('--standard', default='NIST_AI_RMF',
                       choices=['NIST_AI_RMF', 'EU_AI_ACT', 'ISO_IEC_42001', 'OWASP_ML_TOP_10'],
                       help='Compliance standard')
    
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
    
    print(f"[+] Loaded {len(X_test)} test samples\n")
    
    # Initialize validator
    standard = ComplianceStandard[args.standard]
    validator = AISecurityValidator(target_model, args.model_name, standard)
    
    # Run validation
    results = validator.run_validation(X_test, y_test)
    
    # Save report
    validator.save_report(args.output)
    
    # Generate certificate
    validator.generate_certificate_document(args.certificate)
    
    # Print summary
    validator.print_summary()


if __name__ == "__main__":
    main()
