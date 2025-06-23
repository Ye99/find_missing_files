import os
import pytest
from missing_file_finder import core
from missing_file_finder.core import _count_files_in_dir

def _create_file(dir_path, filename, content):
    """Helper function to create a file with specific content."""
    # Ensure parent directory exists if it's a nested path
    os.makedirs(os.path.dirname(os.path.join(dir_path, filename)), exist_ok=True)
    with open(os.path.join(dir_path, filename), "w") as f:
        f.write(content)

def test_count_files_in_dir_empty(tmp_path):
    """Test _count_files_in_dir with an empty directory."""
    assert _count_files_in_dir(tmp_path) == 0

def test_count_files_in_dir_root_files(tmp_path):
    """Test _count_files_in_dir with files only in the root."""
    _create_file(tmp_path, "file1.txt", "content1")
    _create_file(tmp_path, "file2.txt", "content2")
    assert _count_files_in_dir(tmp_path) == 2

def test_count_files_in_dir_nested_files(tmp_path):
    """Test _count_files_in_dir with files in subdirectories."""
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    _create_file(tmp_path, "root_file.txt", "root_content")
    _create_file(subdir, "sub_file1.txt", "sub_content1")
    _create_file(subdir, "sub_file2.txt", "sub_content2")
    
    nested_subdir = subdir / "nested"
    nested_subdir.mkdir()
    _create_file(nested_subdir, "nested_file.txt", "nested_content")
    
    assert _count_files_in_dir(tmp_path) == 4

def test_count_files_in_dir_only_empty_subdirs(tmp_path):
    """Test _count_files_in_dir with only empty subdirectories."""
    subdir1 = tmp_path / "subdir1"
    subdir1.mkdir()
    subdir2 = tmp_path / "subdir2"
    subdir2.mkdir()
    assert _count_files_in_dir(tmp_path) == 0

def test_count_files_in_dir_files_and_empty_subdirs(tmp_path):
    """Test _count_files_in_dir with files and empty subdirectories."""
    _create_file(tmp_path, "file1.txt", "content1")
    subdir1 = tmp_path / "subdir1" # Empty subdir
    subdir1.mkdir()
    assert _count_files_in_dir(tmp_path) == 1

def test_find_missing_files_basic(tmp_path, capsys):
    """
    Tests that the tool correctly identifies a missing file,
    using pytest's tmp_path fixture for cleanup.
    Progress bar output should be captured.
    """
    subset_dir = tmp_path / "subset"
    superset_dir = tmp_path / "superset"
    subset_dir.mkdir()
    superset_dir.mkdir()

    # Create a file that exists in both sets (by content)
    _create_file(superset_dir, "file1.txt", "content1")
    _create_file(subset_dir, "fileA.txt", "content1") # Same content, different name

    # Create a file that only exists in the subset
    _create_file(subset_dir, "fileB.txt", "content2")
    missing_file_path = os.path.abspath(os.path.join(subset_dir, "fileB.txt"))
    
    # Create a file that only exists in superset (should not affect missing list)
    _create_file(superset_dir, "file2.txt", "content3")

    # Find missing files
    missing_files = core.find_missing_files(str(subset_dir), str(superset_dir))

    # Assert that the correct missing file is found
    assert len(missing_files) == 1
    assert missing_file_path in missing_files
    
    # Optionally, assert that captured output is not empty if tqdm fallback is used
    # captured = capsys.readouterr()
    # if "tqdm not installed" in captured.out: # or captured.err depending on tqdm config
    #     assert "Processing (tqdm not installed)" in captured.out

def test_find_missing_files_no_missing(tmp_path, capsys):
    """Test when no files are missing."""
    subset_dir = tmp_path / "subset"
    superset_dir = tmp_path / "superset"
    subset_dir.mkdir()
    superset_dir.mkdir()

    _create_file(superset_dir, "file1.txt", "content1")
    _create_file(subset_dir, "fileA.txt", "content1")
    _create_file(superset_dir, "file2.txt", "content2")
    _create_file(subset_dir, "fileB.txt", "content2")

    missing_files = core.find_missing_files(str(subset_dir), str(superset_dir))
    assert len(missing_files) == 0

def test_find_missing_files_all_missing(tmp_path, capsys):
    """Test when all files in subset are missing from superset."""
    subset_dir = tmp_path / "subset"
    superset_dir = tmp_path / "superset" # Empty superset
    subset_dir.mkdir()
    superset_dir.mkdir()

    _create_file(subset_dir, "fileA.txt", "content1")
    _create_file(subset_dir, "fileB.txt", "content2")
    
    path_a = os.path.abspath(os.path.join(subset_dir, "fileA.txt"))
    path_b = os.path.abspath(os.path.join(subset_dir, "fileB.txt"))

    missing_files = core.find_missing_files(str(subset_dir), str(superset_dir))
    assert len(missing_files) == 2
    assert path_a in missing_files
    assert path_b in missing_files

def test_find_missing_files_empty_subset(tmp_path, capsys):
    """Test when the subset directory is empty."""
    subset_dir = tmp_path / "subset" # Empty subset
    superset_dir = tmp_path / "superset"
    subset_dir.mkdir()
    superset_dir.mkdir()

    _create_file(superset_dir, "file1.txt", "content1")

    missing_files = core.find_missing_files(str(subset_dir), str(superset_dir))
    assert len(missing_files) == 0

def test_find_missing_files_empty_superset_and_subset(tmp_path, capsys):
    """Test when both directories are empty."""
    subset_dir = tmp_path / "subset" 
    superset_dir = tmp_path / "superset"
    subset_dir.mkdir()
    superset_dir.mkdir()

    missing_files = core.find_missing_files(str(subset_dir), str(superset_dir))
    assert len(missing_files) == 0

def test_find_missing_files_nested_directories(tmp_path, capsys):
    """Test with files in nested directories."""
    subset_dir = tmp_path / "subset"
    superset_dir = tmp_path / "superset"
    subset_dir.mkdir()
    superset_dir.mkdir()

    # Files in superset
    _create_file(superset_dir, "common.txt", "content_common")
    superset_sub = superset_dir / "sub"
    superset_sub.mkdir()
    _create_file(superset_sub, "superset_only_in_sub.txt", "content_superset_sub")

    # Files in subset
    _create_file(subset_dir, "common.txt", "content_common") # Same content as in superset root
    subset_sub = subset_dir / "sub"
    subset_sub.mkdir()
    _create_file(subset_sub, "subset_missing_in_sub.txt", "content_subset_sub_missing")
    
    missing_path = os.path.abspath(os.path.join(subset_sub, "subset_missing_in_sub.txt"))

    missing_files = core.find_missing_files(str(subset_dir), str(superset_dir))
    assert len(missing_files) == 1
    assert missing_path in missing_files