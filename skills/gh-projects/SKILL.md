---
name: gh-projects
description: Track issue and PR progress on GitHub Projects with `gh project`, `gh issue --project` and `gh pr --project`. Use when adding an issue or PR to a project, moving it between Status columns, reading where an issue stands, or when an issue may already have been auto-added or moved by a project workflow.
---

# GitHub Projects (`gh project`)

Use a GitHub Project to track where an issue or PR stands (Todo, In
progress, Done, or whatever the project's Status field holds). Labels say
what an issue is. The project says how far along it is.

- Every `gh project` command needs the `project` scope (`read:project` for
  read-only commands). Without it they fail with
  `your authentication token is missing required scopes`. Ask the user to run
  `gh auth refresh -s project`; it opens a browser, so you can't run it for them.
- Projects belong to a user or org, not a repo. Pass `--owner <login>` (or
  `--owner @me`) and the project number: `gh project item-list 3 --owner HEROgold`.
  `gh project list --owner <login>` shows the numbers.
- The output flag is `--format json`, not `--json <fields>`. `--jq` and
  `--template` still work.
- `gh project item-list` caps at 30 items (`-L N`). Filter on the server with
  `--query "status:\"In progress\" assignee:@me"` (the Projects filter syntax).

## Items may already be there

Projects run built-in workflows that move items without anyone touching them.
Common ones: auto-add issues from a linked repo that match a filter, set
Status when an item is added, set Status to Done when an issue closes or a
PR merges, and auto-archive old items. Before you add or move an item:

- Check whether the issue is already on a project:
  `gh issue view <n> --json projectItems` returns each project's title and
  the item's `status`. An empty list can also mean the token lacks the
  project scope, so confirm with `gh project item-list` if it matters.
- Don't add an item a workflow will add, and don't set Status to Done by hand
  on close or merge if a workflow does it. Read the project's workflows in the
  web UI (`gh project view <n> --owner <login> --web`, then Workflows) or ask
  the user. The CLI and API can't list them.

## Adding and moving items

- Add by title from the issue side: `gh issue create --project "Roadmap"`,
  `gh issue edit <n> --add-project "Roadmap"` / `--remove-project "Roadmap"`.
  Same flags on `gh pr create` / `gh pr edit`.
- Or from the project side: `gh project item-add <number> --owner <login> --url <issue-url>`.
- Setting a field (such as Status) needs three IDs, none of them the issue number:
  1. Project ID: `gh project view <n> --owner <login> --format json --jq .id`.
  2. Field and option IDs: `gh project field-list <n> --owner <login> --format json`.
     A single-select field lists its `options` with `id` and `name`.
  3. Item ID: from `gh project item-list` (`.items[] | select(.content.number == <n>) | .id`)
     or the output of `item-add`.

  Then: `gh project item-edit --id <item-id> --project-id <project-id> --field-id <field-id> --single-select-option-id <option-id>`.
  Use `--text`, `--number`, `--date`, or `--iteration-id` for other field
  types, and `--clear` to empty a field. One field per call.
