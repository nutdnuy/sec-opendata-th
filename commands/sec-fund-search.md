---
description: Search bundled Thai SEC mutual-fund and AMC names offline
argument-hint: <fund name, abbreviation, proj_id, AMC name, or unique_id>
---

First read `skills/sec-open-api/references/runtime.md` in `${CLAUDE_PLUGIN_ROOT}`.
Run in that root with its `.venv/bin/python` when available; substitute the
verified Python 3.11+ interpreter if using another environment.

Search the bundled SEC fund/AMC snapshot without asking for an API key.

Query: `$ARGUMENTS`

Run both lookups because the query may identify either an AMC or a fund:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata amc-search "$ARGUMENTS"
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata fund-search "$ARGUMENTS"
```

Present only useful matches with AMC name, fund abbreviation, Thai fund name,
`proj_id`, share class, and status. Also run `catalog-info` and state the
snapshot date if the user may rely on current registration status.
