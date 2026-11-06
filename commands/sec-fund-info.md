---
description: Fetch a fund's investment policy, share classes, and (optionally) top-5 holdings
argument-hint: <proj_id> [top5_period]
---

First read `skills/sec-open-api/references/runtime.md` in `${CLAUDE_PLUGIN_ROOT}`.
Run in that root with its `.venv/bin/python` when available; substitute the
verified Python 3.11+ interpreter if using another environment.

Fetch fund detail from the SEC FundFactsheet API.

Arguments `$ARGUMENTS`: first token is the fund `proj_id`, optional second token
is a top-5 holdings period code.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata fund-info --proj-id "$1" --top5 "$2"
```

Summarize the investment policy, list the share classes, and — if a period was
given — the top-5 holdings. For a missing key, follow
`skills/sec-onboarding/SKILL.md` through `/sec-opendata:onBording FundFactsheet`.
For an unsubscribed key, check that legacy product subscription before retrying.
