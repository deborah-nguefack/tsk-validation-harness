#!/usr/bin/env python3
"""
Comparator for TSK Validation Harness
Compares TSK-extracted hashes against ground truth
"""

import csv
import sys
import os

def compare_hashes(tsk_csv, truth_csv, output_csv):
    """Compare TSK hashes against ground truth"""
    
    # Read TSK hashes
    tsk_hashes = {}
    with open(tsk_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tsk_hashes[row['filename']] = row['sha256']
    
    # Read ground truth
    truth_hashes = {}
    with open(truth_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            truth_hashes[row['filename']] = row['sha256']
    
    # Compare
    results = []
    matches = 0
    mismatches = 0
    missing_in_tsk = 0
    missing_in_truth = 0
    
    # Check all files in ground truth
    for filename, truth_hash in truth_hashes.items():
        if filename in tsk_hashes:
            if tsk_hashes[filename] == truth_hash:
                results.append({
                    'filename': filename,
                    'tsk_hash': tsk_hashes[filename],
                    'truth_hash': truth_hash,
                    'match': 'YES'
                })
                matches += 1
            else:
                results.append({
                    'filename': filename,
                    'tsk_hash': tsk_hashes[filename],
                    'truth_hash': truth_hash,
                    'match': 'NO'
                })
                mismatches += 1
        else:
            results.append({
                'filename': filename,
                'tsk_hash': 'MISSING',
                'truth_hash': truth_hash,
                'match': 'MISSING_IN_TSK'
            })
            missing_in_tsk += 1
    
    # Check for extra files in TSK not in ground truth
    for filename in tsk_hashes:
        if filename not in truth_hashes:
            results.append({
                'filename': filename,
                'tsk_hash': tsk_hashes[filename],
                'truth_hash': 'MISSING',
                'match': 'EXTRA_IN_TSK'
            })
            missing_in_truth += 1
    
    # Write results
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ['filename', 'tsk_hash', 'truth_hash', 'match']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    # Summary
    total = matches + mismatches
    accuracy = (matches / total * 100) if total > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"COMPARISON RESULTS")
    print(f"{'='*50}")
    print(f"Total files compared: {total}")
    print(f"✅ Matches: {matches}")
    print(f"❌ Mismatches: {mismatches}")
    print(f"📊 Accuracy: {accuracy:.2f}%")
    if missing_in_tsk > 0:
        print(f"⚠️  Files missing in TSK: {missing_in_tsk}")
    if missing_in_truth > 0:
        print(f"⚠️  Extra files in TSK: {missing_in_truth}")
    print(f"{'='*50}")
    print(f"Results saved to: {output_csv}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python comparator.py <tsk_csv> <truth_csv> <output_csv>")
        sys.exit(1)
    
    tsk_csv = sys.argv[1]
    truth_csv = sys.argv[2]
    output_csv = sys.argv[3]
    
    compare_hashes(tsk_csv, truth_csv, output_csv)
