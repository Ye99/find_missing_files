import runpy
import pytest
from unittest import mock

def test_main_module_invokes_cli_main(tmp_path):
    """
    Tests if running the package as a module correctly invokes cli.main.
    We don't need to test cli.main's functionality here, just that it's called.
    We also need to provide dummy arguments for subset_dir and superset_dir
    because cli.main expects them, even though their actual values don't matter
    for this specific test of the __main__ module's dispatch.
    """
    # Create dummy directories as cli.main expects paths that exist
    subset_dir = tmp_path / "subset_dummy"
    superset_dir = tmp_path / "superset_dummy"
    subset_dir.mkdir()
    superset_dir.mkdir()

    # Mock sys.argv because runpy will use the test runner's args otherwise
    # and cli.main (via click) will try to parse them.
    # We provide the module name and two dummy paths.
    with mock.patch('sys.argv', ['missing_file_finder', str(subset_dir), str(superset_dir)]):
        with mock.patch('missing_file_finder.cli.main') as mock_cli_main:
            # Execute missing_file_finder as the main module
            # This simulates `python -m missing_file_finder <args>`
            runpy.run_module('missing_file_finder', run_name='__main__')
            
            # Assert that cli.main was called
            mock_cli_main.assert_called_once() 