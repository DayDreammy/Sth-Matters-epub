import json
import sys
from pathlib import Path

import pytest


# Ensure src/ is importable for modules like quick_search/workflow
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
for path in (str(SRC_DIR), str(ROOT_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)


@pytest.fixture()
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture()
def temp_project(tmp_path: Path) -> dict:
    kb_dir = tmp_path / "knowledge_base" / "sth-matters"
    kb_dir.mkdir(parents=True, exist_ok=True)

    sample_md = kb_dir / "sample.md"
    sample_md.write_text(
        "# Sample Title\n\nAI content with keyword match.\nhttps://zhuanlan.zhihu.com/p/12345\n",
        encoding="utf-8",
    )

    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    return {
        "base": tmp_path,
        "kb_dir": kb_dir,
        "output_dir": output_dir,
        "sample_md": sample_md,
    }


@pytest.fixture()
def sample_index_file(temp_project: dict) -> Path:
    index_path = temp_project["output_dir"] / "AI_index.json"
    index_data = {
        "metadata": {
            "topic": "AI",
            "search_date": "2024-01-01",
            "total_sources": 1,
            "description": "Sample index for testing",
        },
        "sources": [
            {
                "id": 1,
                "title": "Sample Title",
                "file_path": "sample.md",
                "zhihu_link": "https://zhuanlan.zhihu.com/p/12345",
                "category": "Quick Search Result",
                "tags": ["AI"],
                "content_preview": "AI content with keyword match.",
                "word_count": 10,
                "key_concepts": ["AI"],
                "full_content": "Sample body with AI mention.",
            }
        ],
        "relationships": {},
    }
    index_path.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return index_path


class DummyResult:
    def __init__(self, stdout: str, stderr: str = "", returncode: int = 0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
