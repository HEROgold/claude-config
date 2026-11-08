---
name: ai-disclosure
description: Label how much AI was involved in a repo, PR or change with the 0rwx levels (ZER0, READ, WRITE, EXECUTE). Use when writing a README, opening a PR, or asked what AI level a project or change is.
---

# AI disclosure with the 0rwx levels

The [0rwx framework](https://0rwx.com/) names four levels of AI involvement, modeled on unix permissions. The level depends on whether the human can still read and check the output, not on which tool was used.

| Level | Badge | Meaning | Short form |
| --- | --- | --- | --- |
| ZER0 | `badges/AI-0.svg` | AI cannot read or write the work. | I think |
| READ | `badges/AI-R.svg` | AI can read the work but does not change it. | I make |
| WRITE | `badges/AI-W.svg` | AI reads and changes the work, and the human reviews it. | I fix |
| EXECUTE | `badges/AI-X.svg` | The human can no longer read the work. | I curate |

## Picking the level

Ask what the session did, then take the highest level that applies:

1. Did Claude edit or create the files? If not, and it only read them, the level is READ.
2. Did Claude edit or create them, and has the user read the result? The level is WRITE.
3. Did Claude produce output the user has not read and could not check, such as generated code merged without review? The level is EXECUTE.

## Where the label goes

- **PR body.** One line near the top: `0rwx: WRITE`.
- **README.** Only when the user asks for a project-level label. Copy the matching SVG from `badges/` into the repo, for example `docs/ai-write.svg`, and add `![0rwx: WRITE](docs/ai-write.svg)` plus one sentence on what the level covers.
- **Per path.** If parts of a repo differ, list them in a small table in the README, such as `docs/` at READ and `src/` at WRITE. Do not invent a split the user has not described.

The badges fill with `currentColor`, so they render black when embedded as an image. On a dark README background, wrap them in a `<picture>` element or recolor the copy.

## Source

Badges are from [NamtaoProductions/0rwx.com](https://github.com/NamtaoProductions/0rwx.com) (`static/AI-*-light.svg`), released into the public domain (CC0).
