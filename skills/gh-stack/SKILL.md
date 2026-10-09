---
name: gh-stack
description: Stacked PRs with `gh stack` (alias `gs`). Use when creating, pushing, rebasing, or syncing a chain of dependent branches or PRs, or when a repo's open PRs target each other instead of the trunk.
---

# Stacked PRs

`gh stack` owns every branch in a stack. Push, rebase, and open PRs through it. A plain `git push`, `git rebase`, or `gh pr create --base <branch>` desyncs the stack on GitHub, and that PR stops showing as part of it.

Run `gh stack view --short` first. If it lists branches, the current branch is in a stack and this skill applies.

## Commands

| Goal | Command |
| --- | --- |
| Start a stack on the trunk | `gh stack init` |
| Turn existing branches into a stack, bottom first | `gh stack init b1 b2 b3` |
| Commit and add a branch on top | `gh stack add -Am "<msg>" <branch>` |
| Push every branch and open or update all PRs | `gh stack submit --auto --open` |
| Push branches only, PRs already exist | `gh stack push` |
| Pull trunk, cascade-rebase, push, sync PR state | `gh stack sync` |
| Rebase after a conflict | `gh stack rebase`, fix files, `git add`, `gh stack rebase --continue` |
| Rebase only branches above the current one | `gh stack rebase --upstack` |
| Inspect state as data | `gh stack view --json` |
| Move around | `gh stack up`, `down`, `top`, `bottom`, `trunk`, `checkout <pr#>` |

`submit` is interactive by default. Pass `--auto` to skip the editor. `--auto` alone creates draft PRs, so always add `--open` to make them ready for review.

## Fixing a lower branch

1. `gh stack checkout <branch>` and commit the fix there, as a new commit.
2. `gh stack sync`. It rebases every branch above onto the fix and force-pushes them with lease.
3. If `sync` reports a conflict, it restores all branches. Run `gh stack rebase`, resolve, then `gh stack sync` again.

## Labels

Version-bump labels (`Major`, `Minor`, `Patch`) go on the top PR of the stack. Every branch below merges up into it, and CI bumps the version from the PR that reaches the trunk.
