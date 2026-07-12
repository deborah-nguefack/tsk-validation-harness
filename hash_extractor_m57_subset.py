#!/usr/bin/env python3
import csv
import os

def load_hashes(filename):
    hashes = {}
    with open(filename, 'r') as f:
        for line in f:
            if 'Processing:' in line:
                # Get the next line with the hash
                next_line = f.readline()
                if ':' in next_line:
                    parts = next_line.strip().split(': ')
                    if len(parts) == 2:
                        filepath = parts[0].strip()
                        hash_value = parts[1]
                        # Use basename for comparison
                        basename = os.path.basename(filepath)
                        hashes[basename] = hash_value
    return hashes

def load_ground_truth(filename):
    ground = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ground[row['filename']] = row['sha256']
    return ground

tsk = load_hashes('tsk_hashes_m57.txt')
truth = load_ground_truth('m57_ground_truth.csv')

match = 0
total = 0
for f in tsk:
    if f in truth:
        total += 1
        if tsk[f] == truth[f]:
            match += 1
            print(f"✅ {f}: MATCH")
        else:
            print(f"❌ {f}: MISMATCH")

if total > 0:
    print(f"\nAccuracy: {match/total*100:.2f}% ({match}/{total})")
else:
    print("\nNo matching filenames found")
