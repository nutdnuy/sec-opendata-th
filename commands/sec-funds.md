---
description: List SEC-registered funds for an asset management company (by name or unique_id)
argument-hint: <amc name or unique_id>
allowed-tools: Bash(cd:*), Bash(python3 -m secopendata:*)
---

Fetch the fund universe for an AMC from the SEC FundFactsheet API.

AMC requested: `$ARGUMENTS` (a name like `KASIKORN` or a unique_id like `C0000000021`).

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata funds --amc "$ARGUMENTS"
```

Then present the funds as a compact table: `proj_id`, `abbr_name`, fund name.
If the command reports a missing/unsubscribed key, tell the user which
environment variable to set instead of retrying.
