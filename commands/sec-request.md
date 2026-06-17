---
description: Call any SEC Open Data API path, including GET and POST /v1 portal endpoints
argument-hint: "<GET|POST> <path> [json_body]"
allowed-tools: Bash(cd:*), Bash(python3 -m secopendata:*)
---

Call any SEC Open Data endpoint from `api.sec.or.th`.

Arguments `$ARGUMENTS`: first token is the method (`GET` or `POST`), second
token is the API path such as `/v1/one-report/fs/2021/financial_statement/C0000000013`,
and the remaining text is an optional JSON body for POST endpoints.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata request --method "$1" --path "$2" --json "$3"
```

If the command reports a missing/unsubscribed key, tell the user which
environment variable to set. The key scope is inferred from `/v1/<category>/...`
unless the command needs `--key-scope`.
