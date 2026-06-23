#!/usr/bin/env python3
"""
Court Reporter for TSK Validation Harness
Generates JSON report with match/mismatch + accuracy
"""

import csv
import json
import sys
import os
from datetime import datetime

def generate_report(comparison_csv, output_json):
    """Generate court-ready JSON report"""
    
    # Read comparison results
    results = []
    matches = 0
    mismatches = 0
    missing = 0
    extra = 0
    
    with open(comparison_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
            if row['match'] == 'YES':
                matches += 1
            elif row['match'] == 'NO':
                mismatches += 1
            elif row['match'] == 'MISSING_IN_TSK':
                missing += 1
            elif row['match'] == 'EXTRA_IN_TSK':
                extra += 1
    
    total = matches + mismatches
    accuracy = (matches / total * 100) if total > 0 else 0
    
    # Generate report
    report = {
        "report_metadata": {
            "timestamp": datetime.now().isoformat(),
            "tool": "TSK Validation Harness",
            "version": "1.0",
            "purpose": "Validate TSK for evidence admissibility"
        },
        "summary": {
            "total_files_compared": total,
            "matches": matches,
            "mismatches": mismatches,
            "missing_in_tsk": missing,
            "extra_in_tsk": extra,
            "accuracy_percent": round(accuracy, 2)
        },
        "court_summary": {
            "statement": f"TSK demonstrated {accuracy:.2f}% accuracy on {total} files. {matches} out of {total} files matched ground truth.",
            "recommendation": "Tool is reliable for forensic use" if accuracy >= 95 else "Further validation recommended"
        },
        "detailed_results": results
    }
    
    # Write JSON
    with open(output_json, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Court report saved to: {output_json}")
    print(f"\n📊 SUMMARY:")
    print(f"   Files compared: {total}")
    print(f"   Accuracy: {accuracy:.2f}%")
    print(f"   Court statement: {report['court_summary']['statement']}")
    
    return report

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python court_reporter.py <comparison_csv> <output_json>")
        sys.exit(1)
    
    comparison_csv = sys.argv[1]
    output_json = sys.argv[2]
    
    generate_report(comparison_csv, output_json)
