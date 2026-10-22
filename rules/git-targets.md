# Confirm the target right before a git write

A session's git snapshot ages. The user switches branches, commits, or stashes while you work, so the branch named at session start, or a few turns ago, can be the wrong one by the time you act. A merge, cherry-pick, reset or commit on the wrong branch is local damage that someone has to notice and undo.

## Before a merge, cherry-pick, rebase, reset or commit

- Read the live branch with `git branch --show-current` in the same command that writes, and stop if it isn't the branch the user named. The user's name for the branch is the target. What was checked out earlier is not.
- When the target isn't checked out, write through a worktree of that exact branch (`git worktree add <path> <branch>`), so you leave the user's checkout alone.
- Preview what the operation brings with `git log --oneline <target>..<source>` and `git diff --stat <target>...<source>`. "Merge the fix" means the fix. If the source also carries unrelated commits, for example a branch cut from a newer `main`, cherry-pick only the fix commit.

## After a scripted change across many repos or folders

- Check that every commit holds the change it was made for, such as the bumped version line in its diff. Drop commits that only carry side effects, like a lockfile format bump or touched test fixtures.
- Check that every write landed where the script meant. A path guessed from layout, like "the parent folder is the project", can point into a cache or a vendored clone.

## When it goes wrong

Undo your own commit right away with `git reset --keep HEAD~1`. It keeps the user's uncommitted changes. Then tell the user what happened and what you restored.
