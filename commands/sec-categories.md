---
description: List SEC Open Data portal categories and subscription-key scopes
argument-hint: ""
---

First read `skills/sec-open-api/references/runtime.md` in `${CLAUDE_PLUGIN_ROOT}`.
Run in that root with its `.venv/bin/python` when available; substitute the
verified Python 3.11+ interpreter if using another environment.

List supported SEC Open Data portal key scopes.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && .venv/bin/python -m secopendata categories
```

Use the `key_scope` values when calling generic `/sec-request` endpoints or
when selecting a scope for `/sec-opendata:onBording`. Listing categories needs
no API key.
