import json
import os

from quick_search import perform_quick_search


def test_quick_search_success(temp_project):
    base_dir = str(temp_project["base"])
    result = perform_quick_search("AI", base_dir)

    assert result["success"] is True
    assert result["index_file_path"]
    assert os.path.exists(result["index_file_path"])

    with open(result["index_file_path"], "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["metadata"]["total_sources"] == 1
    assert data["sources"][0]["title"] == "Sample Title"


def test_quick_search_no_results(temp_project):
    base_dir = str(temp_project["base"])
    result = perform_quick_search("NoMatchKeyword", base_dir)

    assert result["success"] is True
    assert result["index_file_path"] is None
