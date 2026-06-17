---
description: Fetch daily NAV for a SEC-registered fund on a given date
argument-hint: <proj_id> [YYYY-MM-DD]
allowed-tools: Bash(cd:*), Bash(python3 -m secopendata:*)
---

Fetch daily NAV from the SEC FundDailyInfo API.

Arguments `$ARGUMENTS`: first token is the fund `proj_id`, optional second token
is the NAV date (`YYYY-MM-DD`, defaults to today).

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata nav --proj-id "$1" --date "$2"
```

Then report the NAV value(s) per share class in a short table. A `null` NAV
means the market was closed or no data exists for that date — state that rather
than treating it as an error. If you don't know the `proj_id`, run `/sec-funds`
for the relevant AMC first.
