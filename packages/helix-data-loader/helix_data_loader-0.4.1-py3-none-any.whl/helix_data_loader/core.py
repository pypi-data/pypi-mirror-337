import json
import requests
import uuid
import time
import sys
import os
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from .utils.transaction_meter import TransactionMeter
from .utils.config_loader import load_config

def fetch_table_schema(table_name, api_key, tenant_id, debug=False):
    """
    Fetch schema information for a specific table from the Helix API.
    
    Args:
        table_name (str): The name of the table to fetch schema for
        api_key (str): API key for authentication
        tenant_id (str): Tenant ID for authentication
        debug (bool): Whether to print debug information
        
    Returns:
        dict: A dictionary containing table information including namespace and version
    """
    # Build URL to get all schemas
    api_url = "https://openam-helix.forgeblocks.com/dpc/jas/entityDefinitions"
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "X-Tenant-Id": tenant_id
    }
    
    # Print debug information if requested
    if debug:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write(f"\n[{timestamp}] [DEBUG] Fetching schemas from API:\n")
        sys.stdout.write(f"  URL    : {api_url}\n")
        sys.stdout.write(f"  Headers: {headers}\n")
        sys.stdout.flush()
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response - API returns an array of all schema definitions
        all_schemas = response.json()
        
        if not isinstance(all_schemas, list):
            raise ValueError(f"Expected an array of schemas but got {type(all_schemas)}")
            
        if debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sys.stdout.write(f"[{timestamp}] [DEBUG] Retrieved {len(all_schemas)} schema definitions\n")
            sys.stdout.flush()
        
        # Filter schemas for the requested table name
        matching_schemas = [schema for schema in all_schemas if schema.get("name") == table_name]
        
        if not matching_schemas:
            raise ValueError(f"No schema found for table '{table_name}'")
            
        if debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sys.stdout.write(f"[{timestamp}] [DEBUG] Found {len(matching_schemas)} versions of schema for table '{table_name}'\n")
            sys.stdout.flush()
        
        # Find the schema with the highest version number
        latest_schema = max(matching_schemas, key=lambda s: int(s.get("version", 0)))
        
        # Verify that the schema has the required properties
        if not latest_schema or not latest_schema.get("schemas", {}).get("properties"):
            raise ValueError(f"Table '{table_name}' schema does not contain required properties")
            
        # Make sure we have the essential fields needed
        if not latest_schema.get("namespace") or not latest_schema.get("version"):
            raise ValueError(f"Table '{table_name}' schema is missing essential fields (namespace or version)")
        
        if debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sys.stdout.write(f"[{timestamp}] [DEBUG] Found latest schema for table '{table_name}'\n")
            sys.stdout.write(f"  Tenant ID: {tenant_id}\n")
            sys.stdout.write(f"  Namespace: {latest_schema.get('namespace')}\n")
            sys.stdout.write(f"  Version: {latest_schema.get('version')}\n")
            sys.stdout.flush()
        
        return latest_schema
        
    except ValueError as ve:
        # Re-raise ValueError errors for more specific handling
        sys.stderr.write(f"Error with schema data: {str(ve)}\n")
        sys.stderr.flush()
        raise
        
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"Error fetching schema information: {e}\n")
        if hasattr(e, 'response') and e.response is not None:
            sys.stderr.write(f"Response: {e.response.status_code}, {e.response.text}\n")
        sys.stderr.flush()
        raise

def process_data(table_name=None, context_id=None, tenant_id=None, api_key=None, data=None, delete_mode=False, debug=False, table_schema=None):
    """
    Processes a single data record by either uploading to or deleting from the API.

    Args:
        table_name (str): Name of the table.
        context_id (str): Context ID to use in the payload.
        tenant_id (str): Tenant ID for the API call (optional if table_schema is provided).
        api_key (str): API key for authentication.
        data (dict): Dictionary containing the data to process.
        delete_mode (bool): If True, deletes the record instead of inserting/updating it.
        debug (bool): If True, prints detailed request and response information.
        table_schema (dict): Optional table schema information.
    """
    # Create entity_data for a single record
    if delete_mode:
        # In delete mode, we use the first column/field as the primary key
        if not data or not list(data.keys()):
            raise ValueError("No data provided for deletion")
        
        primary_key_field = list(data.keys())[0]
        primary_key_value = data[primary_key_field]
        
        if not primary_key_value:
            raise ValueError(f"Primary key value is empty: {primary_key_field}")
            
        # Create entity data with just the primary key
        entity_data = {primary_key_field: primary_key_value}
    else:
        # Preserve the original data
        entity_data = {}
        for key, value in data.items():
            entity_data[key] = value
    
    # Call the batch processing function with just one record
    return process_data_batch(table_name, context_id, tenant_id, api_key, [entity_data], delete_mode, debug, table_schema)

def process_data_batch(table_name=None, context_id=None, tenant_id=None, api_key=None, entity_data_list=None, delete_mode=False, debug=False, table_schema=None):
    """
    Processes multiple data records in a single batch by either uploading to or deleting from the API.

    Args:
        table_name (str): Name of the table.
        context_id (str): Context ID to use in the payload.
        tenant_id (str): Tenant ID for the API call.
        api_key (str): API key for authentication.
        entity_data_list (list): List of dictionaries containing the data to process.
        delete_mode (bool): If True, deletes the records instead of inserting/updating them.
        debug (bool): If True, prints detailed request and response information.
        table_schema (dict): Table schema information containing namespace and version.
    """
    if not entity_data_list:
        raise ValueError("No data provided for processing")
        
    # Get namespace and version from table schema
    namespace = table_schema.get("namespace")
    version = table_schema.get("version")
    
    if debug:
        sys.stdout.write(f"Using schema information: namespace={namespace}, version={version}\n")
        
    # Build the URL using the namespace and version from the schema
    if delete_mode:
        api_url = f"https://openam-helix.forgeblocks.com/dpc/jas/entity/delete{namespace}/{table_name}/{version}"
    else:
        api_url = f"https://openam-helix.forgeblocks.com/dpc/jas/entity/persist{namespace}/{table_name}/{version}"
    # Create the payload with all entity data
    payload = {
        "branch": "actual",
        "contextId": context_id,
        "entityData": entity_data_list,  # Include all records in the batch
        "indexingRequired": True,
        "tags": {},
        "indexInSync": True
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept":"application/json, text/plain, */*",
        "x-api-key": api_key,
        "X-Tenant-Id": tenant_id
    }
    
    # Print debug information if requested
    if debug:
        http_method = "DELETE" if delete_mode else "POST"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stdout.write(f"\n[{timestamp}] [DEBUG] Batch Request details ({len(entity_data_list)} records):\n")
        sys.stdout.write(f"  HTTP Method: {http_method}\n")
        sys.stdout.write(f"  URL: {api_url}\n")
        sys.stdout.write(f"  Headers: {json.dumps(headers, indent=2)}\n")
        
        # Print a summarized version of the payload for debug to avoid excessive output
        debug_payload = payload.copy()
        if len(entity_data_list) > 5:
            debug_payload["entityData"] = entity_data_list[:3] + ["... and " + str(len(entity_data_list)-3) + " more records"]
        sys.stdout.write(f"  Payload (summarized): {json.dumps(debug_payload, indent=2)}\n")
        sys.stdout.write(f"  Total records in batch: {len(entity_data_list)}\n")
        sys.stdout.write("-----------------------------------------------------------\n")  # Separator line
        sys.stdout.flush()
    
    try:
        if delete_mode:
            response = requests.delete(api_url, json=payload, headers=headers)
            action = "deleting"
        else:
            response = requests.post(api_url, json=payload, headers=headers)
            action = "posting"
            
        # Print debug response information if requested
        if debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sys.stdout.write(f"[{timestamp}] [DEBUG] Response details for batch of {len(entity_data_list)} records:\n")
            sys.stdout.write(f"  Status code: {response.status_code}\n")
            sys.stdout.write(f"  Response body: {response.text}\n")
            sys.stdout.write(f"  Headers: {json.dumps(dict(response.headers), indent=2)}\n")  # Include response headers
            sys.stdout.write("-----------------------------------------------------------\n")  # Separator line
            sys.stdout.flush()
            
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response  # Return the response object for status code tracking
    except requests.exceptions.RequestException as e:
        http_method = "DELETE" if delete_mode else "POST"
        error_msg = f"Error {action} data with {http_method}: {e}\n"
        sys.stderr.write(error_msg)
        sys.stderr.write(f"Failed batch with {len(entity_data_list)} records\n")
        if hasattr(e, 'response') and e.response is not None:
            sys.stderr.write(f"Response: {e.response.status_code}, {e.response.text}\n")
        else:
            sys.stderr.write("No Response received.\n")  
        sys.stderr.flush()
        # Re-raise the exception to be caught by the calling function
        raise Exception(error_msg) from e

def count_lines(file_path, start_line=1):
    """
    Count the number of non-empty lines in a file from the start_line to the end.
    
    Args:
        file_path (str): Path to the file
        start_line (int): Line number to start counting from (1-based)
        
    Returns:
        int: Number of non-empty lines in the file from start_line
    """
    try:
        # Check if the file is a CSV or JSONL to handle appropriately
        if file_path.endswith('.csv'):
            import csv
            # For CSV files, we need to parse as CSV and check each row
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                csv_reader = csv.reader(file, quotechar='"', delimiter=',')
                
                # Skip header row
                header = next(csv_reader, None)
                if not header:
                    return 0  # Empty file
                
                # Skip rows until we reach start_line (adjust since we already skipped header)
                for _ in range(max(0, start_line - 1)):
                    next(csv_reader, None)
                
                # Count non-empty rows
                non_empty_count = 0
                for row in csv_reader:
                    # Check if the row has at least one non-empty value
                    if any(field.strip() for field in row):
                        non_empty_count += 1
                
                return non_empty_count
                
        elif file_path.endswith('.jsonl'):
            # For JSONL files, check each line for valid JSON with data
            import json
            non_empty_count = 0
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                # Skip lines until we reach start_line
                for _ in range(max(0, start_line - 1)):
                    next(file, None)
                
                # Count non-empty JSON lines
                for line in file:
                    try:
                        data = json.loads(line)
                        # Check if the JSON object has at least one non-empty value
                        if data and any(value for value in data.values()):
                            non_empty_count += 1
                    except json.JSONDecodeError:
                        # Skip invalid JSON lines
                        continue
            
            return non_empty_count
        else:
            # For other file types, just count lines (fallback)
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                # Skip lines until we reach start_line
                for _ in range(max(0, start_line - 1)):
                    next(file, None)
                
                # Count remaining non-empty lines
                non_empty_count = sum(1 for line in file if line.strip())
                return non_empty_count
    
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {file_path}\n")
        sys.stderr.flush()
        return 0
    except Exception as e:
        sys.stderr.write(f"Error counting lines: {e}\n")
        sys.stderr.flush()
        return 0

def process_data_with_metering(meter, table_name=None, context_id=None, tenant_id=None, api_key=None, data=None, delete_mode=False, debug=False, table_schema=None):
    """Wrapper for process_data that increments the transaction meter."""
    try:
        response = process_data(table_name, context_id, tenant_id, api_key, data, delete_mode, debug, table_schema)
        # Increment success counter with the status code if available
        if hasattr(response, 'status_code'):
            status_code = response.status_code
            if debug:
                sys.stdout.write(f"[DEBUG] Recording successful transaction with status code: {status_code}\n")
            meter.increment(status_code)
        else:
            if debug:
                sys.stdout.write(f"[DEBUG] Recording successful transaction with default status code (200)\n")
            meter.increment()
        return response
    except Exception as e:
        # Try to extract status code from the exception if it's available
        status_code = None
        if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
            status_code = e.response.status_code
        elif isinstance(e, Exception) and hasattr(e, '__cause__') and hasattr(e.__cause__, 'response'):
            status_code = e.__cause__.response.status_code
            
        # Increment failure counter with the status code if available
        if debug:
            sys.stdout.write(f"[DEBUG] Recording failed transaction with status code: {status_code}\n")
        meter.increment_failure(status_code)
        raise  # Re-raise the exception for the caller to handle

def process_data_batch_with_metering(meter, table_name=None, context_id=None, tenant_id=None, api_key=None, entity_data_list=None, delete_mode=False, debug=False, table_schema=None):
    """Wrapper for process_data_batch that increments the transaction meter for batch operations."""
    if not entity_data_list:
        return
        
    batch_size = len(entity_data_list)
    
    try:
        response = process_data_batch(table_name, context_id, tenant_id, api_key, entity_data_list, delete_mode, debug, table_schema)
        # Increment success counter with the status code if available
        if hasattr(response, 'status_code'):
            status_code = response.status_code
            if debug:
                sys.stdout.write(f"[DEBUG] Recording successful batch of {batch_size} transactions with status code: {status_code}\n")
            meter.increment(status_code, batch_size)
        else:
            if debug:
                sys.stdout.write(f"[DEBUG] Recording successful batch of {batch_size} transactions with default status code (200)\n")
            meter.increment(count=batch_size)
        return response
    except Exception as e:
        # Try to extract status code from the exception if it's available
        status_code = None
        if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
            status_code = e.response.status_code
        elif isinstance(e, Exception) and hasattr(e, '__cause__') and hasattr(e.__cause__, 'response'):
            status_code = e.__cause__.response.status_code
            
        # Increment failure counter with the status code if available
        if debug:
            sys.stdout.write(f"[DEBUG] Recording failed batch of {batch_size} transactions with status code: {status_code}\n")
        meter.increment_failure(status_code, batch_size)
        raise  # Re-raise the exception for the caller to handle

def process_row(row, header, table_name, context_id, tenant_id, api_key, transaction_meter, delete_mode=False, debug=False, table_schema=None):
    """
    Process a single row of data, can be called from a thread.
    
    Args:
        row (list): List of values for the row
        header (list): List of column names from the header row
        table_name (str): Name of the table to load data into
        context_id (str): Context ID to use in the payload
        tenant_id (str): Tenant ID for the API call
        api_key (str): API key for authentication
        transaction_meter (TransactionMeter): Meter for tracking transactions
        delete_mode (bool): If True, deletes records instead of inserting them
        debug (bool): If True, prints detailed debug information
        table_schema (dict): Optional table schema information
    """
    try:
        if len(row) >= 1:
            # Map each column in the row to its header name
            row_data = {}
            has_data = False
            
            # Create a dictionary of field names and values
            for i, field_value in enumerate(row):
                if i < len(header):  # Make sure we don't go beyond available headers
                    field_name = header[i]
                    row_data[field_name] = field_value
                    # Check if we have at least one non-empty value
                    if field_value:
                        has_data = True
            
            if has_data:
                try:
                    # Use process_data_with_metering which properly handles transaction counts
                    process_data_with_metering(transaction_meter, table_name, context_id, tenant_id, api_key, row_data, delete_mode, debug, table_schema)
                    if debug:
                        sys.stdout.write(f"[DEBUG] Successfully processed row\n")
                except Exception as e:
                    if debug:
                        sys.stdout.write(f"[DEBUG] Failed to process row: {str(e)}\n")
                    # Error already logged by process_data, just continue to next record
                    pass
            else:
                sys.stderr.write(f"Skipping row with all empty values: {row}\n")
                sys.stderr.flush()
        else:
            sys.stderr.write(f"Skipping row with insufficient columns: {row}\n")
            sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"Error processing row: {e}, Row: {row}\n")
        sys.stderr.flush()

def process_csv_with_metering(file_path, table_name, context_id, tenant_id, api_key, transaction_meter, start_line=1, num_threads=4, delete_mode=False, debug=False, table_schema=None, batch_size=None):
    """
    Batch processing version of process_csv that uses transaction metering.
    
    Args:
        file_path (str): Path to the CSV file
        table_name (str): Name of the table to load data into
        context_id (str): Context ID to use in the payload
        tenant_id (str): Tenant ID for the API call
        api_key (str): API key for authentication
        transaction_meter (TransactionMeter): Meter for tracking transactions
        start_line (int): Line number to start processing from (1-based)
        num_threads (int): Number of threads to use for processing
        delete_mode (bool): If True, deletes records instead of inserting them
        debug (bool): If True, prints detailed debug information
        table_schema (dict): Optional table schema information
        batch_size (int): Number of records to process in a single API call (1-500)
    """
    import csv
    
    # If batch_size is not provided, get from configuration
    if batch_size is None:
        config = load_config()
        batch_size = config.get("performance", {}).get("batch_size", 100)
    
    # Ensure batch size is within limits (max 500)
    batch_size = min(500, max(1, batch_size))
    
    sys.stdout.write(f"Using batch size of {batch_size} records per API call\n")
    sys.stdout.flush()
    
    try:
        # Read all rows first
        header = []
        rows_to_process = []
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            csv_reader = csv.reader(f, quotechar='"', delimiter=',')
            
            # Always read the header row first
            for i, row in enumerate(csv_reader, 1):
                if i == 1:
                    # Save the header row
                    header = row
                    sys.stdout.write(f"CSV header columns: {', '.join(header)}\n")
                    sys.stdout.flush()
                    continue
                
                # Skip rows until we reach start_line
                if i < start_line + 1:  # +1 because we already skipped header
                    continue
                    
                rows_to_process.append(row)
        
        if not header:
            sys.stderr.write("Error: CSV file does not have a header row\n")
            sys.stderr.flush()
            return
        
        # Prepare batches of rows to process
        total_rows = len(rows_to_process)
        sys.stdout.write(f"Processing {total_rows} rows in batches of {batch_size}\n")
        sys.stdout.flush()
        
        # If using batch processing with multiple threads
        if batch_size > 1:
            # Convert rows to entity data
            entity_data_list = []
            skipped_rows = 0
            
            for row in rows_to_process:
                # Map each column in the row to its header name
                row_data = {}
                has_data = False
                
                # Create a dictionary of field names and values
                for i, field_value in enumerate(row):
                    if i < len(header):  # Make sure we don't go beyond available headers
                        field_name = header[i]
                        row_data[field_name] = field_value
                        # Check if we have at least one non-empty value
                        if field_value:
                            has_data = True
                
                if has_data:
                    # In delete mode, we need just the primary key
                    if delete_mode:
                        primary_key_field = list(row_data.keys())[0]
                        primary_key_value = row_data[primary_key_field]
                        
                        if primary_key_value:
                            entity_data = {primary_key_field: primary_key_value}
                            entity_data_list.append(entity_data)
                    else:
                        entity_data_list.append(row_data)
                else:
                    skipped_rows += 1
                    if debug:
                        sys.stderr.write(f"Skipping row with all empty values: {row}\n")
                        sys.stderr.flush()
            
            # Process entity data in batches using multiple threads
            batches = [entity_data_list[i:i+batch_size] for i in range(0, len(entity_data_list), batch_size)]
            
            sys.stdout.write(f"Created {len(batches)} batches from {len(entity_data_list)} records (skipped {skipped_rows} empty rows)\n")
            sys.stdout.flush()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Submit all batches to the thread pool
                futures = [
                    executor.submit(process_data_batch_with_metering, transaction_meter, table_name, context_id, tenant_id, api_key, batch, delete_mode, debug, table_schema)
                    for batch in batches
                ]
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()  # This will re-raise any exceptions from the threads
        else:
            # Fall back to original row-by-row processing if batch size is 1
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Submit all rows to the thread pool
                futures = [
                    executor.submit(process_row, row, header, table_name, context_id, tenant_id, api_key, transaction_meter, delete_mode, debug, table_schema)
                    for row in rows_to_process
                ]
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()  # This will re-raise any exceptions from the threads
    
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {file_path}\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"Error processing CSV file: {e}\n")
        sys.stderr.flush()

def process_json_line(line, table_name, context_id, tenant_id, api_key, transaction_meter, delete_mode=False, debug=False, table_schema=None):
    """
    Process a single JSON line, can be called from a thread.
    
    Args:
        line (str): JSON line to process
        table_name (str): Name of the table to load data into
        context_id (str): Context ID to use in the payload
        tenant_id (str): Tenant ID for the API call
        api_key (str): API key for authentication 
        transaction_meter (TransactionMeter): Meter for tracking transactions
        delete_mode (bool): If True, deletes the record instead of inserting it
        debug (bool): If True, prints detailed debug information
        table_schema (dict): Optional table schema information
    """
    try:
        data = json.loads(line)
        
        # Check if we have any data
        if data and any(data.values()):
            try:
                # Use process_data_with_metering which properly handles transaction counts
                process_data_with_metering(transaction_meter, table_name, context_id, tenant_id, api_key, data, delete_mode, debug, table_schema)
                if debug:
                    sys.stdout.write(f"[DEBUG] Successfully processed JSON line\n")
            except Exception as e:
                if debug:
                    sys.stdout.write(f"[DEBUG] Failed to process JSON line: {str(e)}\n")
                # Error already logged by process_data, just continue to next record
                pass
        # Handle case where all fields are empty
        else:
            sys.stderr.write(f"Skipping line due to missing data: {line.strip()}\n")
            sys.stderr.flush()
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error decoding JSON: {e}, Line: {line.strip()}\n")
        sys.stderr.flush()

def process_jsonl_with_metering(file_path, table_name, context_id, tenant_id, api_key, transaction_meter, start_line=1, num_threads=4, delete_mode=False, debug=False, table_schema=None, batch_size=None):
    """
    Batch processing version of process_jsonl that uses transaction metering.
    
    Args:
        file_path (str): Path to the JSONL file
        table_name (str): Name of the table to load data into
        context_id (str): Context ID to use in the payload
        tenant_id (str): Tenant ID for the API call
        api_key (str): API key for authentication
        transaction_meter (TransactionMeter): Meter for tracking transactions
        start_line (int): Line number to start processing from (1-based)
        num_threads (int): Number of threads to use for processing
        delete_mode (bool): If True, deletes records instead of inserting them
        debug (bool): If True, prints detailed debug information
        table_schema (dict): Optional table schema information
        batch_size (int): Number of records to process in a single API call (1-499)
    """
    # If batch_size is not provided, get from configuration
    if batch_size is None:
        config = load_config()
        batch_size = config.get("performance", {}).get("batch_size", 499)
    
    # Ensure batch size is within limits (max 499)
    batch_size = min(499, max(1, batch_size))
    
    sys.stdout.write(f"Using batch size of {batch_size} records per API call\n")
    sys.stdout.flush()
    
    try:
        # Read all lines first
        lines_to_process = []
        first_line_data = None
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for i, line in enumerate(f, 1):
                # Skip lines until we reach the start_line
                if i < start_line:
                    continue
                
                # Parse the first line to get field names
                if not first_line_data and i == start_line:
                    try:
                        data = json.loads(line)
                        first_line_data = data
                        keys = list(data.keys())
                        sys.stdout.write(f"JSONL fields detected: {', '.join(keys)}\n")
                        sys.stdout.flush()
                    except json.JSONDecodeError:
                        pass
                
                lines_to_process.append(line)
        
        if not lines_to_process:
            sys.stderr.write(f"No lines to process in {file_path} starting from line {start_line}\n")
            sys.stderr.flush()
            return
        
        total_lines = len(lines_to_process)
        sys.stdout.write(f"Processing {total_lines} lines in batches of {batch_size}\n")
        sys.stdout.flush()
        
        # If using batch processing
        if batch_size > 1:
            # Parse JSON lines and prepare entity data
            entity_data_list = []
            skipped_lines = 0
            
            for line in lines_to_process:
                try:
                    data = json.loads(line)
                    
                    # Check if we have any data
                    if data and any(data.values()):
                        # In delete mode, we need just the primary key
                        if delete_mode:
                            if not data or not list(data.keys()):
                                skipped_lines += 1
                                continue
                                
                            primary_key_field = list(data.keys())[0]
                            primary_key_value = data[primary_key_field]
                            
                            if primary_key_value:
                                entity_data = {primary_key_field: primary_key_value}
                                entity_data_list.append(entity_data)
                            else:
                                skipped_lines += 1
                        else:
                            entity_data_list.append(data)
                    else:
                        skipped_lines += 1
                        if debug:
                            sys.stderr.write(f"Skipping line due to missing data: {line.strip()}\n")
                            sys.stderr.flush()
                except json.JSONDecodeError as e:
                    skipped_lines += 1
                    if debug:
                        sys.stderr.write(f"Error decoding JSON: {e}, Line: {line.strip()}\n")
                        sys.stderr.flush()
            
            # Process entity data in batches using multiple threads
            batches = [entity_data_list[i:i+batch_size] for i in range(0, len(entity_data_list), batch_size)]
            
            sys.stdout.write(f"Created {len(batches)} batches from {len(entity_data_list)} records (skipped {skipped_lines} invalid lines)\n")
            sys.stdout.flush()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Submit all batches to the thread pool
                futures = [
                    executor.submit(process_data_batch_with_metering, transaction_meter, table_name, context_id, tenant_id, api_key, batch, delete_mode, debug, table_schema)
                    for batch in batches
                ]
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()  # This will re-raise any exceptions from the threads
        else:
            # Fall back to original line-by-line processing if batch size is 1
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Submit all lines to the thread pool
                futures = [
                    executor.submit(process_json_line, line, table_name, context_id, tenant_id, api_key, transaction_meter, delete_mode, debug, table_schema)
                    for line in lines_to_process
                ]
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()  # This will re-raise any exceptions from the threads
    
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {file_path}\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"Error processing JSONL file: {e}\n")
        sys.stderr.flush()