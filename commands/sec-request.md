---
description: Call any SEC Open Data API path, including GET/POST v1 endpoints and cursor-paginated v2 endpoints
argument-hint: "<GET|POST> <path> [json_body]"
---

First read `skills/sec-open-api/references/runtime.md` in `${CLAUDE_PLUGIN_ROOT}`.
Run in that root with its `.venv/bin/python` when available; substitute the
verified Python 3.11+ interpreter if using another environment.

Call any SEC Open Data endpoint from `api.sec.or.th`.

Arguments `$ARGUMENTS`: first token is the method (`GET` or `POST`), second
token is the API path such as `/v1/one-report/fs/2021/financial_statement/C0000000013`
or `/v2/fund/factsheet/performance`, and the remaining text is an optional JSON
body for POST endpoints.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata request --method "$1" --path "$2" --json "$3"
```

For v2 endpoints that return `next_cursor` and `items`, add
`--cursor-paginate --page-size 100` and emit the combined items:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata request --method GET --path "$2" --cursor-paginate --page-size 100
```

If the key is missing, follow `skills/sec-onboarding/SKILL.md` through
`/sec-opendata:onBording` for the inferred scope. For an unsubscribed key, check
subscription validity and scope before replacing it. The key scope is inferred
from `/v1/<category>/...` or `/v2/<category>/...` unless `--key-scope` is set.
