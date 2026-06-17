# Claude Code Instructions

Follow `AGENTS.md`. This repo is a Claude-compatible plugin and a shared
implementation used by Codex, Antigravity/Gemini, and GitHub Copilot.

Use `skills/sec-opendata/SKILL.md` for task behavior. The skill must cover all
SEC Open Data categories through the generic `secopendata request` command, not
only mutual funds.

For slash-command workflows, use:

- `/sec-categories`
- `/sec-request`
- `/sec-funds`
- `/sec-nav`
- `/sec-fund-info`

Before handoff, run:

```bash
.venv/bin/python -m pytest -q
```

