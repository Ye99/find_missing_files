import hashlib
import pytest
from missing_file_finder import utils

def test_hash_file(tmp_path):
    """
    Tests that the hash_file function correctly calculates the SHA-256 hash of a file,
    using pytest's tmp_path fixture for cleanup.
    """
    # Create a temporary file with known content
    content = b"This is a test file for hashing."
    p = tmp_path / "test_file.tmp"
    p.write_bytes(content)

    # Calculate expected hash
    expected_hash = hashlib.sha256(content).hexdigest()

    # Calculate actual hash using the utility function
    actual_hash = utils.hash_file(p)

    # Assert that the hashes are equal
    assert expected_hash == actual_hash