---
name: skylos
description: Skylos findings on a GitHub PR. Use when asked to check, read, wait for, or fix Skylos comments or the Skylos Analysis check, and after pushing a PR in a repo that has `.github/workflows/skylos.yml`.
---

# Skylos findings

The `Skylos Analysis` CI job posts findings on the PR as `github-actions[bot]`. Read them from the PR. The PR comments match the version and config CI runs.

1. Wait for the run: `gh pr checks <n> --watch --fail-fast`.
2. Read the summary, newest last:
   `gh api repos/{owner}/{repo}/issues/<n>/comments --jq '[.[] | select(.user.login=="github-actions[bot]" and (.body|startswith("## Skylos")))] | last | .body'`
3. Read the inline findings with file and line:
   `gh api repos/{owner}/{repo}/pulls/<n>/comments --paginate --jq '.[] | select(.user.login=="github-actions[bot]") | "\(.path):\(.line) \(.body|split("\n")[0])"'`
   Only comments on the PR's latest commit still apply. Compare `.commit_id` with `gh pr view <n> --json headRefOid`.
4. Fix each finding in code. Suppress one only when it is a false positive, and say why in the PR.
5. Push. If the branch is in a stack, use `gh stack sync` (see the `gh-stack` skill). Then go back to step 1.

Done means the latest summary reports 0 issues on changed lines, or every remaining finding has a written reason on the PR.

To scan locally before pushing, run `uvx skylos . --danger --quality --secrets --json`.
