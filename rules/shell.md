# Use PowerShell when it is available, Bash only as a fallback

Check which shell tools the session has. If a PowerShell tool exists, run commands there. Use the Bash tool only when PowerShell is missing.

- Write PowerShell syntax in the PowerShell tool and POSIX syntax in the Bash tool. Don't mix them.
- If a Bash command is the only option, such as a POSIX script, say why in one line.
- Prefer the dedicated Read, Edit, Write, Glob and Grep tools over either shell.
