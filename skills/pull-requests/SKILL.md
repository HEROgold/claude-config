---
name: pull-requests
description: When to open a GitHub PR, and whether it starts as a draft or ready for review. Use when work is committed on a branch and you are deciding whether to push and open a PR, when opening one with `gh pr create` or `gh stack submit`, or when a brief says to open a PR.
---

# Opening pull requests

Committed work that sits on a local branch is easy to lose and nobody can review it. Open a PR for it, and use the draft state to say how sure you are.

This applies only in a git repository with a remote on `github.com`. Check with `git remote -v`.

## Whether to open one

- **You're certain a PR is wanted.** The user asked for one, a brief tells you to open one, or the user asked you to push a branch that has no PR yet. Open it, and pick draft or ready yourself with the list below.
- **You're unsure.** The work is committed and the user said nothing about a PR. Push the branch and open a draft PR. Don't leave the work local, and don't stop to ask.
- **No PR.** The repo has no GitHub remote, the work isn't committed, or the user said not to push.

## Draft or ready

Open it ready for review only when all of these hold:

- The change is complete for its issue or task.
- You ran the project's tests, linters and type checks locally, and they pass.
- No question for the user is open, and no manual step (a server change, a secret, a migration) has to happen before it can merge.
- It doesn't depend on another PR that hasn't merged, unless it's part of a `gh stack`.

Otherwise open a draft. If you are unsure about any of these, open a draft too.

## Commands

| Goal | Command |
| --- | --- |
| Open ready for review | `gh pr create --base <trunk> --title "<title>" --body "<body>"` |
| Open as a draft | `gh pr create --draft --base <trunk> --title "<title>" --body "<body>"` |
| Promote a draft once it's done | `gh pr ready <number>` |
| Stack, ready | `gh stack submit --auto --open` |
| Stack, drafts | `gh stack submit --auto` |

For stacked branches, follow the `gh-stack` skill. Its `submit` makes drafts unless you pass `--open`.

## Telling the user

After opening it, give the PR link, say whether it's a draft or ready, and give the reason in one sentence. For a draft, name what has to happen before it can be marked ready.
