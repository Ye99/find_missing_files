import os
import pytest
from missing_file_finder import core

def _create_file(dir_path, filename, content):
    """Helper function to create a file with specific content."""
    with open(os.path.join(dir_path, filename), "w") as f:
        f.write(content)

def test_find_missing_files_basic(tmp_path):
    """
    Tests that the tool correctly identifies a missing file,
    using pytest's tmp_path fixture for cleanup.
    """
    subset_dir = tmp_path / "subset"
    superset_dir = tmp_path / "superset"
    subset_dir.mkdir()
    superset_dir.mkdir()

    # Create a file that exists in both sets
    _create_file(superset_dir, "file1.txt", "content1")
    _create_file(subset_dir, "fileA.txt", "content1")

    # Create a file that only exists in the subset
    _create_file(subset_dir, "fileB.txt", "content2")
    missing_file_path = os.path.abspath(os.path.join(subset_dir, "fileB.txt"))

    # Find missing files
    missing_files = core.find_missing_files(subset_dir, superset_dir)

    # Assert that the correct missing file is found
    assert len(missing_files) == 1
    assert missing_file_path in missing_files