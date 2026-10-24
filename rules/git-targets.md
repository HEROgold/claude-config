# Aim every git write at the branch the user named

A session's git snapshot ages. The user switches branches, commits, or stashes while you work. The `git_target_guard` hook shows the live branch and the commits a merge, cherry-pick, rebase, reset or commit would bring in or drop, and asks the user to confirm when an operation moves more than one commit. Read what it reports before you go on.

## Choosing the operation

- The branch the user named is the target. Compare it with the branch the hook reports, and stop if they differ.
- When the target isn't checked out, write through a worktree of that exact branch (`git worktree add <path> <branch>`), so you leave the user's checkout alone.
- "Merge the fix" means the fix. If the source also carries unrelated commits, for example a branch cut from a newer `main`, cherry-pick only the fix commit.

## After a scripted change across many repos or folders

- Check that every commit holds the change it was made for, such as the bumped version line in its diff. Drop commits that only carry side effects, like a lockfile format bump or touched test fixtures.
- Check that every write landed where the script meant. A path guessed from layout, like "the parent folder is the project", can point into a cache or a vendored clone.

## When it goes wrong

Undo your own commit right away with `git reset --keep HEAD~1`. It keeps the user's uncommitted changes. Then tell the user what happened and what you restored.
