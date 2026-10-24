---
name: security-automation
description: Check that a project audits its dependencies and scans for secrets automatically (pre-commit, GitHub Actions, Dependabot), per language, and suggest setups where it doesn't. ALWAYS load this at the start of work on any project, once for each language the project uses (Python, JavaScript/TypeScript, Rust, Go, Docker, ...), unless that project's memory already has a security-automation note listing that language as covered or declined. Skip it for a language the note lists.
---

# Check that each project audits its dependencies automatically, per language

A vulnerable dependency or a leaked secret stays in a project until something looks for it. When nothing runs on its own, nobody looks. Each language in a project needs its own check, because a Python audit doesn't see an npm lockfile.

## Check first

- List the project's languages from its manifests: `pyproject.toml`/`uv.lock`, `package.json`, `Cargo.toml`, `go.mod`, `*.csproj`, `Dockerfile`, and so on.
- Read the project's `security-automation` memory note if there is one. Only check the languages it doesn't list.
- For each of those languages, look for automated security checks:
  - `.pre-commit-config.yaml` hooks such as `uv-audit`, `pip-audit`, `osv-scanner`, `gitleaks`, `detect-secrets`, `bandit`.
  - `.github/workflows/*` jobs such as `uv audit`, `pip-audit`, `npm audit`, `cargo audit`, `govulncheck`, `osv-scanner`, CodeQL, Trivy, `dependency-review-action`.
  - `.github/dependabot.yml` or `renovate.json` entries for that ecosystem.
  - Repo settings: `gh api repos/{owner}/{repo}/vulnerability-alerts` (204 means Dependabot alerts are on) and secret scanning.

## When a language has nothing

- Tell the user which languages lack automated checks, and suggest concrete setups for each one. Name the tool, the place it runs, and a snippet:
  - Python (uv): `uv audit --locked --preview-features audit-command` as a pre-push hook and a CI job (on push, PR and a weekly schedule, since new advisories land without code changes); Dependabot `package-ecosystem: uv`. Without uv: `pip-audit`.
  - JavaScript/TypeScript: `npm audit --audit-level=high` in CI; Dependabot for `npm`.
  - Rust: `cargo audit` (or `cargo deny`) in CI; Dependabot for `cargo`.
  - Go: `govulncheck ./...` in CI; Dependabot for `gomod`.
  - Docker: Trivy on the image in CI; Dependabot for `docker`.
  - Any language: `gitleaks` as a pre-commit hook and in CI, `osv-scanner` across all lockfiles, GitHub CodeQL, Dependabot for `github-actions`.
- [HEROgold/pytemplate](https://github.com/HEROgold/pytemplate) (`use_security_scanning`) has a working Python setup to copy from.
- Suggest, don't install. Set it up only when the user agrees, and then follow the project's own workflow (branch, stack, commit rules).

## Write the memory note

- When a language is covered, either because it already was or because the user just set it up, write or update a `project` memory for that project named `security-automation`. List each covered language and what covers it, for example: "Python: uv audit pre-push + CI weekly, gitleaks, Dependabot uv. Covered."
- When the user declines for a language, record it in the same note as "declined", with the date, so the next session doesn't ask again.
- Add the note to the project's `MEMORY.md` index, so later sessions see it without loading this skill.
- A language the project adds later, such as a new `package.json`, isn't in the note, so the skill applies to it again.
