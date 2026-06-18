# Gemini / Antigravity Instructions

Follow `AGENTS.md`. Treat this repository as the source of truth for SEC Open
Data Thailand access across all AI tools.

Use the Python CLI for data pulls:

```bash
.venv/bin/python -m secopendata categories
.venv/bin/python -m secopendata request --method GET --path /v1/<category>/<path>
.venv/bin/python -m secopendata request --method GET --path /v2/fund/factsheet/performance --cursor-paginate
.venv/bin/python -m secopendata request --method POST --path /v1/<category>/<path> --json '{"Name":""}'
```

Use `skills/sec-open-api/SKILL.md` as the reusable operating guide. Preserve
generic `/v1` endpoint coverage for digital assets, funds, Licence Check, One
Report, provident funds, debt, equity, ESG, operators/professionals, investors,
and future SEC portal categories. Use `--cursor-paginate` for v2 endpoints that
return `next_cursor` and `items`.
