#!/usr/bin/env python3
import csv
import json
from datetime import datetime

def generate_report(comparison_csv, output_json):
    results = []
    matches = 0
    mismatches = 0
    
    with open(comparison_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
            if row['match'] == 'YES':
                matches += 1
            elif row['match'] == 'NO':
                mismatches += 1
    
    total = matches + mismatches
    accuracy = (matches / total * 100) if total > 0 else 0
    
    report = {
        "validation_summary": {
            "total_files": total,
            "matches": matches,
            "mismatches": mismatches,
            "accuracy": round(accuracy, 2),
            "validation_timestamp": datetime.now().isoformat(),
            "validation_status": "PASSED" if accuracy >= 95 else "REVIEW_REQUIRED"
        },
        "court_summary": {
            "tool": "TSK Hash Extractor",
            "validation_result": "PASSED" if accuracy >= 95 else "REVIEW_REQUIRED",
            "accuracy": f"{accuracy:.2f}%",
            "confidence_level": "HIGH" if accuracy >= 98 else "MODERATE" if accuracy >= 90 else "LOW",
            "confidence_statement": f"TSK demonstrated {accuracy:.2f}% accuracy against ground truth.",
            "legal_reference": "Validated under R. v. Mohan (1994) and R. v. Bingley (2017)."
        },
        "file_results": results
    }
    
    with open(output_json, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Court report saved to: {output_json}")
    print(f"\n📊 SUMMARY:")
    print(f"   Files compared: {total}")
    print(f"   Accuracy: {accuracy:.2f}%")
    print(f"   Status: {report['validation_summary']['validation_status']}")
    
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python court_reporter.py <comparison_csv> <output_json>")
        sys.exit(1)
    generate_report(sys.argv[1], sys.argv[2])
