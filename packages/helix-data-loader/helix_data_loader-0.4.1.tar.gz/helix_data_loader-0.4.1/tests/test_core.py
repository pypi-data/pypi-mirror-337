import unittest
from unittest.mock import patch, MagicMock, mock_open

from helix_data_loader.core import (
    process_data,
    process_data_batch,
    count_lines,
    process_row,
    fetch_table_schema
)


class TestCore(unittest.TestCase):
    """Tests for core functionality."""
    
    @patch('helix_data_loader.core.process_data_batch')
    def test_process_data(self, mock_batch):
        """Test processing a single data record."""
        # Set up test data
        test_data = {"id": "123", "name": "Test Record"}
        
        # Configure the mock to return a response-like object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_batch.return_value = mock_response
        
        # Call the function
        result = process_data(
            table_name="test_table",
            context_id="test-context",
            tenant_id="test-tenant",
            api_key="test-key",
            data=test_data,
            delete_mode=False,
            debug=False
        )
        
        # Check the result
        self.assertEqual(result.status_code, 200)
        
        # Verify process_data_batch was called correctly
        mock_batch.assert_called_once()
        args, kwargs = mock_batch.call_args
        
        # The function is using positional arguments, not keyword arguments
        # so we need to check the positional arguments
        self.assertEqual(args[0], "test_table")  # table_name
        self.assertEqual(args[4], [test_data])   # entity_data_list
        self.assertEqual(args[5], False)         # delete_mode
    
    @patch('helix_data_loader.core.requests.post')
    def test_process_data_batch_post(self, mock_post):
        """Test batch processing with POST."""
        # Set up test data
        test_records = [
            {"id": "123", "name": "Test Record 1"},
            {"id": "456", "name": "Test Record 2"}
        ]
        
        # Configure the mock to return a response-like object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Call the function
        result = process_data_batch(
            table_name="test_table",
            context_id="test-context",
            tenant_id="test-tenant",
            api_key="test-key",
            entity_data_list=test_records,
            delete_mode=False,
            debug=False
        )
        
        # Check the result
        self.assertEqual(result.status_code, 200)
        
        # Verify requests.post was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn("test_table", args[0])  # URL contains table name
        self.assertEqual(len(kwargs["json"]["entityData"]), 2)  # Has 2 records
        self.assertEqual(kwargs["headers"]["X-Tenant-Id"], "test-tenant")
    
    @patch('helix_data_loader.core.requests.delete')
    def test_process_data_batch_delete(self, mock_delete):
        """Test batch processing with DELETE."""
        # Set up test data for delete mode
        test_records = [
            {"id": "123"},
            {"id": "456"}
        ]
        
        # Configure the mock to return a response-like object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response
        
        # Call the function in delete mode
        result = process_data_batch(
            table_name="test_table",
            context_id="test-context",
            tenant_id="test-tenant",
            api_key="test-key",
            entity_data_list=test_records,
            delete_mode=True,
            debug=False
        )
        
        # Check the result
        self.assertEqual(result.status_code, 200)
        
        # Verify requests.delete was called correctly
        mock_delete.assert_called_once()
        args, kwargs = mock_delete.call_args
        self.assertIn("delete", args[0])  # URL contains "delete"
        self.assertEqual(len(kwargs["json"]["entityData"]), 2)  # Has 2 records
    
    def test_count_lines_csv(self):
        """Test counting lines in a CSV file."""
        # Mock file content for a CSV file (with header)
        mock_csv_content = "id,name,value\n1,test1,100\n2,test2,200\n3,test3,300"
        
        with patch('builtins.open', mock_open(read_data=mock_csv_content)), \
             patch('helix_data_loader.core.os.path.exists', return_value=True):
            
            # Count lines from the beginning
            count = count_lines("test.csv", start_line=1)
            self.assertEqual(count, 3)  # 3 data lines (excluding header)
            
            # Count lines starting from line 2
            count = count_lines("test.csv", start_line=2)
            self.assertEqual(count, 2)  # 2 data lines (starting from the 2nd data line)
    
    def test_count_lines_jsonl(self):
        """Test counting lines in a JSONL file."""
        # Mock file content for a JSONL file
        mock_jsonl_content = '{"id": 1, "name": "test1"}\n{"id": 2, "name": "test2"}\n{"id": 3, "name": "test3"}'
        
        with patch('builtins.open', mock_open(read_data=mock_jsonl_content)), \
             patch('helix_data_loader.core.os.path.exists', return_value=True):
            
            # Count lines from the beginning
            count = count_lines("test.jsonl", start_line=1)
            self.assertEqual(count, 3)  # 3 lines total
            
            # Count lines starting from line 2
            count = count_lines("test.jsonl", start_line=2)
            self.assertEqual(count, 2)  # 2 lines (skipping the first)
    
    @patch('helix_data_loader.core.requests.get')
    def test_fetch_table_schema(self, mock_get):
        """Test fetching table schema with the latest=true parameter."""
        # Mock response data for the optimized endpoint
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "test_table",
            "tenantId": "test-tenant-id",
            "namespace": "/custom",
            "version": "3",
            "schemas": {
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        }
        mock_get.return_value = mock_response
        
        # Call the function
        schema = fetch_table_schema(
            table_name="test_table",
            api_key="test-key",
            debug=False
        )
        
        # Verify the results
        self.assertEqual(schema["name"], "test_table")
        self.assertEqual(schema["tenantId"], "test-tenant-id")
        self.assertEqual(schema["namespace"], "/custom")
        self.assertEqual(schema["version"], "3")
        
        # Verify the request was made correctly with latest=true parameter
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://openam-helix.forgeblocks.com/dpc/jas/entityDefinitions/test_table?latest=true")
        self.assertEqual(kwargs["headers"]["x-api-key"], "test-key")
    
    @patch('helix_data_loader.core.requests.post')
    def test_process_data_batch_with_schema(self, mock_post):
        """Test batch processing with schema information."""
        # Set up test data
        test_records = [
            {"id": "123", "name": "Test Record 1"},
            {"id": "456", "name": "Test Record 2"}
        ]
        
        # Set up schema information
        test_schema = {
            "tenantId": "schema-tenant-id",
            "namespace": "/custom",
            "version": "3"
        }
        
        # Configure the mock to return a response-like object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Call the function with schema
        result = process_data_batch(
            table_name="test_table",
            context_id="test-context",
            tenant_id=None,  # Should be taken from schema
            api_key="test-key",
            entity_data_list=test_records,
            delete_mode=False,
            debug=False,
            table_schema=test_schema
        )
        
        # Check the result
        self.assertEqual(result.status_code, 200)
        
        # Verify requests.post was called correctly with schema-based URL
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # URL should use namespace and version from schema
        self.assertIn("/custom/test_table/3", args[0])
        
        # Headers should use tenant ID from schema
        self.assertEqual(kwargs["headers"]["X-Tenant-Id"], "schema-tenant-id")


if __name__ == '__main__':
    unittest.main()