# Missing File Finder

This tool identifies files within a specified `subset_dir` that are not present in a `superset_dir` by comparing their content hashes. While this approach is more computationally intensive than methods relying solely on filenames or modification times, it provides a more reliable way to determine if files with identical content exist across the two directories.

## Key Features

- **Content-based comparison**: Uses SHA-256 hashing to compare file content rather than names or timestamps
- **Memory efficient**: Extremely low memory requirements - uses only ~32 bytes per file in the superset directory plus file paths for missing files
- **Large file support**: Processes files of any size using 4KB streaming chunks, maintaining constant memory usage during file reading
- **Progress tracking**: Real-time progress bars show processing status for both directories

## Memory Requirements

The tool has minimal memory requirements that scale predictably:

- **Per superset file**: ~105 bytes (for SHA-256 hash string storage)
- **Per missing file**: ~100-500 bytes (for absolute file path storage, depending on path length)
- **File reading**: Fixed 4KB buffer regardless of individual file sizes

**Memory Complexity (Big O notation):**
- **Space complexity**: O(F_superset + M) where:
  - F_superset = number of files in superset directory
  - M = number of missing files found
- **Auxiliary space**: O(F_superset) for hash storage during processing
- **File processing**: O(1) constant memory per file regardless of file size

- **Example**: For 100,000 files in superset with 1,000 missing files, total memory usage is approximately 11MB

This makes the tool suitable for processing directories containing millions of files without memory constraints.

## Environment Setup

1.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**

    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the tool, use the following command in your terminal:

```bash
python -m missing_file_finder <subset_dir> <superset_dir>
```

### Arguments

*   `<subset_dir>`: The path to the directory containing the files you want to check.
*   `<superset_dir>`: The path to the reference directory against which the files from `<subset_dir>` will be compared.

The tool will compare the content of files in both directories and display:
- Total number of missing files (if any)
- Complete list of files found in `<subset_dir>` but not in `<superset_dir>` based on their content