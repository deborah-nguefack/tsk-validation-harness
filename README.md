# TSK Validation Harness

This is a Python-based validation tool for The Sleuth Kit (TSK) that helps small law enforcement agencies demonstrate tool reliability for evidence admissibility in Canadian courts.

## Overview

This tool validates TSK file hashes against the NIST CFReDS M57-Jean ground truth dataset, producing a court-ready JSON report. It addresses the challenge faced by resource-constrained Canadian law enforcement agencies who use open-source forensic tools but must still meet evidentiary standards under *R. v. Mohan* (1994) and *R. v. Bingley* (2017).

## Features

- Extracts file hashes from disk images using TSK (`fls`, `icat`, `istat`)
- Compares extracted hashes against NIST ground truth
- Generates JSON report with:
  - File-by-file match/mismatch status
  - Accuracy percentage
  - Plain-language court summary
- Sanity test injection for mismatch detection verification
- Processing: <10 minutes/10GB on standard hardware

## Repository Structure

```
tsk-validation-harness/
├── README.md
├── LICENSE
├── requirements.txt
├── src/
│   ├── validator.py
│   ├── hash_extractor.py
│   ├── comparator.py
│   └── court_reporter.py
├── tests/
│   └── test_hash_extractor.py
├── data/
│   ├── ground_truth.csv
│   └── test_image.dd
└── outputs/
    ├── tsk_hashes.json
    ├── comparison_results.json
    └── court_report.json
```

## Installation

### Prerequisites

- Python 3.11+
- The Sleuth Kit (TSK) 4.12+

### Step 1: Install TSK

**Ubuntu/Debian:**
```bash
sudo apt-get install sleuthkit
```

**macOS:**
```bash
brew install sleuthkit
```

**Windows:**
Download from https://www.sleuthkit.org/sleuthkit/download.php

### Step 2: Clone and Set Up

```bash
git clone https://github.com/deborah-nguefack/tsk-validation-harness.git
cd tsk-validation-harness
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

### Option A: One Command (Recommended)

```bash
python src/validator.py
```

### Option B: Run Step by Step

```bash
python src/hash_extractor.py   # Step 1: Extract hashes
python src/comparator.py       # Step 2: Compare against ground truth
python src/court_reporter.py   # Step 3: Generate court report
```

## Expected Output

```json
{
  "validation_summary": {
    "total_files": 500,
    "matches": 498,
    "mismatches": 2,
    "accuracy": 99.6
  },
  "court_summary": {
    "validation_result": "PASSED",
    "confidence_level": "HIGH"
  }
}
```

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT License

## Authors

- Naomi Nguefack (1416225)
- Deborah Essien (1408505)

## References

- Casey, E., Nelson, A. & Hyde, J. (2019). Digital Investigation, 31, 100873.
- Hargreaves, C., Nelson, A., & Casey, E. (2024). Forensic Science International: Digital Investigation, 48(Suppl.) 301723.
- NIST (2023). Computer Forensic Reference Data Sets (CFReDS). https://cfreds.nist.gov/
