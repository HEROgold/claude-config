"""Show the live git target before Claude merges, cherry-picks, rebases, resets or commits.

PreToolUse hook for the Bash and PowerShell tools. A session's git snapshot ages:
the user switches branches while Claude works, so a merge aimed at "the current
branch" can land somewhere else. For each git write in the command, this hook
reads the live branch and what the operation brings in or drops, then:

- asks the user to confirm when a merge, cherry-pick range or rebase brings in
  more than one commit, or a reset drops commits or uses --hard;
- otherwise passes the branch and commit summary to Claude as context.

Fails open: any parse or git error lets the command through unchanged.
"""

import json
import os
import re
import shlex
import subprocess
import sys

GUARDED = {"merge", "cherry-pick", "rebase", "reset", "commit"}
CONTROL_FLAGS = {"--abort", "--continue", "--quit", "--skip", "--edit-todo"}
SEGMENT_SPLIT = re.compile(r"&&|\|\||;|\n|\|")
MAX_LISTED = 12


def git(repo: str, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, timeout=10
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def resolve(path: str, base: str) -> str:
    path = os.path.expandvars(os.path.expanduser(path))
    return os.path.normpath(path if os.path.isabs(path) else os.path.join(base, path))


def commits(repo: str, rev_range: str) -> list[str]:
    out = git(repo, "log", "--oneline", "--no-merges", rev_range)
    return out.splitlines() if out else []


def listing(lines: list[str]) -> str:
    shown = "\n".join(f"    {line}" for line in lines[:MAX_LISTED])
    more = len(lines) - MAX_LISTED
    return shown + (f"\n    ... and {more} more" if more > 0 else "")


def inspect(repo: str, sub: str, args: list[str]) -> tuple[str, bool]:
    """Return (summary, needs_confirmation) for one git write."""
    branch = git(repo, "branch", "--show-current") or f"detached at {git(repo, 'rev-parse', '--short', 'HEAD')}"
    name = os.path.basename(git(repo, "rev-parse", "--show-toplevel")) or repo
    head = f"{name}: `git {sub}` on branch '{branch}'"
    refs = [a for a in args if not a.startswith("-")]

    if sub == "commit":
        return head, False

    if sub in ("merge", "rebase"):
        source = refs[0] if refs else "@{upstream}"
        brought = commits(repo, f"HEAD..{source}")
        verb = "brings in" if sub == "merge" else "rebases onto"
        text = f"{head} {verb} {len(brought)} commit(s) from '{source}':\n{listing(brought)}"
        return text, len(brought) > 1

    if sub == "cherry-pick":
        picked: list[str] = []
        for ref in refs:
            picked += commits(repo, ref) if ".." in ref else [git(repo, "log", "--oneline", "-1", ref)]
        text = f"{head} applies {len(picked)} commit(s):\n{listing(picked)}"
        return text, len(picked) > 1

    if sub == "reset":
        target = refs[0] if refs else "HEAD"
        dropped = commits(repo, f"{target}..HEAD")
        hard = "--hard" in args
        text = f"{head} moves to '{target}', dropping {len(dropped)} commit(s){' and discarding uncommitted changes (--hard)' if hard else ''}:\n{listing(dropped)}"
        return text, hard or len(dropped) > 0

    return head, False


def git_writes(command: str, cwd: str):
    """Yield (repo, subcommand, args) for each guarded git call in a shell command."""
    here = cwd
    for segment in SEGMENT_SPLIT.split(command):
        try:
            tokens = shlex.split(segment.replace("\\", "/"))
        except ValueError:
            continue
        if not tokens:
            continue
        if tokens[0] in ("cd", "Set-Location", "pushd") and len(tokens) > 1:
            here = resolve(tokens[1], here)
            continue
        if os.path.basename(tokens[0]).removesuffix(".exe") != "git":
            continue
        repo, i = here, 1
        while i < len(tokens) and tokens[i].startswith("-"):
            if tokens[i] == "-C" and i + 1 < len(tokens):
                repo = resolve(tokens[i + 1], repo)
                i += 2
            elif tokens[i] == "-c":
                i += 2
            else:
                i += 1
        if i >= len(tokens) or tokens[i] not in GUARDED:
            continue
        args = tokens[i + 1 :]
        if CONTROL_FLAGS & set(args):
            continue
        yield repo, tokens[i], args


def main() -> None:
    try:
        payload = json.load(sys.stdin)
        command = payload.get("tool_input", {}).get("command", "")
        if "git" not in command:
            return
        cwd = payload.get("cwd") or os.getcwd()
        summaries, confirm = [], False
        for repo, sub, args in git_writes(command, cwd):
            text, needs = inspect(repo, sub, args)
            summaries.append(text)
            confirm |= needs
    except Exception:
        return
    if not summaries:
        return
    message = "Live git target (checked just now, not from the session snapshot):\n" + "\n".join(summaries)
    output = {"hookSpecificOutput": {"hookEventName": "PreToolUse"}}
    if confirm:
        output["hookSpecificOutput"]["permissionDecision"] = "ask"
        output["hookSpecificOutput"]["permissionDecisionReason"] = message
    else:
        output["hookSpecificOutput"]["additionalContext"] = message
    print(json.dumps(output))


if __name__ == "__main__":
    main()
