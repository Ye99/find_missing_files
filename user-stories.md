Create user story for this Python tool: 1. the tool takes subset folder and superset folder as parameters 2. for each file in subset folder (recursive including its child folders), look up if it is in superset folder as well. Compare hash code of files to make reliable identitiy test. 3. Note the folder structures can be different between subset folder and superset folder. As long as hash code matches, it's a found. 4. List files are in subset folder but missing from super folder. Give full path of such file to help user review it. 5. non-fuction requirement: use efficient algorithm, the tool should run as fast as possible. 5. use TDD method to develop the tool, write unit tests. 

User Story 1: Core File Comparison
Title: Find Missing Files by Content

As a data manager,
I want to compare files in a "subset" directory with files in a "superset" directory and identify those that are missing from the superset,
So that I can ensure all necessary files are present in the master collection.

Acceptance Criteria:

The tool must accept two command-line arguments: the path to the "subset" folder and the path to the "superset" folder.
The tool must recursively scan all files within the subset folder and its subdirectories.
For each file in the subset folder, the tool must determine if a file with the exact same content exists anywhere within the superset folder's entire directory tree.
File identity must be verified by comparing the hash (e.g., SHA-256) of file contents, not by comparing filenames or directory structures.
The tool must output a list of the full, absolute paths of all files that exist in the subset folder but are not found in the superset folder.
If all files in the subset folder are found in the superset folder, the tool should output a confirmation message indicating that no files are missing.
Edge Cases and Considerations:

Error Handling: The tool should handle cases where provided paths are invalid or do not exist.
Empty Folders: The tool should function correctly if either the subset or superset folder is empty.
Permissions: The tool must have read permissions for all files and directories it needs to scan.
User Story 2: Performance Optimization (Non-Functional)
Title: Ensure Efficient File Comparison

As a developer,
I want to implement an efficient algorithm for hashing and comparing files,
So that the tool runs as quickly as possible, even with very large folders.

Acceptance Criteria:

The process of hashing files in the superset folder should be optimized to avoid re-computation.
A hash lookup map (e.g., a hash set or dictionary) should be created for the superset files to allow for near-constant time O(1) lookups.
The tool should process the subset folder file by file, performing a single hash computation and one lookup per file.
The overall time complexity should be optimized to be proportional to the total number of files, not a nested comparison loop.
Edge Cases and Considerations:

Memory Usage: The hash map for the superset folder will consume memory. The implementation should be mindful of memory constraints for extremely large file sets.
Large Files: Hashing very large files can be time-consuming; the process should be streamed to avoid loading entire large files into memory at once.
User Story 3: Development Methodology (Technical)
Title: Develop with Test-Driven Development

As a developer,
I want to use Test-Driven Development (TDD) to build the tool,
So that I can ensure each component is reliable, correct, and maintainable from the start.

Acceptance Criteria:

A unit test must be written before the corresponding application code is implemented.
Each new feature or change must start with a failing test that passes once the feature is correctly implemented.
Unit tests must cover all core logic, including file hashing, directory traversal, and comparison logic.
Tests must include scenarios for found files, missing files, empty directories, and nested directory structures.
All tests must pass before the feature is considered complete.

