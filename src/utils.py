#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for the Sth-Matters project.
"""

import os
import glob
import shutil
from datetime import datetime

def archive_existing_output(base_dir: str):
    """
    Archives all existing files and folders in the output directory
    into a timestamped subdirectory within output/archive.
    """
    output_dir = os.path.join(base_dir, "output")
    archive_base_dir = os.path.join(output_dir, "archive")
    
    # Ensure the base output and archive directories exist
    os.makedirs(archive_base_dir, exist_ok=True)

    # Find all items in the output directory, excluding the archive folder itself
    items_to_archive = [item for item in glob.glob(os.path.join(output_dir, '*')) 
                        if os.path.basename(item) != 'archive']

    if not items_to_archive:
        print("Output directory is clean. No archiving needed.")
        return

    # Create a new timestamped directory for this archive operation
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_dest_dir = os.path.join(archive_base_dir, timestamp)
    os.makedirs(archive_dest_dir, exist_ok=True)
    
    print(f"Archiving existing output to: {os.path.relpath(archive_dest_dir, base_dir)}")

    # Move each item to the new archive destination
    for item_path in items_to_archive:
        try:
            shutil.move(item_path, archive_dest_dir)
            print(f"  - Archived: {os.path.basename(item_path)}")
        except Exception as e:
            print(f"  - Failed to archive {os.path.basename(item_path)}: {e}")

if __name__ == '__main__':
    # For testing the archive function
    print("--- Testing archive_existing_output ---")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Create some dummy files and folders to archive
    dummy_output_dir = os.path.join(project_root, "output")
    os.makedirs(dummy_output_dir, exist_ok=True)
    with open(os.path.join(dummy_output_dir, "test_file.txt"), "w") as f:
        f.write("test")
    os.makedirs(os.path.join(dummy_output_dir, "test_folder"), exist_ok=True)
    with open(os.path.join(dummy_output_dir, "test_folder", "nested_file.txt"), "w") as f:
        f.write("nested")
    
    print("\n1. Before archiving:")
    for item in os.listdir(dummy_output_dir):
        print(f"  - {item}")
        
    archive_existing_output(project_root)
    
    print("\n2. After archiving:")
    for item in os.listdir(dummy_output_dir):
        print(f"  - {item}")

    print("\n--- Test complete ---")
