# Stack each issue, feature or concept on its own branch with `gh stack`

When a session covers more than one issue, ticket, feature or concept, put each one on its own branch and stack the branches in the order you build them. Each branch then becomes one small PR that reviews and merges on its own, rather than one large mixed diff.

## Where this applies

- Only in a git repository whose remote points at GitHub. Before you start, check with `git remote -v` that a remote URL is on `github.com`.
- If the folder isn't a git repository, or none of its remotes is on GitHub, this rule doesn't apply. Don't run `gh stack` there.

## Building the stack

- Before the first change, start a stack with `gh stack init <branch>`. If the work builds on a branch other than the default branch, pass it as the trunk: `gh stack init --base v2 <branch>`.
- When one unit is done and committed, start the next one on top with `gh stack add <branch>`. Use `gh stack add -Am "<message>" <branch>` to commit the staged work and add the branch in one step.
- Keep a change to the branch it belongs to. To fix an earlier unit, move to its branch (`gh stack down`, `gh stack checkout <branch>`), commit there, then run `gh stack rebase` so the branches above pick it up.
- Order the stack by dependency: a unit that another one needs goes lower in the stack.
- Name each branch after its unit, with the issue number if there is one, for example `207-guild-scoping`.
- Check the stack with `gh stack view`.

## Publishing

- `gh stack push` and `gh stack submit` publish to GitHub. Run them only when the user asks you to push or open PRs.
- Keep the stack in step with the remote with `gh stack sync`.

## When not to stack

- A single issue or feature goes on one branch. Don't split it into a stack.
