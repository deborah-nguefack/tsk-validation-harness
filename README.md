# TSK Validation Harness

A Python-based validation tool for The Sleuth Kit (TSK) that helps small law enforcement agencies demonstrate tool reliability for evidence admissibility in Canadian courts.

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
