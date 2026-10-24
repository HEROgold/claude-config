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

- **Version bumps.** Copy `.github/workflows/bump-version-by-labels.yml` from `HEROgold/HeroPy`: `gh repo read-file .github/workflows/bump-version-by-labels.yml -R HEROgold/HeroPy`. Set `base_branch` to the repo's trunk. PR labels `Major`, `Minor`, `Patch` pick the bump.
- **Docs.** Use zensical, configured in `zensical.toml`. When a repo still has `mkdocs.yml`, migrating it is a separate PR.
- **Pre-commit.** Run hooks with prek: `uv run prek install`, `uv run prek run --all-files`. The config file stays `.pre-commit-config.yaml`.
- **Dockerfiles and compose files.** Lint with `droast <file>` after each change, and fix its findings before committing.
- **Shell scripts.** A Windows checkout drops the executable bit, and CI then fails with `permission denied`. Stage new scripts with `git add --chmod=+x <file>`, and check that `git ls-files -s <file>` shows mode `100755`.
- **Release gates.** `release.yml` waits on every check workflow (Skylos, tests, lint), not only one. Trunk branch protection requires those same checks.
