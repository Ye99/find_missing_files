import os
from . import utils
from tqdm import tqdm

def _count_files_in_dir(directory: str) -> int:
    """Helper function to count files in a directory for tqdm progress bar."""
    count = 0
    for _, _, filenames in os.walk(directory):
        count += len(filenames)
    return count

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
    
    total_superset_files = _count_files_in_dir(superset_dir)
    superset_files_iterable = (
        os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk(superset_dir)
        for filename in filenames
    )

    for filepath in tqdm(superset_files_iterable, total=total_superset_files, desc="Hashing superset files", unit="file", leave=False):
        file_hash = utils.hash_file(filepath)
        superset_hashes.add(file_hash)

    missing_files = []
    
    total_subset_files = _count_files_in_dir(subset_dir)
    subset_files_iterable = (
        os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk(subset_dir)
        for filename in filenames
    )

    for filepath in tqdm(subset_files_iterable, total=total_subset_files, desc="Comparing subset files", unit="file", leave=True):
        file_hash = utils.hash_file(filepath)
        if file_hash not in superset_hashes:
            missing_files.append(os.path.abspath(filepath))

    return missing_files