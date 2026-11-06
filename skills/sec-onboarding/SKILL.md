---
name: sec-onboarding
description: Set up or replace a Thai SEC Open Data API subscription key on this computer. Use for first-time SEC setup, missing SEC credentials, or when the user types /onBording. Check configuration without exposing keys.
---

# SEC onboarding

Read `../sec-open-api/references/runtime.md` to locate the bundled Python
runtime. This workflow backs the Claude `onBording` command and the Codex
`$sec-onboarding` skill.

1. Identify the requested key scope. Use `categories` for current scopes or
   `products` for legacy products; default to `fund` for a first-time fund user.
   Different scopes may need different subscriptions.
2. Run `onboarding --status --scope <scope>`. The result contains configuration
   metadata only. If configured, reuse it and continue the original task.
   A configured key has not yet been authenticated with SEC.
3. If missing, give the user the exact terminal command using the resolved
   interpreter: `python -m secopendata onboarding --scope <scope>`. Explain that
   it opens a hidden input prompt and saves to the local key store. The user
   enters the key in their own terminal; a background agent shell cannot collect
   it. Link the [SEC portal](https://secopendata.sec.or.th/sec-open-apis) for
   obtaining a subscription for that scope. Follow the portal's current guide;
   do not invent dashboard labels.
4. Once the user finishes, rerun the status command. Report the scope and
   configuration source, then resume the requested API query. Only a successful
   live query establishes API access. For 401/403, check subscription scope and
   validity; do not repeatedly request or print the key.

For explicit key replacement, use `onboarding --scope <scope> --replace` in
the user's terminal. Existing environment variables take precedence over saved
keys; explain any override notice from the CLI.

Keep secrets out of chat, arguments, logs, source files, and generated reports.
Use only the redacted status command to inspect configuration, never `cat` the
key store or print environment values. Offline fund lookup needs no onboarding.
