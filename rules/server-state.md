# Check a server before you state what it runs

Files in a repo show what a project ships. They don't show what a server runs. A deploy that only sends an image digest copies no compose file, script or `.env`, so the server keeps whatever was last copied there by hand.

## Before you claim anything about a live server

- Find out how files reach it. Read the deploy workflow: does it copy files (scp, rsync, ssh, a git pull on the server), or only send an image?
- If files reach it only by hand, don't treat the repo's copy as the server's copy. Read the server's file read-only (for example over Tailscale SSH), or say you don't know what it holds.
- Server-specific files for HEROgold's machines live in the private `HEROgold/ops` repo, under `hosts/<host>/`. Even those are only as current as the last copy. Compare before relying on them.

## Changing a server

- Changing a server's files is outward-facing. Explain why the change is needed and get the user's go-ahead first, even with SSH access.
- Change `HEROgold/ops` first, then copy the file to the server.
