import os
import json
import tempfile
import unittest
from unittest.mock import patch, mock_open

from helix_data_loader.utils.config_loader import load_config


class TestConfigLoader(unittest.TestCase):
    """Tests for the configuration loading functionality."""
    
    def test_load_default_config(self):
        """Test loading the default configuration."""
        # Create a mock config file in the expected location
        with patch('os.path.exists') as mock_exists, \
             patch('builtins.open', mock_open(read_data='{"test": "value"}')):
            
            mock_exists.return_value = True
            config = load_config()
            
            self.assertEqual(config, {"test": "value"})
    
    def test_load_custom_config(self):
        """Test loading a custom configuration file."""
        # Create a temporary file with test configuration
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            test_config = {
                "api": {
                    "context_id": "test-context",
                    "api_key": "test-key",
                    "tenant_id": "test-tenant"
                },
                "defaults": {
                    "table_name": "test_table",
                    "threads": 2
                }
            }
            json.dump(test_config, temp_file)
            temp_file_path = temp_file.name
        
        try:
            # Test loading this custom config
            config = load_config(temp_file_path)
            self.assertEqual(config, test_config)
            self.assertEqual(config["api"]["context_id"], "test-context")
            self.assertEqual(config["defaults"]["table_name"], "test_table")
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    
    def test_nonexistent_config(self):
        """Test behavior when config file doesn't exist."""
        # Test with a non-existent file
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            config = load_config("/path/does/not/exist.json")
            
            # Should return empty dict
            self.assertEqual(config, {})
    
    def test_invalid_json(self):
        """Test behavior with invalid JSON."""
        # Test with invalid JSON content
        with patch('os.path.exists') as mock_exists, \
             patch('builtins.open', mock_open(read_data='{"invalid": json')):
            
            mock_exists.return_value = True
            config = load_config()
            
            # Should return empty dict
            self.assertEqual(config, {})


if __name__ == '__main__':
    unittest.main()