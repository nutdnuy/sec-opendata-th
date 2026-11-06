# sec-opendata-th

A reusable **skill set**, Python client, and Codex/Claude plugin for pulling Thai capital-market
data from the SEC OpenAPI (`api.sec.or.th`) — every SEC Open Data portal
category, including digital assets, funds, Licence Check, One Report, provident
funds, debt, equity, ESG, capital-market operators/professionals, investors,
and future `/v1/...` or `/v2/...` endpoints.

The SEC exposes both legacy *products* such as **FundFactsheet** and
**FundDailyInfo**, and current portal paths such as
`/v1/one-report/fs/{report_year}/financial_statement/{unique_id}` and
`/v2/fund/factsheet/performance`. The generic `request` command reaches any
endpoint once you have the matching subscription key.

## Install

```bash
git clone https://github.com/nutdnuy/sec-opendata-th
cd sec-opendata-th
python3 -m venv .venv       # Python 3.11+
.venv/bin/python -m pip install -e .
```

On Windows, use `py -3.11 -m venv .venv` and
`.venv\Scripts\python.exe` for the interpreter.

## First run: `/onBording`

Start with `/onBording` in Claude. When installed as a plugin, use the
namespaced command `/sec-opendata:onBording`. In Codex, select
`$sec-onboarding` from the skill picker; Codex does not register Claude's custom
slash commands. You can also ask in ordinary text to run the `/onBording`
workflow.

The agent checks configuration, helps select the API scope, and gives you a
terminal command. Enter your key in **your own terminal**, where input is hidden:

```bash
.venv/bin/python -m secopendata onboarding --scope fund
# Exact spelling is also available as a CLI alias:
.venv/bin/python -m secopendata onBording --scope fund

# Read configuration metadata without revealing the key or calling SEC:
.venv/bin/python -m secopendata onboarding --status --scope fund
```

The default scope is `fund`. Run `categories` or `products` to select another
scope. Setup stores keys in `~/.config/secopendata/keys.toml` (or the
`SECOPENDATA_KEYS_FILE` override), preserves other scopes, and reuses existing
credentials on subsequent runs. Use `--replace` to change a saved key. Existing
environment variables still take precedence. On POSIX systems the key file is
restricted to its owner (mode `0600`).

Do not paste keys into chat or command arguments. A configured key is **not yet
API-verified**; onboarding performs no live request. Offline searches work
without setup. After terminal setup, return to the agent to continue your query.

## Skills

| Skill | Purpose |
|---|---|
| `sec-onboarding` | First-time setup, redacted status, and key replacement |
| `sec-fund-search` | Offline fund/AMC name and ID lookup, without a key |
| `sec-open-api` | Live SEC data across categories, using saved credentials |

Use the Codex/Claude plugin installation below to install the full set. To use
native skills without a plugin, keep this full checkout and link the three skill
directories into your agent's skill directory. From the repository root on
macOS/Linux, choose **one** target:

```bash
# Codex native skills:
skill_target="$HOME/.agents/skills"
# Or Claude native skills:
# skill_target="$HOME/.claude/skills"
mkdir -p "$skill_target"
for skill in sec-onboarding sec-fund-search sec-open-api; do
  ln -s "$PWD/skills/$skill" "$skill_target/$skill"
done
```

If a target already exists, inspect it before replacing it. For the exact bare
`/onBording` command in native Claude, also link the command:

```bash
mkdir -p "$HOME/.claude/commands"
ln -s "$PWD/commands/onBording.md" "$HOME/.claude/commands/onBording.md"
```

Restart/reload the agent after installation. Choose native skills or the plugin
to avoid duplicate entries. Copying only `SKILL.md` or a single skill directory
does not include the shared Python package, catalog, or sibling references.

## Subscription keys

Get keys from the SEC API Developer Portal:
[secopendata.sec.or.th/sec-open-apis](https://secopendata.sec.or.th/sec-open-apis)
is the current home. The SEC announced discontinuation of the old portal on
30 June 2026; see the [official migration notice](https://api-portal.sec.or.th/changes).
Keys are resolved in this order:

1. value passed in code
2. `SEC_<PRODUCT_OR_CATEGORY>_KEY` env var, e.g. `SEC_FUND_KEY`,
   `SEC_BOND_KEY`, `SEC_PVD_KEY`, `SEC_ONE_REPORT_KEY`,
   `SEC_DIGITAL_ASSET_KEY`
3. `SEC_API_KEY` (shared fallback)
4. `~/.config/secopendata/keys.toml`

```bash
export SEC_FUNDFACTSHEET_KEY="your-factsheet-key"
export SEC_FUNDDAILYINFO_KEY="your-nav-key"
export SEC_FUND_KEY="your-v2-fund-key"
```

Or `~/.config/secopendata/keys.toml`:

```toml
[keys]
FundFactsheet = "your-factsheet-key"
FundDailyInfo = "your-nav-key"
```

Keys are never committed (`keys.toml` and `.env` are git-ignored).

## CLI

```bash
secopendata products                                   # registered products
secopendata categories                                 # current portal key scopes
secopendata catalog-info                               # bundled snapshot metadata
secopendata amc-search "กสิกร"                         # offline AMC lookup; no key
secopendata fund-search "K-CHANGE" --status Registered # offline fund lookup; no key
secopendata amcs                                       # all AMCs (id + name)
secopendata funds --amc KASIKORN                       # funds of an AMC
secopendata nav --proj-id <id> --date 2026-06-16       # daily NAV
secopendata nav --amc KASIKORN --abbr <ABBR> --date 2026-06-16
secopendata fund-info --proj-id <id> --top5 <period>   # policy + classes + top5
secopendata get --product <Name> --path <path> --param key=value [--paginate]  # legacy
secopendata request --method GET --path /v1/one-report/fs/2021/financial_statement/C0000000013
secopendata request --method GET --path /v2/fund/factsheet/performance --cursor-paginate
secopendata request --method GET --path /v2/fund/factsheet/benchmarks --cursor-paginate
secopendata request --method POST --path /v1/digital-asset/profile/intermediary --json '{"IntermediaryName":""}'
```

Successful subcommands print JSON; onboarding prompts go to stderr. Exit codes:
`2` invalid input or setup cancelled/failed, `3` missing key for a data request,
`4` not subscribed, `5` other API error. A successful `onboarding --status`
returns `0` even when `configured` is `false`.

`amc-search` and `fund-search` use the bundled compact SEC profile snapshot and
do not make a network request. Run `catalog-info` to check its as-of date before
relying on current registration status.

## Library

```python
from secopendata import SECClient, FundFactsheet, FundDailyInfo

client = SECClient()
ff = FundFactsheet(client)
amc_id = ff.resolve_amc_id("KASIKORN")
funds = ff.funds_by_amc(amc_id)

nav = FundDailyInfo(client).daily_nav(funds[0]["proj_id"], "2026-06-16")

# Any other product:
data = client.get("SomeOtherProduct", "some/path", params={"q": "x"})
one_report = client.request(
    "GET",
    "/v1/one-report/fs/2021/financial_statement/C0000000013",
)
digital_asset = client.request(
    "POST",
    "/v1/digital-asset/profile/intermediary",
    json_body={"IntermediaryName": ""},
)

for row in client.request_cursor_paginated("/v2/fund/factsheet/performance"):
    ...
```

The client handles the subscription-key header, a sliding-window rate limiter
(default 5000 calls / 300 s with >=16 ms between requests, matching the current
SEC portal), retries throttle/`5xx` responses with `Retry-After` (the SEC
gateway throttles with HTTP **421**), and treats 204 / empty 200 as "no data".

## Equity active/passive study

The `scripts/` folder includes resumable research utilities for SEC Fund v2
data. They read `SEC_FUND_KEY` from the environment and write local artifacts
under `outputs/`, which is intentionally git-ignored.

```bash
export SEC_FUND_KEY="your-v2-fund-key"

# 1) Export the full fund profile universe once.
python scripts/sec_fund_research_export.py profiles \
  --out outputs/sec-active-passive/raw

# 2a) Build the latest factsheet active-vs-passive study for domestic Thai equity funds.
python scripts/sec_active_passive_study.py all \
  --raw-dir outputs/sec-active-passive/raw \
  --out outputs/sec-active-passive/study

# 2b) Or include every equity fund, including foreign/feeder/global equity funds.
python scripts/sec_active_passive_study.py all \
  --raw-dir outputs/sec-active-passive/raw \
  --out outputs/sec-active-passive/study-all-equity \
  --include-foreign-equity
```

By default the study filters `policy_desc = "ตราสารทุน"` and
`invest_country_flag = 3`. Add `--include-foreign-equity` to include every fund
where `policy_desc = "ตราสารทุน"` across all `invest_country_flag` values. It
classifies active/passive from `management_style`, and compares SEC factsheet
`ผลตอบแทนกองทุนรวม` against `ผลตอบแทนตัวชี้วัด` for 1Y/3Y/5Y/10Y. Outputs
include `latest_return_pairs.csv`, `summary_by_horizon_style.csv`, and a
QuantSeras-style HTML report under the selected `--out` directory.

### Gateway host

Defaults to `https://api.sec.or.th`. If the SEC moves the gateway during the
2026 portal migration, override it without touching code:

```bash
export SEC_API_BASE_URL="https://new-host.sec.or.th"
```

## Use as a Codex plugin

This repo is also a Codex plugin (`.codex-plugin/plugin.json`) with a
three skills listed above. The API skill includes endpoint references for bond, fund,
PVD, digital asset, license, and One Report APIs.

```bash
codex plugin marketplace add nutdnuy/sec-opendata-th
```

Then enable/install `sec-opendata` from the Codex plugin UI. The repo includes
`.agents/plugins/marketplace.json` so Codex can read it as a marketplace, and
`.codex-plugin/plugin.json` so the plugin root is valid.

## Use as a Claude Code plugin

The repo is a Claude marketplace and plugin. Add this GitHub repository as a
marketplace in Claude Code:

```text
/plugin marketplace add https://github.com/nutdnuy/sec-opendata-th
/plugin install sec-opendata
```

The Claude UI "Add marketplace" field should use the same GitHub URL:
`https://github.com/nutdnuy/sec-opendata-th`. The marketplace manifest lives at
`.claude-plugin/marketplace.json`, and the plugin manifest lives at
`.claude-plugin/plugin.json`.

Then in Claude Code:

- `/sec-opendata:onBording` — first-time API-key setup
- `/sec-categories`
- `/sec-fund-search K-CHANGE`
- `/sec-request GET /v1/one-report/fs/2021/financial_statement/C0000000013`
- `/sec-funds KASIKORN`
- `/sec-nav <proj_id> 2026-06-16`
- `/sec-fund-info <proj_id> <top5_period>`

Or just ask in natural language. Name lookups use `sec-fund-search` offline;
live requests use `sec-open-api` and route missing credentials to onboarding.

## Develop

```bash
pip install -e ".[dev]"
pytest          # fully mocked — no live subscription key needed
```

## License

MIT
