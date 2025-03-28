import unittest
from unittest.mock import patch, MagicMock
import time

from helix_data_loader.utils.transaction_meter import TransactionMeter


class TestTransactionMeter(unittest.TestCase):
    """Tests for the TransactionMeter class."""
    
    def setUp(self):
        """Set up for tests."""
        # Create a transaction meter with known values
        self.meter = TransactionMeter(total_lines=100, start_line=1, disable_progress_bar=True)
        # Reset its internals for consistent testing
        self.meter.total_transactions = 0
        self.meter.failed_transactions = 0
        self.meter.start_time = time.time()
        self.meter.record_count = 0
        self.meter.status_codes = {}
    
    def test_increment(self):
        """Test incrementing successful transactions."""
        # Single increment
        self.meter.increment()
        self.assertEqual(self.meter.total_transactions, 1)
        self.assertEqual(self.meter.record_count, 1)
        
        # Increment with count
        self.meter.increment(count=5)
        self.assertEqual(self.meter.total_transactions, 6)  # 1+5
        self.assertEqual(self.meter.record_count, 6)
        
        # Increment with status code
        self.meter.increment(status_code=201)
        self.assertEqual(self.meter.total_transactions, 7)
        self.assertEqual(self.meter.status_codes.get(201), 1)
        
        # Multiple increments with same status code
        self.meter.increment(status_code=201, count=2)
        self.assertEqual(self.meter.total_transactions, 9)
        self.assertEqual(self.meter.status_codes.get(201), 3)  # 1+2
    
    def test_increment_failure(self):
        """Test incrementing failed transactions."""
        # Single failure
        self.meter.increment_failure()
        self.assertEqual(self.meter.failed_transactions, 1)
        self.assertEqual(self.meter.record_count, 1)
        
        # Multiple failures
        self.meter.increment_failure(count=3)
        self.assertEqual(self.meter.failed_transactions, 4)  # 1+3
        self.assertEqual(self.meter.record_count, 4)
        
        # Failure with status code
        self.meter.increment_failure(status_code=404)
        self.assertEqual(self.meter.failed_transactions, 5)
        self.assertEqual(self.meter.status_codes.get(404), 1)
        
        # Multiple failures with same status code
        self.meter.increment_failure(status_code=404, count=2)
        self.assertEqual(self.meter.failed_transactions, 7)
        self.assertEqual(self.meter.status_codes.get(404), 3)  # 1+2
    
    def test_progress_calculation(self):
        """Test progress calculation."""
        # The progress bar is disabled in the setup for cleaner testing
        # So we need to enable it first
        self.meter.disable_progress_bar = False
        
        # Process 25% of records
        for _ in range(25):
            self.meter.increment()
        
        # Manually calculate what the progress percentage should be
        expected_percentage = 25.0  # 25%
        
        # Force a report with a non-blocking call
        with patch('sys.stdout.write') as mock_write:
            # Force the last_report_time to be older to ensure report triggers
            self.meter.last_report_time = time.time() - 2
            self.meter.report_if_needed()
            
            # Verify mock_write was called
            mock_write.assert_called()
            
            # Check if any call to write contains the expected percentage
            contains_percentage = False
            for call in mock_write.call_args_list:
                if "25.0%" in str(call):  # Look for the formatted percentage
                    contains_percentage = True
                    break
            self.assertTrue(contains_percentage)
    
    def test_status_code_tracking(self):
        """Test HTTP status code tracking."""
        # Add a mix of status codes
        self.meter.increment(status_code=200, count=50)  # Success
        self.meter.increment(status_code=201, count=10)  # Created
        self.meter.increment_failure(status_code=404, count=5)  # Not Found
        self.meter.increment_failure(status_code=500, count=2)  # Server Error
        
        # Check status code counts
        self.assertEqual(self.meter.status_codes.get(200), 50)
        self.assertEqual(self.meter.status_codes.get(201), 10)
        self.assertEqual(self.meter.status_codes.get(404), 5)
        self.assertEqual(self.meter.status_codes.get(500), 2)
        
        # Check total counts
        self.assertEqual(self.meter.total_transactions, 60)  # 50+10
        self.assertEqual(self.meter.failed_transactions, 7)  # 5+2
        self.assertEqual(self.meter.record_count, 67)  # 60+7


if __name__ == '__main__':
    unittest.main()