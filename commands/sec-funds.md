---
description: List SEC-registered funds for an asset management company (by name or unique_id)
argument-hint: <amc name or unique_id>
---

First read `skills/sec-open-api/references/runtime.md` in `${CLAUDE_PLUGIN_ROOT}`.
Run in that root with its `.venv/bin/python` when available; substitute the
verified Python 3.11+ interpreter if using another environment.

Fetch the fund universe for an AMC from the SEC FundFactsheet API.

AMC requested: `$ARGUMENTS` (a name like `KASIKORN` or a unique_id like `C0000000021`).

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata funds --amc "$ARGUMENTS"
```

Then present the funds as a compact table: `proj_id`, `abbr_name`, fund name.
For a missing key, follow `skills/sec-onboarding/SKILL.md` through
`/sec-opendata:onBording FundFactsheet`. For an unsubscribed key, check that
legacy product subscription before retrying.
