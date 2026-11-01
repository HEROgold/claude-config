---
paths:
  - "**/.github/workflows/*.yml"
  - "**/.github/workflows/*.yaml"
  - "**/azure-pipelines*.yml"
  - "**/Dockerfile*"
  - "**/compose*.yml"
  - "**/docker-compose*.yml"
  - "**/*.sh"
  - "**/mkdocs.yml"
  - "**/zensical.toml"
  - "**/.pre-commit-config.yaml"
  - "**/copier.yml"
---

# CI, deploy, and docs tooling

My repos share one toolchain. Copy from a repo that already has the piece working. Writing it from memory brings back old versions.

- **Version bumps.** Use `HEROgold/bump-by-label` v5 or later, pinned by SHA. Copy the workflow from its README (`gh repo read-file README.md -R HEROgold/bump-by-label`), "Example usage" for a `pull_request: closed` trigger or "Push events" for a bump job that runs on push after the other checks. Don't copy HeroPy's workflow, which still runs v3. v5 finds the merged PR on a push itself, so don't add a lookup step. Inputs are kebab-case (`github-token`, `base-branch`). Set `base-branch` to the repo's trunk, `checkout: "false"` when the job already checks out, and `create-tag: "false"` when `release.yml` tags. PR labels `Major`, `Minor`, `Patch` pick the bump.
- **Docs.** Use zensical, configured in `zensical.toml`. When a repo still has `mkdocs.yml`, migrating it is a separate PR.
- **Pre-commit.** Run hooks with prek: `uv run prek install`, `uv run prek run --all-files`. The config file stays `.pre-commit-config.yaml`.
- **Dockerfiles and compose files.** Lint with `droast <file>` after each change, and fix its findings before committing.
- **Shell scripts.** A Windows checkout drops the executable bit, and CI then fails with `permission denied`. Stage new scripts with `git add --chmod=+x <file>`, and check that `git ls-files -s <file>` shows mode `100755`.
- **Release gates.** `release.yml` waits on every check workflow (Skylos, tests, lint), not only one. Trunk branch protection requires those same checks.
