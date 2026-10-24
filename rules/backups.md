# Back up a file before changing it, unless git or another copy already holds it

A file that isn't committed or saved anywhere else has no history. Once it's overwritten, the old contents are gone. Tokens, passwords and other local config are usually in exactly these files.

## Make a `.bak` first

- Before the first change to such a file in a session, copy it next to itself: `cp bot.ini bot.ini.bak`.
- This covers gitignored files (`.ini`, `.env`, local config), untracked files, and tracked files with uncommitted changes.
- It covers every way the file can change: your own edits, overwrites, scripts, and a program or container that writes to the file, such as a bind mount.
- If a `.bak` already exists, look at it before replacing it. It may be the only copy of what used to be there.
- A committed file with no local changes doesn't need one, because git has it.
