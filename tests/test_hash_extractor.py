#!/usr/bin/env python3
import pytest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hash_extractor import extract_hashes


class TestHashExtractor:
    def test_extract_hashes_function_exists(self):
        assert callable(extract_hashes)

    def test_extract_hashes_accepts_two_arguments(self):
        import inspect
        sig = inspect.signature(extract_hashes)
        params = list(sig.parameters.keys())
        assert len(params) >= 2
        assert params[0] == 'image_path'
        assert params[1] == 'output_csv'

    def test_extract_hashes_runs_with_test_image(self):
        if os.path.exists("my-test.dd"):
            extract_hashes("my-test.dd", "outputs/test_hashes.csv")
            assert os.path.exists("outputs/test_hashes.csv")
