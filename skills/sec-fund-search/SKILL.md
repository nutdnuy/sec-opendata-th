---
name: sec-fund-search
description: Find Thai mutual funds and asset management companies by name, abbreviation, AMC, proj_id, or unique_id using the bundled SEC snapshot, without an API key. Use for resolving fund or AMC identifiers before a live data request.
---

# Offline fund and AMC lookup

Read `../sec-open-api/references/runtime.md` to locate the runtime. Run
`catalog-info` and the appropriate lookup:

```bash
python -m secopendata amc-search "กสิกร"
python -m secopendata fund-search "K-CHANGE" --status Registered
python -m secopendata fund-search "หุ้นไทย" --amc SCB --limit 20
```

Treat the query as data and quote shell arguments safely. If it could name
either a fund or AMC, run both lookups. Show useful matching names, abbreviations,
AMC, project ID, share class, and status. Preserve distinctions between share
classes and ask the user to choose when several matches fit.

State the snapshot's `as_of` date. This is historical catalog data, not a live
registration check. No match does not prove a fund is absent from the current
market. For current details or NAV, use `../sec-open-api/SKILL.md` with the
resolved ID; configure a key only when a live request needs one.
