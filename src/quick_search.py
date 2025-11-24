#!/usr/bin/env python3
# -*- coding: utf-8 -#
"""
Quick Search: A local, keyword-based search implementation.
"""

import os
import json
import glob
import re
from datetime import datetime
from typing import List, Dict, Any

def _extract_title(content: str, file_path: str) -> str:
    """Extracts the H1 title from markdown content, or defaults to the filename."""
    match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return os.path.splitext(os.path.basename(file_path))[0]

def _extract_zhihu_links(content: str) -> List[str]:
    """Extracts all zhihu zhuanlan links from the content."""
    return re.findall(r'(https://zhuanlan.zhihu.com/p/\w+)', content)

def perform_quick_search(topic: str, base_dir: str) -> Dict[str, Any]:
    """
    Performs a quick, keyword-based search through the knowledge base.

    Args:
        topic: The keyword to search for.
        base_dir: The project's root directory.

    Returns:
        A dictionary containing the search result status and the path to the index file.
    """
    knowledge_base_dir = os.path.join(base_dir, "knowledge_base", "sth-matters")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(knowledge_base_dir):
        return {"success": False, "error": "Knowledge base directory not found."}

    print(f"Starting quick search for topic: '{topic}' in '{knowledge_base_dir}'")

    # Define exclusion list
    def should_exclude_file(file_path, knowledge_base_dir):
        """Check if file should be excluded from search"""
        # Get relative path from knowledge base
        rel_path = os.path.relpath(file_path, knowledge_base_dir)

        # Exclude files and directories starting with .
        path_parts = rel_path.split(os.sep)
        for part in path_parts:
            if part.startswith('.'):
                return True

        # Exclude specific README.md file in root of knowledge base
        if rel_path == "README.md":
            return True

        return False

    search_results = []
    # Using glob to recursively find all markdown files
    for file_path in glob.glob(os.path.join(knowledge_base_dir, '**', '*.md'), recursive=True):
        # Skip excluded files
        if should_exclude_file(file_path, knowledge_base_dir):
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Case-insensitive search
            if re.search(topic, content, re.IGNORECASE):
                print(f"Found match in: {file_path}")
                title = _extract_title(content, file_path)
                word_count = len(content)
                zhihu_links = _extract_zhihu_links(content)

                source_item = {
                    "id": len(search_results) + 1,
                    "title": title,
                    "file_path": os.path.relpath(file_path, knowledge_base_dir),
                    "zhihu_link": zhihu_links[0] if zhihu_links else "", # Taking the first link
                    "category": "Quick Search Result",
                    "tags": [topic],
                    "content_preview": content[:200] + "...",
                    "word_count": word_count,
                    "key_concepts": [topic],
                    "full_content": content # Add full content for the generator
                }
                search_results.append(source_item)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

    if not search_results:
        return {"success": True, "index_file_path": None, "message": "No results found."}

    # Assemble the final index structure
    final_index = {
        "metadata": {
            "topic": topic,
            "search_date": datetime.now().strftime('%Y-%m-%d'),
            "total_sources": len(search_results),
            "description": f"Quick search results for '{topic}'"
        },
        "sources": search_results,
        "relationships": {} # Keep empty for compatibility
    }

    # Save the index file
    index_filename = f"{topic.replace(' ', '_')}_quick_search_索引.json"
    index_file_path = os.path.join(output_dir, index_filename)
    
    try:
        with open(index_file_path, 'w', encoding='utf-8') as f:
            json.dump(final_index, f, ensure_ascii=False, indent=2)
        print(f"Quick search index file created: {index_file_path}")
        return {"success": True, "index_file_path": index_file_path}
    except Exception as e:
        print(f"Error writing index file: {e}")
        return {"success": False, "error": f"Failed to write index file: {e}"}

if __name__ == '__main__':
    # For testing purposes
    test_topic = "社会化"
    # Assuming the script is in src/, so base_dir is one level up
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    result = perform_quick_search(test_topic, project_root)
    print("\n--- Test Result ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Test with a topic that might not exist
    test_topic_no_result = "NonExistentTopic12345"
    result_no_result = perform_quick_search(test_topic_no_result, project_root)
    print("\n--- No Result Test ---")
    print(json.dumps(result_no_ascii=False, indent=2))