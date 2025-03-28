import json
import os
import sys

def load_config(config_path=None):
    """
    Load configuration from a JSON file.
    
    Args:
        config_path (str): Path to the configuration file. If None, will use default path.
        
    Returns:
        dict: Configuration dictionary
    """
    # Default config file path is config.json in the same directory as the script
    if config_path is None:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(script_dir, 'config.json')
    
    # Check if the config file exists
    if not os.path.exists(config_path):
        sys.stderr.write(f"Error: Configuration file not found at {config_path}\n")
        sys.stderr.flush()
        return {}
    
    # Load the config file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error parsing configuration file: {e}\n")
        sys.stderr.flush()
        return {}
    except Exception as e:
        sys.stderr.write(f"Error loading configuration file: {e}\n")
        sys.stderr.flush()
        return {}