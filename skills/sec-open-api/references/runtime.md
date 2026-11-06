# Shared Python runtime

All three skills use the full `sec-opendata-th` checkout or plugin bundle.
Locate this file's real path (resolve symlinks): its fourth parent is the
repository root containing `pyproject.toml`, `secopendata/`, and `skills/`.
Use that absolute root as the command working directory, regardless of the
user's current project. Never assume their current directory is this repository.

Prefer `<root>/.venv/bin/python` (Windows: `<root>/.venv/Scripts/python.exe`).
Otherwise use an installed Python 3.11+ with `requests` available. If setup is
needed, run in the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

On Windows use `py -3.11 -m venv .venv` and the Windows interpreter path.
If a managed plugin directory is read-only, use a user-owned clone and create
the virtual environment there. Do not edit the plugin cache.

Examples in the skills abbreviate the selected interpreter as `python`.
Verify it with `python -m secopendata catalog-info` before first use.
The package has no MCP-server requirement.

Key resolution is explicit client value, scope-specific environment variable,
`SEC_API_KEY`, then the local TOML store. Use
`python -m secopendata onboarding --status --scope fund` to inspect redacted
metadata. A missing key directs the user to `/onBording` (Claude) or
`$sec-onboarding` (Codex). Never request a raw key in chat.
