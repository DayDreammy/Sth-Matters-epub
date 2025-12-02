import os
from types import SimpleNamespace

import pytest

from workflow import (
    extract_index_path,
    run_document_generators,
    run_deep_search_workflow,
)


def test_extract_index_path_success():
    output = "some logs\n[[[ /tmp/output/index.json ]]]"
    assert extract_index_path(output) == "/tmp/output/index.json"


def test_extract_index_path_failure():
    with pytest.raises(ValueError):
        extract_index_path("no marker here")


def test_run_document_generators(temp_project, sample_index_file, project_root):
    files = run_document_generators(
        index_path=str(sample_index_file),
        kb_dir=str(temp_project["kb_dir"]),
        output_dir=str(temp_project["output_dir"]),
        base_dir=str(project_root),
    )

    assert "md" in files and os.path.exists(files["md"])
    assert "html" in files and os.path.exists(files["html"])
    assert "epub" in files and os.path.exists(files["epub"])


def test_run_deep_search_workflow_with_fake_claude(temp_project, project_root):
    index_path = temp_project["output_dir"] / "AI_index.json"

    def fake_claude_invoker(prompt: str, base_dir: str):
        index_path.write_text(
            """
{
  "metadata": {"topic": "AI", "search_date": "2024-01-01", "total_sources": 1},
  "sources": [{
    "id": 1,
    "title": "Sample Title",
    "file_path": "sample.md",
    "category": "Quick Search Result",
    "tags": ["AI"],
    "content_preview": "AI preview",
    "word_count": 5,
    "key_concepts": ["AI"],
    "full_content": "AI content"
  }],
  "relationships": {}
}
""",
            encoding="utf-8",
        )
        return SimpleNamespace(
            stdout=f"finished\n[[[ {index_path} ]]]", stderr="", returncode=0
        )

    result = run_deep_search_workflow(
        topic="AI",
        base_dir=str(project_root),
        kb_dir=str(temp_project["kb_dir"]),
        output_dir=str(temp_project["output_dir"]),
        claude_invoker=fake_claude_invoker,
    )

    assert result["success"] is True
    assert os.path.exists(result["index_path"])
    for path in result["files"].values():
        assert os.path.exists(path)
