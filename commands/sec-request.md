---
description: Call any SEC Open Data API path, including GET/POST v1 endpoints and cursor-paginated v2 endpoints
argument-hint: "<GET|POST> <path> [json_body]"
allowed-tools: Bash(cd:*), Bash(python3 -m secopendata:*)
---

Call any SEC Open Data endpoint from `api.sec.or.th`.

Arguments `$ARGUMENTS`: first token is the method (`GET` or `POST`), second
token is the API path such as `/v1/one-report/fs/2021/financial_statement/C0000000013`
or `/v2/fund/factsheet/performance`, and the remaining text is an optional JSON
body for POST endpoints.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata request --method "$1" --path "$2" --json "$3"
```

For v2 endpoints that return `next_cursor` and `items`, add
`--cursor-paginate --page-size 100` and emit the combined items:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata request --method GET --path "$2" --cursor-paginate --page-size 100
```

If the command reports a missing/unsubscribed key, tell the user which
environment variable to set. The key scope is inferred from `/v1/<category>/...`
or `/v2/<category>/...` unless the command needs `--key-scope`.
