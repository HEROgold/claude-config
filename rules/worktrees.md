# Make worktrees with the tool you are given, else under `.claude/worktrees/`

A worktree gives an agent its own checkout, so it doesn't disturb the user's. Worktrees created by hand end up as sibling folders such as `HeroPy-44` or `repo-worktrees/`. Those look like separate repos, and nothing cleans them up.

## Choosing where the worktree goes

- If the session has a worktree tool, use it. Examples are `EnterWorktree`, a subagent started with `isolation: "worktree"`, or the `wt` CLI (see the `worktrunk` skill). Don't run `git worktree add` yourself when one of these exists.
- If the session has none, run `git worktree add .claude/worktrees/<name> -b <branch>` from the repo root. Use the issue or branch name for `<name>`.
- Never create a worktree beside the repo or outside it, such as `../<repo>-<name>` or `~/worktrees/`.
- `.claude/worktrees/` must be in the repo's `.gitignore`. Add the line before the first worktree if it is missing.

## When you are done

- Remove the worktree once its branch is merged or pushed: `git worktree remove .claude/worktrees/<name>`.
- Don't remove a worktree that has uncommitted changes or commits no remote holds. Tell the user instead.
