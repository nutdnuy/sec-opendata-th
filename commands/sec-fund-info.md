---
description: Fetch a fund's investment policy, share classes, and (optionally) top-5 holdings
argument-hint: <proj_id> [top5_period]
allowed-tools: Bash(cd:*), Bash(python3 -m secopendata:*)
---

Fetch fund detail from the SEC FundFactsheet API.

Arguments `$ARGUMENTS`: first token is the fund `proj_id`, optional second token
is a top-5 holdings period code.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata fund-info --proj-id "$1" --top5 "$2"
```

Summarize the investment policy, list the share classes, and — if a period was
given — the top-5 holdings. If the command reports a missing/unsubscribed key,
tell the user which environment variable to set.
