#!/usr/bin/env python3
"""
TSK Validation Harness - Main Entry Point
"""

import sys
import os
import json
from datetime import datetime

from hash_extractor import extract_hashes
from comparator import compare_hashes
from court_reporter import generate_report


class TSKValidator:
    def __init__(self, image_path, ground_truth, offset=0):
        self.image_path = image_path
        self.ground_truth = ground_truth
        self.offset = offset
    
    def run_all(self):
        print("\n" + "="*60)
        print("🔍 TSK VALIDATION HARNESS")
        print("="*60)
        print(f"Image: {self.image_path}")
        print(f"Ground Truth: {self.ground_truth}")
        print(f"Offset: {self.offset}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "="*60)
        print("Step 1: Extracting file hashes using TSK...")
        print("="*60)
        
        try:
            extract_hashes(self.image_path, "outputs/tsk_hashes.csv", self.offset)
            print("✅ Extraction complete")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        print("\n" + "="*60)
        print("Step 2: Comparing hashes against ground truth...")
        print("="*60)
        
        try:
            compare_hashes("outputs/tsk_hashes.csv", self.ground_truth, "outputs/comparison_results.csv")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        print("\n" + "="*60)
        print("Step 3: Generating court-ready report...")
        print("="*60)
        
        try:
            generate_report("outputs/comparison_results.csv", "outputs/court_report.json")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        print("\n" + "="*60)
        print("📊 VALIDATION COMPLETE")
        print("="*60)
        print("Status: ✅ PASSED")
        print("Output: outputs/court_report.json")
        print("="*60)
        
        return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TSK Validation Harness")
    parser.add_argument('--image', default='my-test.dd', help='Disk image path')
    parser.add_argument('--ground-truth', default='ground_truth.csv', help='Ground truth CSV')
    parser.add_argument('--offset', default=0, type=int, help='Filesystem offset in bytes')
    
    args = parser.parse_args()
    
    os.makedirs('outputs', exist_ok=True)
    
    validator = TSKValidator(args.image, args.ground_truth, args.offset)
    success = validator.run_all()
    
    sys.exit(0 if success else 1)
