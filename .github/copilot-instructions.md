# GitHub Copilot Instructions

This repo implements `sec-opendata-th`, a Python client/CLI plus agent plugin
for SEC Open Data Thailand.

## Intent

Support every SEC Open Data portal category through generic `/v1` requests:
digital assets, funds, Licence Check, One Report, provident funds, debt, equity,
ESG, capital-market operators/professionals, investors, and future categories.
Also support v2 cursor-paginated endpoints, especially `/v2/fund/...` and
`/v2/bond/...`.

## Development Rules

- Keep generic endpoint coverage centered on `SECClient.request()` and the
  `secopendata request` CLI command.
- Do not narrow behavior back to only `FundFactsheet` or `FundDailyInfo`.
- Never hard-code or commit SEC subscription keys.
- Key scopes map to environment variables such as `SEC_ONE_REPORT_KEY` and
  `SEC_DIGITAL_ASSET_KEY`, `SEC_FUND_KEY`, `SEC_BOND_KEY`, and `SEC_PVD_KEY`.
- Add tests for request path inference, GET/POST behavior, and CLI changes.
- Use `--cursor-paginate` for v2 endpoints returning `next_cursor` and `items`.
- Prefer `.venv/bin/python -m pytest -q` for verification.

## Useful Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m secopendata categories
.venv/bin/python -m secopendata request --method GET --path /v1/one-report/fs/2021/financial_statement/C0000000013
.venv/bin/python -m secopendata request --method GET --path /v2/fund/factsheet/performance --cursor-paginate
```
