import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import os

from helix_data_loader.cli import main
from helix_data_loader.utils.transaction_meter import TransactionMeter


class TestCLI(unittest.TestCase):
    """Tests for the CLI interface."""
    
    def test_main_with_csv(self):
        """Test the main function with a CSV file."""
        # Configure mocks
        with patch('helix_data_loader.cli.load_config') as mock_load_config, \
             patch('helix_data_loader.cli.process_csv_with_metering') as mock_process_csv, \
             patch('helix_data_loader.cli.count_lines') as mock_count_lines, \
             patch('helix_data_loader.cli.sys.exit') as mock_exit, \
             patch('helix_data_loader.cli.uuid.uuid4', return_value='test-uuid'), \
             patch('helix_data_loader.cli.fetch_table_schema', return_value={"tenantId": "test-tenant", "namespace": "/test", "version": "1"}), \
             patch('helix_data_loader.cli.sys.argv', ['helix-data-loader', '--file', 'test.csv', '--table-name', 'test_table']):
            
            mock_config = {
                "api": {
                    "api_key": "test-key"
                },
                "defaults": {
                    "threads": 4,
                    "debug": False
                }
            }
            mock_load_config.return_value = mock_config
            mock_count_lines.return_value = 100
            
            # Capture stdout and stderr
            captured_stdout = io.StringIO()
            captured_stderr = io.StringIO()
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            
            try:
                sys.stdout = captured_stdout
                sys.stderr = captured_stderr
                
                # Call the main function - sys.exit is mocked to prevent actual exit
                main()
                    
            finally:
                # Restore stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr
            
            # Verify processing was attempted
            mock_process_csv.assert_called_once()
            
            # Check that output contains expected information
            stdout = captured_stdout.getvalue()
            self.assertIn("Total 100 lines", stdout)
            self.assertIn("INSERT", stdout)  # Default mode
    
    def test_main_with_jsonl_delete(self):
        """Test the main function with a JSONL file in delete mode."""
        # Configure mocks
        with patch('helix_data_loader.cli.load_config') as mock_load_config, \
             patch('helix_data_loader.cli.process_jsonl_with_metering') as mock_process_jsonl, \
             patch('helix_data_loader.cli.count_lines') as mock_count_lines, \
             patch('helix_data_loader.cli.sys.exit') as mock_exit, \
             patch('helix_data_loader.cli.uuid.uuid4', return_value='test-uuid'), \
             patch('helix_data_loader.cli.fetch_table_schema', return_value={"tenantId": "test-tenant", "namespace": "/test", "version": "1"}), \
             patch('helix_data_loader.cli.sys.argv', ['helix-data-loader', '--file', 'test.jsonl', '--table-name', 'test_table', '--delete']):
            
            mock_config = {
                "api": {
                    "api_key": "test-key"
                },
                "defaults": {
                    "threads": 4,
                    "debug": False
                }
            }
            mock_load_config.return_value = mock_config
            mock_count_lines.return_value = 100
            
            # Capture stdout and stderr
            captured_stdout = io.StringIO()
            captured_stderr = io.StringIO()
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            
            try:
                sys.stdout = captured_stdout
                sys.stderr = captured_stderr
                
                # Call the main function - sys.exit is mocked to prevent actual exit
                main()
                    
            finally:
                # Restore stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr
            
            # Verify jsonl processing was attempted
            mock_process_jsonl.assert_called_once()
            
            # Check that output contains expected information
            stdout = captured_stdout.getvalue()
            self.assertIn("Total 100 lines", stdout)
            self.assertIn("DELETE", stdout)  # Delete mode
    
    def test_version_flag(self):
        """Test the --version flag."""
        # Configure mock
        with patch('helix_data_loader.cli.load_config') as mock_load_config, \
             patch('helix_data_loader.__version__', '0.1.0'), \
             patch('helix_data_loader.cli.sys.exit') as mock_exit, \
             patch('helix_data_loader.cli.TransactionMeter'), \
             patch('helix_data_loader.cli.count_lines') as mock_count, \
             patch('helix_data_loader.cli.fetch_table_schema'), \
             patch('helix_data_loader.cli.sys.argv', ['helix-data-loader', '--version']):
            
            mock_load_config.return_value = {
                "api": {
                    "api_key": "test-key"
                }
            }
            mock_exit.side_effect = SystemExit  # Make it actually exit the function when called
            
            # Capture stdout
            captured_stdout = io.StringIO()
            original_stdout = sys.stdout
            
            try:
                sys.stdout = captured_stdout
                
                # Call the main function - this should exit early
                with self.assertRaises(SystemExit):
                    main()
                    
            finally:
                # Restore stdout
                sys.stdout = original_stdout
            
            # Check that version information was printed
            stdout = captured_stdout.getvalue()
            self.assertIn("Helix Data Loader version", stdout)


    def test_api_key_from_env(self):
        """Test getting API key from environment variable."""
        # Configure mocks
        with patch('helix_data_loader.cli.load_config') as mock_load_config, \
             patch('helix_data_loader.cli.process_csv_with_metering') as mock_process_csv, \
             patch('helix_data_loader.cli.count_lines') as mock_count_lines, \
             patch('helix_data_loader.cli.sys.exit') as mock_exit, \
             patch('helix_data_loader.cli.uuid.uuid4', return_value='test-uuid'), \
             patch('helix_data_loader.cli.fetch_table_schema', return_value={"tenantId": "test-tenant", "namespace": "/test", "version": "1"}), \
             patch.dict(os.environ, {"HELIX_API_KEY": "env-test-key"}), \
             patch('helix_data_loader.cli.sys.argv', ['helix-data-loader', '--file', 'test.csv', '--table-name', 'test_table']):
            
            # Config without API key
            mock_config = {
                "api": {},
                "defaults": {
                    "threads": 4,
                    "debug": False
                }
            }
            mock_load_config.return_value = mock_config
            mock_count_lines.return_value = 100
            
            # Capture stdout and stderr
            captured_stdout = io.StringIO()
            captured_stderr = io.StringIO()
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            
            try:
                sys.stdout = captured_stdout
                sys.stderr = captured_stderr
                
                # Call the main function - sys.exit is mocked to prevent actual exit
                main()
                    
            finally:
                # Restore stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr
            
            # Verify fetch_table_schema was called with the environment variable API key
            args, _ = mock_process_csv.call_args
            # process_csv_with_metering(file_path, table_name, context_id, tenant_id, api_key, transaction_meter, start_line, num_threads, delete_mode, debug_mode, table_schema)
            # api_key is the 5th positional argument
            self.assertEqual(args[4], "env-test-key")
            
            # Check that output contains expected information
            stdout = captured_stdout.getvalue()
            self.assertIn("Total 100 lines", stdout)


if __name__ == '__main__':
    unittest.main()