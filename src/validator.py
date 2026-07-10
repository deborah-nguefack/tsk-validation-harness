#!/usr/bin/env python3
"""
TSK Validation Harness - Main Entry Point
Runs the complete validation pipeline: extract → compare → report
"""

import sys
import os
import json
from datetime import datetime

# Import your modules (all use functions, not classes)
from hash_extractor import extract_hashes
from comparator import compare_hashes
from court_reporter import generate_report


class TSKValidator:
    """
    Main validation harness that orchestrates:
    1. Hash extraction using TSK
    2. Comparison against ground truth
    3. Court-ready report generation
    """
    
    def __init__(self, image_path="data/test_image.dd", ground_truth="data/ground_truth.csv"):
        self.image_path = image_path
        self.ground_truth = ground_truth
        self.start_time = None
        self.end_time = None
    
    def run_hash_extractor(self):
        """Step 1: Extract hashes from disk image using TSK"""
        print("\n" + "="*60)
        print("Step 1: Extracting file hashes using TSK...")
        print("="*60)
        
        try:
            extract_hashes(self.image_path, "outputs/tsk_hashes.csv")
            print(f"✅ Extraction complete")
            return True
            
        except Exception as e:
            print(f"❌ Error during hash extraction: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_comparator(self):
        """Step 2: Compare extracted hashes against ground truth"""
        print("\n" + "="*60)
        print("Step 2: Comparing hashes against ground truth...")
        print("="*60)
        
        try:
            compare_hashes("outputs/tsk_hashes.csv", self.ground_truth, "outputs/comparison_results.csv")
            return True
            
        except Exception as e:
            print(f"❌ Error during comparison: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_court_reporter(self):
        """Step 3: Generate court-ready JSON report"""
        print("\n" + "="*60)
        print("Step 3: Generating court-ready report...")
        print("="*60)
        
        try:
            generate_report("outputs/comparison_results.csv", "outputs/court_report.json")
            return True
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_full_validation(self):
        """Run the complete validation pipeline"""
        print("\n" + "="*60)
        print("🔍 TSK VALIDATION HARNESS")
        print("="*60)
        print(f"Image: {self.image_path}")
        print(f"Ground Truth: {self.ground_truth}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = datetime.now()
        
        success = True
        if not self.run_hash_extractor():
            success = False
        if not self.run_comparator():
            success = False
        if not self.run_court_reporter():
            success = False
        
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        print("\n" + "="*60)
        print("📊 VALIDATION COMPLETE")
        print("="*60)
        print(f"Duration: {duration:.2f} seconds")
        print(f"Status: {'✅ PASSED' if success else '❌ FAILED'}")
        print("\nOutputs saved to: outputs/")
        print("  - tsk_hashes.csv")
        print("  - comparison_results.csv")
        print("  - court_report.json")
        print("\n📋 Court report ready for review: outputs/court_report.json")
        print("="*60)
        
        return success


def main():
    """Command-line entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="TSK Validation Harness - Validate TSK against NIST ground truth"
    )
    
    parser.add_argument(
        '--image',
        default='data/test_image.dd',
        help='Path to disk image (default: data/test_image.dd)'
    )
    parser.add_argument(
        '--ground-truth',
        default='data/ground_truth.csv',
        help='Path to ground truth CSV (default: data/ground_truth.csv)'
    )
    
    args = parser.parse_args()
    
    os.makedirs('outputs', exist_ok=True)
    
    validator = TSKValidator(args.image, args.ground_truth)
    success = validator.run_full_validation()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
