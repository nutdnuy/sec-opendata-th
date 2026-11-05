---
description: Fetch daily NAV for a SEC-registered fund on a given date
argument-hint: <proj_id> [YYYY-MM-DD]
---

First read `skills/sec-open-api/references/runtime.md` in `${CLAUDE_PLUGIN_ROOT}`.
Run in that root with its `.venv/bin/python` when available; substitute the
verified Python 3.11+ interpreter if using another environment.

Fetch daily NAV from the SEC FundDailyInfo API.

Arguments `$ARGUMENTS`: first token is the fund `proj_id`, optional second token
is the NAV date (`YYYY-MM-DD`, defaults to today).

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata nav --proj-id "$1" --date "$2"
```

Then report the NAV value(s) per share class in a short table. A `null` NAV
means the market was closed or no data exists for that date — state that rather
than treating it as an error. If you don't know the `proj_id`, run `/sec-funds`
for the relevant AMC first.

For a missing key, follow `skills/sec-onboarding/SKILL.md` through
`/sec-opendata:onBording FundDailyInfo`. For an unsubscribed key, check that
legacy product subscription before retrying.
