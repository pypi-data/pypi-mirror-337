import sys
import time
import threading
from datetime import datetime

class TransactionMeter:
    """
    Tracks and reports transactions per minute with completion percentage and failures.
    Thread-safe implementation for concurrent processing.
    """
    def __init__(self, total_lines=0, start_line=1, disable_progress_bar=False):
        self.total_transactions = 0
        self.failed_transactions = 0
        self.start_time = time.time()
        self.last_report_time = self.start_time
        self.transactions_since_last_report = 0
        self.failures_since_last_report = 0
        self.report_interval = 1  # Report every 1 second
        self.total_lines = total_lines  # Total number of lines to process
        self.start_line = start_line  # Starting line number (1-based)
        self.disable_progress_bar = disable_progress_bar  # Whether to disable the progress bar
        
        # For progress calculation, we need to know how many lines we're processing
        self.lines_to_process = total_lines
        
        # Progress tracking - needed for batch processing
        self.record_count = 0  # Total records processed (for progress tracking)
        
        # Track HTTP status codes
        self.status_codes = {}  # Dict to track count of each status code
        
        # Add locks for thread safety
        self.transaction_lock = threading.Lock()
        self.report_lock = threading.Lock()
    
    def increment(self, status_code=200, count=1):
        """
        Increment successful transaction count and track status code. Thread-safe.
        
        Args:
            status_code (int): HTTP status code of the response
            count (int): Number of records processed (default: 1, for batch operations can be > 1)
        """
        with self.transaction_lock:
            self.total_transactions += count
            self.transactions_since_last_report += count
            # Update record count for progress tracking
            self.record_count += count
            
            # Track status code
            if status_code in self.status_codes:
                self.status_codes[status_code] += count
            else:
                self.status_codes[status_code] = count
                
        self.report_if_needed()
        
    def increment_failure(self, status_code=None, count=1):
        """
        Increment failed transaction count and track status code. Thread-safe.
        
        Args:
            status_code (int, optional): HTTP status code of the failed response
            count (int): Number of records that failed (default: 1, for batch operations can be > 1)
        """
        with self.transaction_lock:
            self.failed_transactions += count
            self.failures_since_last_report += count
            # Update record count for progress tracking
            self.record_count += count
            
            # Track status code if provided
            if status_code is not None:
                if status_code in self.status_codes:
                    self.status_codes[status_code] += count
                else:
                    self.status_codes[status_code] = count
                    
        self.report_if_needed()
    
    def create_progress_bar(self, percentage, width=50):
        """Create a text-based progress bar."""
        filled_width = int(width * percentage / 100)
        bar = '█' * filled_width + '░' * (width - filled_width)
        return bar
    
    def report_if_needed(self):
        """Report transactions per minute with a progress bar. Thread-safe."""
        current_time = time.time()
        elapsed_since_report = current_time - self.last_report_time
        
        # Use non-blocking check first to avoid lock contention
        if elapsed_since_report >= self.report_interval and self.report_lock.acquire(False):
            try:
                # Double-check after acquiring lock
                current_time = time.time()
                elapsed_since_report = current_time - self.last_report_time
                
                if elapsed_since_report < self.report_interval:
                    # Another thread already reported recently
                    return
                    
                # Copy values under transaction lock to ensure consistency
                with self.transaction_lock:
                    transactions_since_report = self.transactions_since_last_report
                    total_transactions = self.total_transactions
                    failed_transactions = self.failed_transactions
                    self.transactions_since_last_report = 0
                    self.last_report_time = current_time
                
                # If progress bar is disabled (debug mode), just update internal state
                # and provide a simple counter update every 10 transactions
                if self.disable_progress_bar:
                    # Only print status every 10 transactions to avoid too much output
                    if (total_transactions + failed_transactions) % 10 == 0:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sys.stdout.write(f"[{timestamp}] Progress: {total_transactions} successful, {failed_transactions} failed\n")
                        sys.stdout.flush()
                    return
                
                # Calculate transactions per minute
                tpm = (transactions_since_report / elapsed_since_report) * 60
                total_elapsed_seconds = current_time - self.start_time
                
                # Format elapsed time as HH:MM:SS
                hours, remainder = divmod(int(total_elapsed_seconds), 3600)
                minutes, seconds = divmod(remainder, 60)
                elapsed_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                # Initialize progress bar data
                percentage = 0
                remaining_formatted = "00:00:00"
                progress_bar = ""
                
                # Calculate completion percentage if total lines is known
                if self.total_lines > 0:
                    # Use record_count for more accurate progress in batch processing
                    record_count = total_transactions + failed_transactions
                    percentage = min(100, (record_count / self.lines_to_process) * 100)
                
                    # Create progress bar
                    progress_bar = self.create_progress_bar(percentage)
                
                    # Estimate time remaining
                    if percentage > 0:
                        elapsed_seconds = current_time - self.start_time
                        total_estimated_seconds = (elapsed_seconds / percentage) * 100
                        remaining_seconds = total_estimated_seconds - elapsed_seconds
                        
                        # Format remaining time as HH:MM:SS
                        r_hours, r_remainder = divmod(int(remaining_seconds), 3600)
                        r_minutes, r_seconds = divmod(r_remainder, 60)
                        remaining_formatted = f"{r_hours:02d}:{r_minutes:02d}:{r_seconds:02d}"
                
                # Clear the current line and create progress output
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Build the status line
                if self.total_lines > 0:
                    # Calculate error rate
                    attempts = total_transactions + failed_transactions
                    error_rate = (failed_transactions / attempts) * 100 if attempts > 0 else 0
                    error_display = f"Err: {error_rate:.1f}%" if failed_transactions > 0 else "No errors"
                    
                    # Get total records processed (success + failures)
                    record_count = total_transactions + failed_transactions
                    
                    status = (f"\r[{timestamp}] {progress_bar} {percentage:.1f}% | "
                             f"{record_count}/{self.total_lines} records | "
                             f"{tpm:.1f} tpm | {error_display} | ETA: {remaining_formatted}")
                    
                    if failed_transactions > 0:
                        status += f" | Errors: {failed_transactions}/{attempts}"
                else:
                    # Get total records processed
                    record_count = total_transactions + failed_transactions
                    error_rate = (failed_transactions / record_count) * 100 if record_count > 0 else 0
                    status = (f"\r[{timestamp}] {total_transactions} succeeded | "
                             f"{failed_transactions} failed ({error_rate:.1f}% error rate) | "
                             f"{record_count} total records | {tpm:.1f} tpm | Elapsed: {elapsed_formatted}")
                
                # Print the status line without line break
                sys.stdout.write(status)
                sys.stdout.flush()
            
            finally:
                # Always release the lock
                self.report_lock.release()
    
    def final_report(self):
        """Generate final metrics report."""
        # Always print a prominent header to make the final report more visible
        sys.stdout.write("\n\n=================================================================\n")
        sys.stdout.write("                          FINAL REPORT                          \n")
        sys.stdout.write("=================================================================\n")
        sys.stdout.flush()
        
        # Different spacing based on whether progress bar was used
        if not self.disable_progress_bar:
            # Need a newline to move below the progress bar
            sys.stdout.write("\n")
            sys.stdout.flush()
            # Add a spacing newline before the report header
            newline_prefix = "\n"
        else:
            # In debug mode (no progress bar), just add a single divider line
            newline_prefix = "\n"
        
        # Ensure we have the latest values
        with self.transaction_lock:
            total_transactions = self.total_transactions
            failed_transactions = self.failed_transactions
            record_count = self.record_count
            status_codes_copy = self.status_codes.copy()  # Make a copy of status codes
            
        # Debug information about transaction counts
        sys.stdout.write(f"DEBUG: Total successful records: {total_transactions}\n")
        sys.stdout.write(f"DEBUG: Failed records: {failed_transactions}\n") 
        sys.stdout.write(f"DEBUG: Total records processed: {record_count}\n")
        sys.stdout.write(f"DEBUG: Status codes tracked: {status_codes_copy}\n")
        sys.stdout.flush()
            
        if total_transactions == 0 and failed_transactions == 0:
            sys.stdout.write("No transactions processed.\n")
            sys.stdout.flush()
            return
            
        total_elapsed = time.time() - self.start_time
        total_elapsed_minutes = total_elapsed / 60
        
        # Calculate total records for metrics
        total_records = total_transactions + failed_transactions
        
        # Calculate overall throughput based on total records
        overall_tpm = (total_records / total_elapsed) * 60 if total_elapsed > 0 else 0
        
        # Format elapsed time as HH:MM:SS
        hours, remainder = divmod(int(total_elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Calculate completion percentage
        completion_info = ""
        progress_bar = ""
        if self.total_lines > 0:
            # Calculate total records processed
            record_count = total_transactions + failed_transactions
            percentage = min(100, (record_count / self.lines_to_process) * 100)
            progress_bar = self.create_progress_bar(percentage)
            completion_info = f" ({percentage:.1f}% of {self.total_lines} records)"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write(f"{newline_prefix}[{timestamp}] FINAL METRICS:\n")
        
        if self.total_lines > 0:
            sys.stdout.write(f"{completion_info}\n")
            
        sys.stdout.write(f"Successful records            : {total_transactions:,}\n")
        
        if failed_transactions > 0:
            error_rate = (failed_transactions / total_records) * 100
            success_rate = 100 - error_rate
            sys.stdout.write(f"Failed records                : {failed_transactions:,} ({error_rate:.2f}% error rate)\n")
            sys.stdout.write(f"Success rate                  : {success_rate:.2f}% ({total_transactions:,}/{total_records:,})\n")
        
        sys.stdout.write(f"Total records processed       : {total_records:,}\n")
        
        # Display HTTP status code breakdown
        if status_codes_copy:
            sys.stdout.write("\nHTTP Status Code Breakdown:\n")
            sys.stdout.write("-------------------------\n")
            
            # For calculating percentages
            total_attempts = sum(status_codes_copy.values())
            
            # Group status codes by category
            success_codes = {k: v for k, v in status_codes_copy.items() if 200 <= k < 300}
            redirect_codes = {k: v for k, v in status_codes_copy.items() if 300 <= k < 400}
            client_error_codes = {k: v for k, v in status_codes_copy.items() if 400 <= k < 500}
            server_error_codes = {k: v for k, v in status_codes_copy.items() if 500 <= k < 600}
            other_codes = {k: v for k, v in status_codes_copy.items() if (isinstance(k, int) and (k < 200 or k >= 600)) or not isinstance(k, int)}
            
            # Display success codes (2xx)
            if success_codes:
                total_success = sum(success_codes.values())
                sys.stdout.write(f"Success (2xx)        : {total_success:,} total\n")
                for code, count in sorted(success_codes.items()):
                    percentage = (count / total_attempts) * 100
                    sys.stdout.write(f"  {code}                : {count:,} ({percentage:.1f}%)\n")
            
            # Display redirect codes (3xx)
            if redirect_codes:
                total_redirect = sum(redirect_codes.values())
                sys.stdout.write(f"Redirect (3xx)       : {total_redirect:,} total\n")
                for code, count in sorted(redirect_codes.items()):
                    percentage = (count / total_attempts) * 100
                    sys.stdout.write(f"  {code}                : {count:,} ({percentage:.1f}%)\n")
            
            # Display client error codes (4xx)
            if client_error_codes:
                total_client_error = sum(client_error_codes.values())
                sys.stdout.write(f"Client Error (4xx)   : {total_client_error:,} total\n")
                for code, count in sorted(client_error_codes.items()):
                    percentage = (count / total_attempts) * 100
                    sys.stdout.write(f"  {code}               : {count:,} ({percentage:.1f}%)\n")
            
            # Display server error codes (5xx)
            if server_error_codes:
                total_server_error = sum(server_error_codes.values())
                sys.stdout.write(f"Server Error (5xx)   : {total_server_error:,} total\n")
                for code, count in sorted(server_error_codes.items()):
                    percentage = (count / total_attempts) * 100
                    sys.stdout.write(f"  {code}               : {count:,} ({percentage:.1f}%)\n")
            
            # Display other codes
            if other_codes:
                total_other = sum(other_codes.values())
                sys.stdout.write(f"Other Status Codes   : {total_other:,} total\n")
                for code, count in sorted(other_codes.items()):
                    percentage = (count / total_attempts) * 100
                    sys.stdout.write(f"  {code}               : {count:,} ({percentage:.1f}%)\n")
        
        sys.stdout.write(f"\nProcessing time                : {elapsed_formatted} (total {int(total_elapsed):,} seconds)\n")
        sys.stdout.write(f"Overall records per minute     : {overall_tpm:.2f} ({int(overall_tpm/60):.1f}/second)\n")
        sys.stdout.flush()