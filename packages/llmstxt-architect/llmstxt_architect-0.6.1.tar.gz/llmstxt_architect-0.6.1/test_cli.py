#!/usr/bin/env python3
"""
Test script to debug CLI argument parsing issue.
"""

import argparse
import sys

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Test CLI parser"
    )
    
    # Create mutually exclusive group for URL input sources
    url_group = parser.add_mutually_exclusive_group(required=True)
    
    url_group.add_argument(
        "--urls", 
        nargs="+", 
        help="List of URLs to process"
    )
    
    url_group.add_argument(
        "--existing-llms-file",
        help="Path to an existing llms.txt file to extract URLs from and update"
    )
    
    parser.add_argument(
        "--update-descriptions-only",
        action="store_true",
        help="Update only descriptions in existing llms.txt"
    )
    
    return parser.parse_args()

def main():
    """Test function."""
    try:
        args = parse_args()
        print("Args parsed successfully:")
        print(f"  urls: {args.urls}")
        print(f"  existing_llms_file: {args.existing_llms_file}")
        print(f"  update_descriptions_only: {args.update_descriptions_only}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()