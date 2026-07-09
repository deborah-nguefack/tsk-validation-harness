#!/usr/bin/env python3
"""
Unit tests for Hash Extractor module
"""

import pytest
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.hash_extractor import TSKHashExtractor


class TestTSKHashExtractor:
    """Test suite for TSKHashExtractor"""
    
    def test_initialization(self):
        """Test that extractor initializes correctly"""
        extractor = TSKHashExtractor("data/test_image.dd")
        assert extractor.image_path == "data/test_image.dd"
        assert extractor.file_list == []
        assert extractor.hashes == {}
    
    def test_get_file_list(self):
        """Test file list extraction"""
        extractor = TSKHashExtractor("data/test_image.dd")
        files = extractor.get_file_list()
        assert len(files) > 0
        assert 'filename' in files[0]
        assert 'inode' in files[0]
    
    def test_extract_all_hashes(self):
        """Test hash extraction"""
        extractor = TSKHashExtractor("data/test_image.dd")
        hashes = extractor.extract_all_hashes()
        assert isinstance(hashes, dict)
        assert len(hashes) > 0
