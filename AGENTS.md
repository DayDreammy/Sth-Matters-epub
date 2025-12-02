# Repository Guidelines

This guide keeps contributors aligned on how the system is organized, built, and verified. Aim for small, reviewable changes and favor clarity over cleverness.

## Project Structure & Module Organization
- `src/main.py`: Gradio UI and orchestrator; wires quick/deep search flows and email delivery.
- `src/rpa.py`: Dispatches deep searches to the external `claude` CLI using prompts from `config/ai_prompt.md`.
- `src/document_generator/{md_generator.py,epub_cli.py}`: Convert index JSON into Markdown/HTML/EPUB. Helpers live alongside in `epub_generator.py`.
- `src/quick_search.py`, `src/utils.py`, `src/logger.py`, `src/email_client.py`: Keyword search, shared helpers, structured logging, and SMTP client.
- `config/`: AI prompt and `email_config.json` (keep secrets local). Outputs land in `output/`; logs in `logs/`. The knowledge base is expected at `knowledge_base/sth-matters/`.

## Build, Test, and Development Commands
- Install deps: `pip install -r requirements.txt`.
- Run the app (requires `ANTHROPIC_AUTH_TOKEN`): `python src/main.py` (serves at http://0.0.0.0:7900).
- End-to-end check: `python evaluate.py` (quick search enabled by default; uncomment deep search as needed). Verify Markdown/HTML/EPUB appear in `output/`.
- Generate docs manually: `python src/document_generator/md_generator.py -i <index.json> -o output -k knowledge_base/sth-matters -l all` then `python src/document_generator/epub_cli.py -i <index.json> -o output -k knowledge_base/sth-matters`.

## Coding Style & Naming Conventions
- Python 3, 4-space indentation, snake_case for files/functions/vars. Add type hints for new public functions.
- Use `logger.py` helpers for structured logs; avoid bare prints outside quick diagnostics.
- Keep configuration in `config/` or env vars; never hardcode tokens. Output files follow patterns like `*<topic>*_source_based_文档.md` and `*<topic>*_html_文档.html`.

## Testing Guidelines
- Prefer running `python evaluate.py` after workflow changes; it asserts generation of Markdown/HTML/EPUB for sample topics and checks Markdown structure.
- For new features, add focused scripts or extend `evaluate.py` with deterministic topics. Clean or isolate `output/` artifacts to avoid false positives.
- If changing document generators, open generated files to spot encoding/format regressions.

## Commit & Pull Request Guidelines
- Follow Conventional Commit style seen in history (`feat: ...`, `fix: ...`). Keep messages imperative and scoped.
- In PRs, include: purpose, main changes, test commands run, and sample output paths. Note any required env vars (`ANTHROPIC_AUTH_TOKEN`, SMTP creds) and attach UI screenshots when UI changes.
- Do not commit secrets, large knowledge-base data, or generated artifacts from `output/` and `logs/`.
