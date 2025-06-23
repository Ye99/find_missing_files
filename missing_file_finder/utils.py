import hashlib

def hash_file(filepath: str) -> str:
    """
    Calculates the SHA-256 hash of a file by streaming it in chunks.
    This is memory-efficient for large files.

    Args:
        filepath: The absolute or relative path to the file.

    Returns:
        The hex digest of the SHA-256 hash.
    """
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()