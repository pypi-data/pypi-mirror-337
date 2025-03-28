import sys
import os
import argparse
import uuid
from datetime import datetime

from .core import (
    process_csv_with_metering,
    process_jsonl_with_metering,
    count_lines,
    fetch_table_schema
)
from .utils.transaction_meter import TransactionMeter
from .utils.config_loader import load_config

def main():
    """
    Main entry point for the Helix Data Loader CLI.
    """
    start_time = datetime.now()
    sys.stdout.write(f"[START TIME: {start_time.strftime('%Y-%m-%d %H:%M:%S')}]\n")
    
    # Load configuration
    config = load_config()
    
    # Extract defaults from configuration
    default_api_key = config.get("api", {}).get("api_key", "")
    default_tenant_id = config.get("api", {}).get("tenant_id", "")
    default_table_name = config.get("defaults", {}).get("table_name", "")
    default_start_line = config.get("defaults", {}).get("start_line", 1)
    default_threads = config.get("defaults", {}).get("threads", 4)
    default_delete_mode = config.get("defaults", {}).get("delete_mode", False)
    default_debug = config.get("defaults", {}).get("debug", False)
    default_batch_size = config.get("performance", {}).get("batch_size", 499)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Data loader for Helix platform")
    parser.add_argument("--file",dest="file_path", help="Path to the input file (CSV or JSONL)")
    parser.add_argument("--table-name", dest="table_name", default=default_table_name,
                       help=f"Name of the table to load data into (default: {default_table_name or 'None'})")
    parser.add_argument("--start-line", type=int, default=default_start_line, 
                        help=f"Line number to start processing from (1-based, default: {default_start_line})")
    parser.add_argument("--api-key", default=default_api_key,
                       help="API key for authentication (default from config)")
    parser.add_argument("--tenant-id", default=default_tenant_id,
                       help="Tenant ID for authentication (default from config)")
    parser.add_argument("--threads", type=int, default=default_threads,
                      help=f"Number of threads to use (default: {default_threads})")
    parser.add_argument("--delete", action="store_true", default=default_delete_mode,
                      help=f"Delete mode: delete records using first column as primary key (default: {default_delete_mode})")
    parser.add_argument("--debug", action="store_true", default=default_debug,
                      help=f"Debug mode: print detailed request and response information (default: {default_debug})")
    parser.add_argument("--batch-size", type=int, default=default_batch_size,
                      help=f"Number of records to process in a single API call (1-499, default: {default_batch_size})")
    parser.add_argument("--config", help="Path to a custom configuration file")
    parser.add_argument("--version", action="store_true", help="Print version information and exit")
    args = parser.parse_args()
    
    # Check if version flag was provided
    if args.version:
        from . import __version__
        sys.stdout.write(f"Helix Data Loader version {__version__}\n")
        sys.exit(0)
    
    # If a custom config file is specified, reload the configuration
    if args.config:
        config = load_config(args.config)
        # Update values if they weren't explicitly provided as arguments
        if args.api_key == default_api_key:
            args.api_key = config.get("api", {}).get("api_key", args.api_key)
        if args.tenant_id == default_tenant_id:
            args.tenant_id = config.get("api", {}).get("tenant_id", args.tenant_id)
        if args.table_name == default_table_name:
            args.table_name = config.get("defaults", {}).get("table_name", args.table_name)
        if args.batch_size == default_batch_size:
            args.batch_size = config.get("performance", {}).get("batch_size", args.batch_size)
    
    # Validate required arguments
    if not args.file_path:
        sys.stderr.write("Error: file path is required. Provide it with --file argument.\n")
        sys.exit(1)
        
    if not args.table_name:
        sys.stderr.write("Error: table_name is required. Provide it as a command-line argument or in the config file.\n")
        sys.exit(1)
    
    # Extract arguments
    file_path = args.file_path
    table_name = args.table_name
    start_line = args.start_line
    num_threads = args.threads
    delete_mode = args.delete
    debug_mode = args.debug
    batch_size = args.batch_size
    
    # Ensure batch size is within limits (1-499)
    batch_size = min(499, max(1, batch_size))
    
    # Get API key from command line, config, or environment variable
    api_key = args.api_key
    
    # If API key wasn't provided via command line or config, check environment variable
    if not api_key:
        api_key = os.environ.get("HELIX_API_KEY", "")
        if api_key and debug_mode:
            sys.stdout.write("Using API key from HELIX_API_KEY environment variable\n")
    
    # Get tenant ID from command line, config, or environment variable
    tenant_id = args.tenant_id
    
    # If tenant ID wasn't provided via command line or config, check environment variable
    if not tenant_id:
        tenant_id = os.environ.get("HELIX_TENANT_ID", "")
        if tenant_id and debug_mode:
            sys.stdout.write("Using tenant ID from HELIX_TENANT_ID environment variable\n")
    
    # Generate a random UUID for context_id
    context_id = str(uuid.uuid4())
    if debug_mode:
        sys.stdout.write(f"Generated random context_id: {context_id}\n")
    
    # Validate essential API credentials
    if not api_key:
        sys.stderr.write("Error: api_key is required. Provide it as a command-line argument, in the config file, or set the HELIX_API_KEY environment variable.\n")
        sys.exit(1)
        
    if not tenant_id:
        sys.stderr.write("Error: tenant_id is required. Provide it as a command-line argument, in the config file, or set the HELIX_TENANT_ID environment variable.\n")
        sys.exit(1)
        
    # Fetch table schema (for namespace and version) - still required
    try:
        sys.stdout.write(f"Fetching schema information for table '{table_name}'...\n")
        table_schema = fetch_table_schema(table_name, api_key, tenant_id, debug_mode)
        
        if debug_mode:
            sys.stdout.write(f"Using tenant ID: {tenant_id}\n")
            sys.stdout.write(f"Using namespace from schema: {table_schema.get('namespace')}\n")
            sys.stdout.write(f"Using version from schema: {table_schema.get('version')}\n")
            
    except Exception as e:
        sys.stderr.write(f"Error: Could not fetch table schema: {str(e)}\n")
        sys.stderr.write("Schema information is required to determine the API endpoints.\n")
        sys.exit(1)
    
    # Count the lines in the file to track progress
    total_lines = count_lines(file_path, start_line)
    sys.stdout.write(f"Total {total_lines} lines.\n")
    sys.stdout.flush()
    
    # Initialize transaction meter with line count and start line
    transaction_meter = TransactionMeter(total_lines, start_line, disable_progress_bar=debug_mode)
    
    # Print start time first to avoid UI issues with progress bar
    mode_str = "DELETE" if delete_mode else "INSERT"
    sys.stdout.write(f"Running in {mode_str} mode with {num_threads} worker threads and batch size of {batch_size}\n")
    
    if delete_mode:
        sys.stdout.write(f"DELETE MODE: Will use first column as primary key for deletion\n")
        
    if debug_mode:
        sys.stdout.write(f"DEBUG MODE: Will print detailed request and response information\n")
        
    if start_line > 1:
        sys.stdout.write(f"Skipping the first {start_line-1} lines, starting at line {start_line}\n")
        
    try:
        if file_path.endswith('.csv'):
            process_csv_with_metering(file_path, table_name, context_id, tenant_id, api_key, transaction_meter, start_line, num_threads, delete_mode, debug_mode, table_schema, batch_size)
        
        elif file_path.endswith('.jsonl'):
            process_jsonl_with_metering(file_path, table_name, context_id, tenant_id, api_key, transaction_meter, start_line, num_threads, delete_mode, debug_mode, table_schema, batch_size)
        
        else:
            sys.stderr.write("Unsupported file format. Please provide a .csv or .jsonl file.\n")
            sys.stderr.flush()
    
    finally:
        if debug_mode:
            sys.stdout.write("\n[DEBUG] Processing complete, generating final report...\n")
            
        # Generate final report
        transaction_meter.final_report()
        
        # Print end time 
        end_time = datetime.now()
        elapsed = end_time - start_time
        elapsed_seconds = elapsed.total_seconds()
        
        # Format as HH:MM:SS
        hours, remainder = divmod(int(elapsed_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        sys.stdout.write(f"\nTotal run time: {elapsed_formatted} (total {int(elapsed_seconds):,} seconds)\n")
        sys.stdout.write(f"[END TIME: {end_time.strftime('%Y-%m-%d %H:%M:%S')}]\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()