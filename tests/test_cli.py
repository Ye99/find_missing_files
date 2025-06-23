import os
import pytest
from click.testing import CliRunner
from missing_file_finder import cli

def _create_file(dir_path, filename, content):
    """Helper function to create a file with specific content."""
    with open(os.path.join(dir_path, filename), "w") as f:
        f.write(content)

def test_cli_find_missing_files(tmp_path):
    """
    Tests the CLI by invoking the main command and checking the output.
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

    runner = CliRunner()
    result = runner.invoke(cli.main, [str(subset_dir), str(superset_dir)])

    assert result.exit_code == 0
    assert missing_file_path in result.output

def test_cli_no_missing_files(tmp_path):
    """
    Tests the CLI when no files are missing.
    """
    subset_dir = tmp_path / "subset"
    superset_dir = tmp_path / "superset"
    subset_dir.mkdir()
    superset_dir.mkdir()

    # Create files that exist in both sets (by content)
    _create_file(superset_dir, "file1.txt", "content1")
    _create_file(subset_dir, "fileA.txt", "content1") # Same content
    _create_file(superset_dir, "file2.txt", "content2")
    _create_file(subset_dir, "fileB.txt", "content2") # Same content

    runner = CliRunner()
    result = runner.invoke(cli.main, [str(subset_dir), str(superset_dir)])

    assert result.exit_code == 0
    assert "All files in the subset folder are present in the superset folder." in result.output
    assert "Total missing files number:" not in result.output