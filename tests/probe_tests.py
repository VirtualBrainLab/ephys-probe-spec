import os
import pytest
from your_validation_script import check_required_files, validate_metadata, validate_site_map  # Update this import based on your file

def test_required_files():
    for subdir in os.listdir('.'):
        if os.path.isdir(subdir):
            assert check_required_files(subdir), f"Required files missing in {subdir}"

def test_metadata():
    for subdir in os.listdir('.'):
        if os.path.isdir(subdir):
            metadata_file = os.path.join(subdir, 'metadata.json')
            if os.path.isfile(metadata_file):
                assert validate_metadata(metadata_file), f"Invalid metadata in {subdir}"

def test_site_map():
    for subdir in os.listdir('.'):
        if os.path.isdir(subdir):
            site_map_file = os.path.join(subdir, 'site_map.csv')
            if os.path.isfile(site_map_file):
                assert validate_site_map(site_map_file), f"Invalid site map in {subdir}"
