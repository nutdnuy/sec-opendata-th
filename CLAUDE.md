# Claude Code Instructions

Follow `AGENTS.md`. This repo is a Claude-compatible plugin and a shared
implementation used by Codex, Antigravity/Gemini, and GitHub Copilot.

Use `skills/sec-open-api/SKILL.md` for task behavior. The skill must cover all
SEC Open Data categories through the generic `secopendata request` command and
the bundled reference files.

For slash-command workflows, use:

- `/onBording` (plugin-qualified: `/sec-opendata:onBording`)
- `/sec-categories`
- `/sec-request`
- `/sec-funds`
- `/sec-nav`
- `/sec-fund-info`

Use `skills/sec-onboarding/SKILL.md` for credential setup and
`skills/sec-fund-search/SKILL.md` for offline name lookup. First read the shared
runtime guide referenced by these skills. Have the user enter secrets in their
own terminal, then check redacted configuration status and resume their task.

Before handoff, run:

```bash
.venv/bin/python -m pytest -q
```
