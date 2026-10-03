---
paths:
  - "**/*.py"
  - "**/*.pyi"
  - "**/pyproject.toml"
  - "**/uv.lock"
  - "**/requirements*.txt"
---

# Python tooling

Use the existing CLI tools before editing files by hand. A tool that rewrites the file is faster and makes fewer mistakes than a manual edit.

## Running tools

- If the project lists the tool as a dependency, run it with `uv run <tool>`. That uses the version pinned in `uv.lock`.
- Otherwise use the global install (`ruff`) or run it without installing (`uvx pyrefly`).
- Run scripts and tests with `uv run python ...` and `uv run pytest ...`. Don't call `python` or `pip` directly, and don't activate the venv by hand.

## Dependencies (uv)

- Add a package with `uv add <pkg>`, or `uv add --dev <pkg>` for dev tools.
- In a uv workspace, pass `--package <member>` to target one member.
- Remove a package with `uv remove <pkg>`.
- Install the lockfile into the venv with `uv sync`. Regenerate the lockfile with `uv lock`, and upgrade one package with `uv lock --upgrade-package <pkg>`.
- Never hand-edit the dependency tables in `pyproject.toml`, and never edit `uv.lock`. Never use `pip install`.
- To start a new project, run `uv init`. Don't write `pyproject.toml` from scratch.

## Lint and format (ruff)

- After editing Python files, run `ruff check <glob> --fix --unsafe-fixes` on the files you touched, then `ruff format <glob>`.
- Fix by hand only the errors that ruff leaves behind.
- Read the project's ruff config in `pyproject.toml` or `ruff.toml` before adding a `# noqa`. Add one only when the rule really doesn't apply, and name the rule code.

## Types (pyrefly)

- Check types with `pyrefly check`.
- When annotations are missing, run `pyrefly infer <path>` first. It writes inferred annotations into the file. Review its output, then hand-write only what it couldn't infer.
- If the project uses a different checker (pyright, mypy, ty) in its config or CI, use that one to verify. `pyrefly infer` is still fine for filling in annotations.

## Order of work

1. Make the change.
2. `ruff check <files> --fix --unsafe-fixes`, then `ruff format <files>`.
3. Run the type checker on the changed files.
4. Run the relevant tests with `uv run pytest`.
