---
name: linear
description: Linear workspace conventions (HER-* issues, HEROgold team) and Linear MCP parameter names. Use before creating, updating, commenting on, or searching Linear issues, projects, documents, milestones, or status updates.
---

# Linear

## Workspace

- One team: `HEROgold`. Issue identifiers are `HER-<n>`. `P-HER-<n>` identifiers are projects, not issues.
- Free plan: about 250 active issues. Before creating many issues, count the open ones. Group small related items under one parent issue with a checklist, rather than one issue each.
- The `to grill` label marks items that still need a decision. Tell the user which items carry it, so they can run the grilling skill on them. Remove the label once the item is decided.
- When an item also exists on GitHub, link both ways: add the GitHub URL in `links` on the Linear issue, and the Linear URL in the GitHub issue body.

## MCP parameter names

These guesses fail validation. Use the right-hand names.

| Tool | Wrong | Right |
| --- | --- | --- |
| `save_comment` | `issue` | `issueId` (or `projectId`, `documentId`, ...) |
| `save_issue` | `status` | `state` |
| `get_issue`, `get_document`, `get_project` | `query` | `id` (identifier or slug) |
| `get_status_updates` | missing `type` | `type: "project"` or `"initiative"` |
| `list_issues` `fields` | `relations` | `get_issue` with `includeRelations: true` |

To edit a long description or document, use `patch` with exact `old_string` anchors copied from a fresh `get_*` read. Anchors that do not match exactly fail the whole save.
