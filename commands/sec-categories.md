---
description: List SEC Open Data portal categories and subscription-key scopes
argument-hint: ""
allowed-tools: Bash(cd:*), Bash(python3 -m secopendata:*)
---

List supported SEC Open Data portal key scopes.

Run:

```bash
cd "${CLAUDE_PLUGIN_ROOT}" && python3 -m secopendata categories
```

Use the `key_scope` values when calling generic `/sec-request` endpoints or
when telling the user which `SEC_<SCOPE>_KEY` environment variable to set.
