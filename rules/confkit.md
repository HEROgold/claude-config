---
paths:
  - "**/*.py"
---

# Configure Python projects with confkit

For runtime configuration (settings files, environment variables, app settings), use [confkit](https://pypi.org/project/confkit/): subclass `confkit.Config`, call `set_file()`, and declare each setting as a `Config` descriptor. Don't hand-roll a `Settings` dataclass that reads `os.environ`.

- Subclass `Config` per namespace, as `herogold.orm` does with `DbConfig`. Don't call `set_file()` on the base class.
- `.ini`, `.toml`, `.yaml`, `.json` and `.env` files are picked by extension.
- If confkit can't do what the project needs, open an issue on confkit, patch around it locally, and mark the patch with a TODO that links the issue, the same way as the herogold-first steps.
- When a project already has hand-rolled config, move it to confkit in its own branch. Don't mix the two systems in one module.
