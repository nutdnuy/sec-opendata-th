# Agent Instructions — sec-opendata-th

This repository is the shared source of truth for the SEC Open Data Thailand
client and plugin. It must work for Codex, Claude Code, Antigravity/Gemini, and
GitHub Copilot.

## Goal

Provide a Python CLI/client and reusable agent skill for pulling data from
`api.sec.or.th` across all SEC Open Data portal categories:

- digital assets
- funds
- Licence Check
- One Report
- provident funds
- debt
- equity
- ESG
- capital-market operators/professionals
- investors
- any future `/v1/...` endpoint copied from `secopendata.sec.or.th`

## Core Commands

Use the virtual environment when available:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m secopendata categories
.venv/bin/python -m secopendata request --method GET --path /v1/one-report/fs/2021/financial_statement/C0000000013
```

Generic endpoint access must go through:

```bash
python -m secopendata request --method GET --path /v1/<category>/<path>
python -m secopendata request --method POST --path /v1/<category>/<path> --json '{"next_cursor":""}'
```

Keep legacy fund helpers, but do not build new category-specific helpers unless
they remove repeated real usage. The generic `request` command is the canonical
coverage mechanism for all categories.

## Keys

Never commit subscription keys. Key resolution is:

1. explicit value in code
2. `SEC_<PRODUCT_OR_CATEGORY>_KEY`
3. `SEC_API_KEY`
4. `~/.config/secopendata/keys.toml`

Examples: `SEC_ONE_REPORT_KEY`, `SEC_DIGITAL_ASSET_KEY`,
`SEC_LICENSE_CHECK_KEY`, `SEC_PROVIDENT_FUND_KEY`.

## Plugin Surfaces

- Codex plugin manifest: `.codex-plugin/plugin.json`
- Claude plugin manifest: `.claude-plugin/plugin.json`
- Shared skill: `skills/sec-opendata/SKILL.md`
- Claude slash commands: `commands/*.md`
- GitHub Copilot instructions: `.github/copilot-instructions.md`
- Antigravity/Gemini instructions: `GEMINI.md`

When behavior changes, update all relevant surfaces so every AI tool gives the
same guidance.

## Quality Bar

- Read the existing code before editing.
- Keep changes small and maintainable.
- Add or update tests for client/CLI behavior.
- Run `.venv/bin/python -m pytest -q` before handoff.
- Validate Codex plugin manifests with:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

