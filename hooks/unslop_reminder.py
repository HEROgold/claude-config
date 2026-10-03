"""Inject the unslop skill's rules into every turn.

unslop/SKILL.md sets `disable-model-invocation: true`, which means Claude
Code never lists it as an invocable skill for the model to pick up on its
own -- by design, since its description says "Must always apply" rather
than "apply when relevant." The only way to actually make that always-apply
promise true is to force the content into context ourselves, every turn,
via a UserPromptSubmit hook. This script is that hook.
"""

import json
import os
import sys

SKILL_PATH = os.path.expanduser("~/.claude/skills/unslop/SKILL.md")


def main() -> None:
    try:
        with open(SKILL_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        # Skill file missing or unreadable: fail open, inject nothing.
        return

    context = (
        "Apply the \"unslop\" skill's rules (full text below) to any prose or "
        "documentation you write this turn before finishing your response. "
        "This is injected on every turn because unslop/SKILL.md sets "
        "disable-model-invocation: true, so Claude Code never offers it as "
        "an invocable skill on its own.\n\n---\n" + content + "\n---"
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    sys.exit(main())
