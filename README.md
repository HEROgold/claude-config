# claude-config

My user-level Claude Code rules and skills. `install.ps1` links them into `~/.claude`, so every project on the machine picks them up.

## Layout

| Path | Linked to | Loaded when |
| --- | --- | --- |
| `rules/*.md` | `~/.claude/rules/` | Claude reads a file matching the rule's `paths:` frontmatter. A rule without `paths:` loads every session. |
| `skills/<name>/SKILL.md` | `~/.claude/skills/<name>` | Claude decides the task matches the skill's `description`, or you type `/<name>`. |

Version-specific rules live in `skills/<lang>/versions/<version>.md`, not in `rules/`. Files in `rules/` load for every matching path, but `paths:` can't check the project's language version. The main rule tells Claude which version files to read, so a project on an older version never loads them.

Each language gets a rule and a skill. The rule loads as soon as Claude touches a matching file. The skill covers questions asked before any file is open, and it points back to the rule, so the rule file is the only copy of the content.

## Install

```powershell
git clone https://github.com/HEROgold/claude-config $HOME\claude-config
& $HOME\claude-config\install.ps1
```

The script creates directory junctions, which need no admin rights. It is safe to re-run. If a real folder already sits at a target path, the script moves it to `~/.claude/backups/claude-config-<timestamp>/` and does not delete it.

`skills/gh` and `skills/unslop` are gitignored. They are installed from upstream, not written here.

`rules/unslop.md` has no `paths:`, so it loads every session. Its body is `@~/.claude/skills/unslop/SKILL.md`, which pulls the installed skill's text into context once per session. Updating the upstream skill updates the rule.

## Adding a language

1. Write `rules/<lang>.md` with a `paths:` list of globs.
2. Write `skills/<lang>/SKILL.md` with a `description` that names the language and its tools. Its body should tell Claude to read the rule file.
3. Re-run `install.ps1` to link the new skill.
