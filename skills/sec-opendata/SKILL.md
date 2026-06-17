---
name: sec-opendata
description: "Use when the user needs any Thai capital-market data from SEC Open Data / SEC OpenAPI (api.sec.or.th or secopendata.sec.or.th): digital assets, funds, Licence Check, One Report, provident funds, debt, equity, ESG, capital-market operators/professionals, investors, fund NAVs, or raw /v1 API endpoints."
---

# SEC OpenData (Thailand)

Pull data from the Securities and Exchange Commission of Thailand OpenAPI at
`api.sec.or.th`. The SEC Open Data portal at `secopendata.sec.or.th` exposes
multiple categories, including:

- สินทรัพย์ดิจิทัล (`digital-asset`)
- กองทุน (`fund`, plus legacy `FundFactsheet` and `FundDailyInfo`)
- Licence Check (`license-check`)
- One Report (`one-report`)
- กองทุนสำรองเลี้ยงชีพ (`provident-fund`)
- ตราสารหนี้ (`debt`)
- ตราสารทุน (`equity`)
- ESG (`esg`)
- ผู้ประกอบธุรกิจและบุคลากรในตลาดทุน (`capital-market-professional`)
- ผู้ลงทุน (`investor`)

Use the generic `request` command for all portal endpoints. Use fund helper
commands only when they exactly fit the task.

## Prerequisites

Each product/category may need its own subscription key from
https://secopendata.sec.or.th/sec-open-apis. Resolve keys from, in order:
`SEC_<PRODUCT_OR_CATEGORY>_KEY` → `SEC_API_KEY` →
`~/.config/secopendata/keys.toml`.

```bash
export SEC_FUNDFACTSHEET_KEY="..."
export SEC_FUNDDAILYINFO_KEY="..."
export SEC_ONE_REPORT_KEY="..."
export SEC_DIGITAL_ASSET_KEY="..."
```

If a command exits with an "error: No subscription key" or "not subscribed"
message, tell the user exactly which env var to set — do not retry blindly.

## How to run

Always run the bundled CLI from the plugin root so the package is importable:

```bash
cd "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-.}}" && python3 -m secopendata <subcommand> [options]
```

Every subcommand prints JSON to stdout.

| Need | Command |
|------|---------|
| List legacy products | `python3 -m secopendata products` |
| List portal categories/key scopes | `python3 -m secopendata categories` |
| Any GET endpoint | `python3 -m secopendata request --method GET --path /v1/<category>/<path>` |
| Any POST endpoint | `python3 -m secopendata request --method POST --path /v1/<category>/<path> --json '{"next_cursor":""}'` |
| One Report financial statement | `python3 -m secopendata request --method GET --path /v1/one-report/fs/<report_year>/financial_statement/<unique_id>` |
| List all AMCs (id + name) | `python3 -m secopendata amcs` |
| Funds of an AMC | `python3 -m secopendata funds --amc KASIKORN` |
| Daily NAV | `python3 -m secopendata nav --proj-id <id> --date 2026-06-16` |
| Daily NAV by abbr | `python3 -m secopendata nav --amc KASIKORN --abbr <ABBR> --date 2026-06-16` |
| Policy + classes + top5 | `python3 -m secopendata fund-info --proj-id <id> --top5 <period>` |
| Legacy product/path | `python3 -m secopendata get --product <Name> --path <path> [--param k=v] [--paginate]` |

## Workflow notes

- NAV is keyed by `proj_id`, not by ticker/abbreviation. To find a `proj_id`,
  list the AMC's funds first (`funds --amc ...`) and read `proj_id` / `abbr_name`.
- A `null` NAV usually means the market was closed or no data exists for that
  date — say so rather than reporting a missing value as an error.
- For "all categories": copy the endpoint path from the SEC portal and run
  `request`. The key scope is inferred from `/v1/<category>/...`; override with
  `--key-scope <scope>` if the portal uses a different subscription product.
- POST endpoints often use a cursor body such as `{"next_cursor":""}`. Preserve
  the portal's JSON body shape; do not convert it into query params unless the
  documentation shows query params.
- This skill is the canonical source for live NAVs — prefer it before
  updating or reviewing any Thai mutual-fund portfolio.
