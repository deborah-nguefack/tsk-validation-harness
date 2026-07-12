#!/usr/bin/env python3
import csv
import sys

def load_hashes(filename):
    hashes = {}
    with open(filename, 'r') as f:
        for line in f:
            if ':' in line:
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    hashes[parts[0]] = parts[1]
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

print(f"\nAccuracy: {match/total*100:.2f}% ({match}/{total})")
