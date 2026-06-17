# sec-opendata-th

A Python client **and** Codex/Claude plugin for pulling Thai capital-market
data from the SEC OpenAPI (`api.sec.or.th`) — every SEC Open Data portal
category, including digital assets, funds, Licence Check, One Report, provident
funds, debt, equity, ESG, capital-market operators/professionals, investors,
and future `/v1/...` endpoints.

The SEC exposes both legacy *products* such as **FundFactsheet** and
**FundDailyInfo**, and current portal paths such as
`/v1/one-report/fs/{report_year}/financial_statement/{unique_id}`. The generic
`request` command reaches any endpoint once you have the matching subscription
key.

## Install

```bash
git clone https://github.com/nutdnuy/sec-opendata-th
cd sec-opendata-th
pip install -e .            # installs the `secopendata` package + CLI
# (or: pip install -r requirements.txt and run via `python -m secopendata`)
```

## Subscription keys

Get keys from the SEC API Developer Portal. The portal is migrating:
[secopendata.sec.or.th/sec-open-apis](https://secopendata.sec.or.th/sec-open-apis)
is the new home; the old [api-portal.sec.or.th](https://api-portal.sec.or.th)
is discontinued on 30 June 2026. Subscription keys carry over.
Keys are resolved in this order:

1. value passed in code
2. `SEC_<PRODUCT_OR_CATEGORY>_KEY` env var, e.g. `SEC_FUNDFACTSHEET_KEY`,
   `SEC_ONE_REPORT_KEY`, `SEC_DIGITAL_ASSET_KEY`
3. `SEC_API_KEY` (shared fallback)
4. `~/.config/secopendata/keys.toml`

```bash
export SEC_FUNDFACTSHEET_KEY="your-factsheet-key"
export SEC_FUNDDAILYINFO_KEY="your-nav-key"
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
secopendata amcs                                       # all AMCs (id + name)
secopendata funds --amc KASIKORN                       # funds of an AMC
secopendata nav --proj-id <id> --date 2026-06-16       # daily NAV
secopendata nav --amc KASIKORN --abbr <ABBR> --date 2026-06-16
secopendata fund-info --proj-id <id> --top5 <period>   # policy + classes + top5
secopendata get --product <Name> --path <path> --param key=value [--paginate]  # legacy
secopendata request --method GET --path /v1/one-report/fs/2021/financial_statement/C0000000013
secopendata request --method POST --path /v1/digital-asset/... --json '{"next_cursor":""}'
```

All subcommands print JSON. Exit codes: `3` missing key, `4` not subscribed,
`5` other API error.

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
    "/v1/digital-asset/business-operators/search",
    json_body={"next_cursor": ""},
)
for row in client.get_paginated("SomeOtherProduct", "list", page_size=200):
    ...
```

The client handles the subscription-key header, a sliding-window rate limiter
(default 5000 calls / 300 s with >=16 ms between requests, matching the current
SEC portal), retries throttle/`5xx` responses with `Retry-After` (the SEC
gateway throttles with HTTP **421**), and treats 204 / empty 200 as "no data".

### Gateway host

Defaults to `https://api.sec.or.th`. If the SEC moves the gateway during the
2026 portal migration, override it without touching code:

```bash
export SEC_API_BASE_URL="https://new-host.sec.or.th"
```

## Use as a Codex plugin

This repo is also a Codex plugin (`.codex-plugin/plugin.json`) with a
`sec-opendata` skill. The skill prefers the generic `request` command for all
portal categories and uses fund helpers only for convenience.

## Use as a Claude Code plugin

The repo also keeps Claude slash-command files for compatibility with older
Claude Code workflows.

```text
/plugin marketplace add /path/to/sec-opendata-th
/plugin install sec-opendata
```

Then in Claude Code:

- `/sec-categories`
- `/sec-request GET /v1/one-report/fs/2021/financial_statement/C0000000013`
- `/sec-funds KASIKORN`
- `/sec-nav <proj_id> 2026-06-16`
- `/sec-fund-info <proj_id> <top5_period>`

Or just ask in natural language — the `sec-opendata` skill triggers on Thai
SEC Open Data requests and runs the CLI for you.

## Develop

```bash
pip install -e ".[dev]"
pytest          # fully mocked — no live subscription key needed
```

## License

MIT
