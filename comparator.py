#!/usr/bin/env python3
import csv

def compare_hashes(tsk_csv, truth_csv, output_csv):
    tsk_hashes = {}
    with open(tsk_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tsk_hashes[row['filename']] = row['sha256']
    
    ground_truth = {}
    with open(truth_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ground_truth[row['filename']] = row['sha256']
    
    results = []
    matches = 0
    mismatches = 0
    
    for filename, truth_hash in ground_truth.items():
        if filename in tsk_hashes:
            if tsk_hashes[filename] == truth_hash:
                matches += 1
                results.append({'filename': filename, 'tsk_hash': tsk_hashes[filename], 'truth_hash': truth_hash, 'match': 'YES'})
            else:
                mismatches += 1
                results.append({'filename': filename, 'tsk_hash': tsk_hashes[filename], 'truth_hash': truth_hash, 'match': 'NO'})
    
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ['filename', 'tsk_hash', 'truth_hash', 'match']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    total = matches + mismatches
    accuracy = (matches / total * 100) if total > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"COMPARISON RESULTS")
    print(f"{'='*50}")
    print(f"Total files compared: {total}")
    print(f"✅ Matches: {matches}")
    print(f"❌ Mismatches: {mismatches}")
    print(f"📊 Accuracy: {accuracy:.2f}%")
    print(f"{'='*50}")
    print(f"Results saved to: {output_csv}")
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python comparator.py <tsk_csv> <truth_csv> <output_csv>")
        sys.exit(1)
    compare_hashes(sys.argv[1], sys.argv[2], sys.argv[3])
