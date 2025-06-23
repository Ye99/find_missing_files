import os
from . import utils

def find_missing_files(subset_dir: str, superset_dir: str) -> list[str]:
    """
    Finds files that are in the subset directory but not in the superset directory
    by comparing their content hashes.

    Args:
        subset_dir: The path to the directory of files to check.
        superset_dir: The path to the directory of files to check against.

    Returns:
        A list of absolute paths to files that are in the subset directory
        but not in the superset directory.
    """
    superset_hashes = set()
    for dirpath, _, filenames in os.walk(superset_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = utils.hash_file(filepath)
            superset_hashes.add(file_hash)

    missing_files = []
    for dirpath, _, filenames in os.walk(subset_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = utils.hash_file(filepath)
            if file_hash not in superset_hashes:
                missing_files.append(os.path.abspath(filepath))

    return missing_files