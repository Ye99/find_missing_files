# Missing File Finder

This tool finds files in a subset directory that are not present in a superset directory by comparing file content.

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

*   `<subset_dir>`: The path to the directory that you expect to be a subset of the other.
*   `<superset_dir>`: The path to the directory that should contain all the files from the subset directory.

The tool will then compare the files in both directories and output a list of files that are present in `<subset_dir>` but missing from `<superset_dir>`.