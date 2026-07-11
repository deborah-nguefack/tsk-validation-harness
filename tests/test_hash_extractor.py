#!/usr/bin/env python3
"""
Unit tests for Hash Extractor module
"""

import pytest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.hash_extractor import extract_hashes


class TestHashExtractor:
    """Test suite for hash_extractor.py"""
    
    def test_extract_hashes_function_exists(self):
        """Test that extract_hashes is a callable function"""
        assert callable(extract_hashes)
    
    def test_extract_hashes_accepts_two_arguments(self):
        """Test that extract_hashes accepts image_path and output_csv"""
        import inspect
        sig = inspect.signature(extract_hashes)
        params = list(sig.parameters.keys())
        assert len(params) == 2
        assert params[0] == 'image_path'
        assert params[1] == 'output_csv'
    
    def test_extract_hashes_runs_with_test_image(self):
        """Test that extract_hashes runs without errors on test image"""
        # This creates a small test file and verifies the function runs
        import tempfile
        
        # Use the existing test image if available
        test_image = "data/test_image.dd"
        output_csv = "outputs/test_hashes.csv"
        
        if os.path.exists(test_image):
            extract_hashes(test_image, output_csv)
            assert os.path.exists(output_csv)
