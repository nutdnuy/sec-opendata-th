---
name: sec-opendata
description: Use when the user needs Thai capital-market data from the SEC OpenAPI (api.sec.or.th) — asset management companies, the fund universe, fund policy/holdings/share classes, or daily NAV history. Trigger before any Thai mutual-fund portfolio update or NAV lookup.
---

# SEC OpenData (Thailand)

Pull data from the Securities and Exchange Commission of Thailand OpenAPI at
`api.sec.or.th`. Two products are documented today — **FundFactsheet** and
**FundDailyInfo** — and any other product is reachable through the generic
`get` command.

## Prerequisites

Each product needs its own subscription key (from https://api-portal.sec.or.th).
Resolve keys from, in order: `SEC_<PRODUCT>_KEY` → `SEC_API_KEY` → `~/.config/secopendata/keys.toml`.

```bash
export SEC_FUNDFACTSHEET_KEY="..."
export SEC_FUNDDAILYINFO_KEY="..."
```

If a command exits with an "error: No subscription key" or "not subscribed"
message, tell the user exactly which env var to set — do not retry blindly.

## How to run

Always run the bundled CLI from the plugin root so the package is importable:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata <subcommand> [options]
```

Every subcommand prints JSON to stdout.

| Need | Command |
|------|---------|
| List API products | `python3 -m secopendata products` |
| List all AMCs (id + name) | `python3 -m secopendata amcs` |
| Funds of an AMC | `python3 -m secopendata funds --amc KASIKORN` |
| Daily NAV | `python3 -m secopendata nav --proj-id <id> --date 2026-06-16` |
| Daily NAV by abbr | `python3 -m secopendata nav --amc KASIKORN --abbr <ABBR> --date 2026-06-16` |
| Policy + classes + top5 | `python3 -m secopendata fund-info --proj-id <id> --top5 <period>` |
| Any other product/path | `python3 -m secopendata get --product <Name> --path <path> [--param k=v] [--paginate]` |

## Workflow notes

- NAV is keyed by `proj_id`, not by ticker/abbreviation. To find a `proj_id`,
  list the AMC's funds first (`funds --amc ...`) and read `proj_id` / `abbr_name`.
- A `null` NAV usually means the market was closed or no data exists for that
  date — say so rather than reporting a missing value as an error.
- For "all products": the `get` subcommand hits `api.sec.or.th/<product>/<path>`
  directly, so a newly discovered product works immediately once its key is set.
- This skill is the canonical source for live NAVs — prefer it before
  updating or reviewing any Thai mutual-fund portfolio.
