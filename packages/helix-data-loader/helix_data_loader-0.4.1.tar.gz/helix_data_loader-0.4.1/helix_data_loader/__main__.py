#!/usr/bin/env python
"""
Main module for direct execution of the package.
This allows the module to be run as: python -m helix_data_loader
"""

from .cli import main

if __name__ == "__main__":
    main()