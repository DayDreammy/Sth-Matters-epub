import json
import os
from pathlib import Path
from types import SimpleNamespace

from workflow import run_deep_search_workflow


def test_end_to_end_deep_search_generates_outputs(temp_project, project_root):
    """Full pipeline: fake Claude -> JSON index -> generators -> artifacts."""
    index_path = temp_project["output_dir"] / "AI_index.json"

    def fake_claude_invoker(prompt: str, base_dir: str):
        index_payload = {
            "metadata": {
                "topic": "AI",
                "search_date": "2024-01-01",
                "total_sources": 1,
                "description": "Integration test index",
            },
            "sources": [
                {
                    "id": 1,
                    "title": "Sample Title",
                    "file_path": "sample.md",
                    "category": "Quick Search Result",
                    "tags": ["AI"],
                    "content_preview": "AI preview",
                    "word_count": 5,
                    "key_concepts": ["AI"],
                    "full_content": "AI content from fixture.",
                }
            ],
            "relationships": {},
        }
        index_path.write_text(json.dumps(index_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return SimpleNamespace(stdout=f"done\n[[[ {index_path} ]]]", stderr="", returncode=0)

    result = run_deep_search_workflow(
        topic="AI",
        base_dir=str(project_root),
        kb_dir=str(temp_project["kb_dir"]),
        output_dir=str(temp_project["output_dir"]),
        claude_invoker=fake_claude_invoker,
    )

    assert result["success"] is True
    assert os.path.exists(result["index_path"])

    md_path = Path(result["files"]["md"])
    html_path = Path(result["files"]["html"])
    epub_path = Path(result["files"]["epub"])

    assert md_path.exists()
    assert html_path.exists()
    assert epub_path.exists()
    assert md_path.read_text(encoding="utf-8").startswith("# AI")
    assert "<html" in html_path.read_text(encoding="utf-8").lower()
    assert epub_path.stat().st_size > 0
