---
description: Set up your SEC Open Data API key for the first time
argument-hint: "[scope, e.g. fund or bond]"
---

Follow `skills/sec-onboarding/SKILL.md` in the repository root. Use
`${CLAUDE_PLUGIN_ROOT}` when available; for a standalone symlink installation,
resolve this command file's real path and use its parent's parent. Treat
`$ARGUMENTS` as a scope selection, never as an
API key or executable shell input. If the argument is not a known scope,
show `categories` and `products` and ask the user to choose.

Run only the redacted status check in the agent shell. For missing credentials,
provide the resolved terminal command for the user to run interactively and
enter their key with hidden input. Recheck status after they finish and resume
the original SEC task. Never collect secrets through chat or command arguments.
