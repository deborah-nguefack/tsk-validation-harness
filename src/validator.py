#!/usr/bin/env python3
"""
TSK Validation Harness - Main Entry Point
Runs the complete validation pipeline: extract → compare → report
"""

import subprocess
import sys
import os
import json
from datetime import datetime


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
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def run_hash_extractor(self):
        """Step 1: Extract hashes from disk image using TSK"""
        print("\n" + "="*60)
        print("Step 1: Extracting file hashes using TSK...")
        print("="*60)
        
        try:
            # Import the hash extractor
            from hash_extractor import TSKHashExtractor
            
            # Run extraction
            extractor = TSKHashExtractor(self.image_path)
            hashes = extractor.extract_all_hashes()
            extractor.save_hashes("outputs/tsk_hashes.csv")
            
            print(f"✅ Extracted {len(hashes)} file hashes")
            print(f"   Saved to: outputs/tsk_hashes.csv")
            return True
            
        except Exception as e:
            print(f"❌ Error during hash extraction: {e}")
            return False
    
    def run_comparator(self):
        """Step 2: Compare extracted hashes against ground truth"""
        print("\n" + "="*60)
        print("Step 2: Comparing hashes against ground truth...")
        print("="*60)
        
        try:
            from comparator import HashComparator
            import json
            
            # Load extracted hashes
            with open("outputs/tsk_hashes.json", 'r') as f:
                extracted = json.load(f)
            
            # Compare against ground truth
            comparator = HashComparator(self.ground_truth)
            results = comparator.compare(extracted)
            accuracy = comparator.get_accuracy(results)
            
            # Save results
            with open("outputs/comparison_results.json", 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"✅ Matches: {len(results['matches'])}")
            print(f"❌ Mismatches: {len(results['mismatches'])}")
            print(f"📊 Accuracy: {accuracy:.2f}%")
            print(f"   Saved to: outputs/comparison_results.json")
            return True
            
        except Exception as e:
            print(f"❌ Error during comparison: {e}")
            return False
    
    def run_court_reporter(self):
        """Step 3: Generate court-ready JSON report"""
        print("\n" + "="*60)
        print("Step 3: Generating court-ready report...")
        print("="*60)
        
        try:
            from court_reporter import CourtReporter
            import json
            
            # Load comparison results
            with open("outputs/comparison_results.json", 'r') as f:
                results = json.load(f)
            
            # Calculate accuracy
            total = len(results['matches']) + len(results['mismatches'])
            accuracy = (len(results['matches']) / total * 100) if total > 0 else 0
            
            # Generate report
            reporter = CourtReporter(results, accuracy)
            reporter.save_report("outputs/court_report.json")
            
            # Display summary
            with open("outputs/court_report.json", 'r') as f:
                report = json.load(f)
            
            print(f"✅ Court report generated successfully")
            print(f"   Saved to: outputs/court_report.json")
            print("\n📋 Report Summary:")
            print(f"   Total Files: {report['validation_summary']['total_files']}")
            print(f"   Accuracy: {report['validation_summary']['accuracy']}%")
            print(f"   Status: {report['validation_summary']['validation_status']}")
            print(f"   Confidence: {report['court_summary']['confidence_level']}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
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
        
        # Run all three steps
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
        print("  - tsk_hashes.json")
        print("  - comparison_results.json")
        print("  - court_report.json")
        print("\n📋 Court report ready for review: outputs/court_report.json")
        print("="*60)
        
        return success


def main():
    """Command-line entry point with optional arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="TSK Validation Harness - Validate TSK against NIST ground truth",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/validator.py                                    # Run with default test image
  python src/validator.py --image my_image.dd                # Use custom image
  python src/validator.py --ground-truth my_truth.csv        # Use custom ground truth
        """
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
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Skip hash extraction if previous results exist'
    )
    
    args = parser.parse_args()
    
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    # Run validation
    validator = TSKValidator(args.image, args.ground_truth)
    success = validator.run_full_validation()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
