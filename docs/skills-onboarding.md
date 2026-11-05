# Skill set and onboarding contract

This change keeps the existing Python API, CLI, offline catalog, and plugin
installations. It adds three discoverable skills: `sec-onboarding`,
`sec-fund-search`, and `sec-open-api`. The shared Python runtime stays in the
repository; installing a skill folder alone is insufficient.

The requested first-time command spelling is `/onBording`. Claude exposes the
command through `commands/onBording.md`; installed plugins can namespace it as
`/sec-opendata:onBording`. Codex uses `$sec-onboarding` or its skill picker;
it does not register Claude's custom slash commands. The onboarding skill also
recognizes `/onBording` when passed as ordinary prompt text.

The CLI accepts `onboarding` and the `onBording` alias. It collects secrets via
hidden input in a user-controlled terminal, writes the existing local key
store, preserves other scopes, and emits only redacted metadata. Repeated setup
reuses existing credentials unless replacement is requested. Environment
variables retain their existing precedence. Local setup makes no live request
and must not be described as successful SEC authentication.

Acceptance checks cover setup, later resolver reuse, scope preservation,
replacement, environment precedence, file permissions, unsafe or malformed
stores, cancellation/noninteractive use, and absence of keys in output.
The existing tests cover API access with mocked SEC responses and offline
catalog behavior. Live SEC access requires a user-provided subscription and
is separate from these checks.

Packaging follows the [Agent Skills specification](https://agentskills.io/specification)
and [Claude skill/command documentation](https://code.claude.com/docs/en/skills).
Portable skill names are lowercase; the exact mixed-case command is a Claude
command alias, not the canonical skill name.
