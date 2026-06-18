---
name: sec-open-api
description: Query Thailand's SEC (Securities and Exchange Commission) Open API for bond, mutual fund, provident fund (PVD), digital asset business operator, license/enforcement, and One Report (Form 56-1) data. Use whenever the user asks about Thai listed companies, bonds, mutual funds, PVD, SEC-licensed persons/entities, investor alerts, auditors, or one-report/56-1 disclosures, or mentions "ก.ล.ต.", "SEC Open API", "Ocp-Apim-Subscription-Key".
---

# SEC Open API (Thailand)

Wrapper skill for calling the Thai SEC's Open Data API. In this repository,
prefer the bundled Python CLI/client over raw `curl` because it handles key
resolution, retry/backoff, rate limiting, JSON output, and v2 cursor pagination.

## 1. Get the API key — every time, from the conversation only

This skill is shared/portable, so **never read or write the key to disk** and never hardcode it in commands you save to files.

- If the user has already given a key earlier in *this* conversation, reuse it.
- Otherwise, ask the user directly: "ขอ Ocp-Apim-Subscription-Key ของคุณเพื่อใช้เรียก SEC Open API" before making any request.
- If the user instead says it's in an environment variable (e.g. `SEC_API_KEY`), use that env var in the command rather than asking again.
- Never echo the raw key back in your own commentary; only pass it inside the request header.

## 2. Base URL & headers

```
https://api.sec.or.th
```

Every request needs this header; the bundled CLI adds it automatically from the
resolved env var/key store:

```
-H "Ocp-Apim-Subscription-Key: <key>"
-H "Content-Type: application/json"
```

Preferred CLI examples:

```bash
SEC_PVD_KEY="$SEC_API_KEY" python -m secopendata request \
  --method GET \
  --path /v1/pvd/factsheet/amc
```

POST endpoints (search-style) send a JSON body, e.g.:

```bash
SEC_LICENSE_CHECK_KEY="$SEC_API_KEY" python -m secopendata request \
  --method POST \
  --path /v1/license-check/licensee/person \
  --json '{"Name":"สมชาย"}'
```

## 3. Rate limit & retry

- Max 5,000 requests / 300 seconds.
- If a response comes back faster than 16ms, add a small delay (`sleep 0.02`) before the next request in a loop.
- On HTTP 421, read the `Retry-After` value and wait that long before retrying — don't just retry immediately.

## 4. Pagination (cursor-based)

Most v2 endpoints return:

```json
{ "message": "success", "page_size": 100, "next_cursor": "xxxx", "items": [ ... ] }
```

- `page_size` max 100, settable via query param.
- For v2 endpoints, prefer `--cursor-paginate` so the CLI keeps calling the
  same endpoint with `next_cursor` until it becomes `""` and emits the combined
  `items` array.
- Older v1 endpoints (license-check, pvd, digital-asset, one-report) do not paginate — they return all `items` in one shot.

```bash
SEC_FUND_KEY="$SEC_API_KEY" python -m secopendata request \
  --method GET \
  --path /v2/fund/factsheet/performance \
  --cursor-paginate \
  --page-size 100
```

## 5. Endpoint index

Full field-level request/response schemas are in `references/<file>.md` next to this SKILL.md — read the relevant file before building a request you're not already sure about (param names, enum codes, nested object shapes).

### Bond — `references/bond.md` (v2, paginated)
| Method & Path | Purpose |
|---|---|
| GET /v2/bond/issuers | รายชื่อผู้ออกตราสารหนี้ |
| GET /v2/bond/features | ลักษณะทั่วไปของตราสารหนี้ (type, coupon, maturity, offering...) |
| GET /v2/bond/credit-ratings | อันดับความน่าเชื่อถือตามช่วงเวลา |
| GET /v2/bond/outstanding-values | มูลค่าคงค้างตามช่วงเวลา |
| GET /v2/bond/involve-parties | ผู้เกี่ยวข้องกับตราสารหนี้ตามช่วงเวลา |
| GET /v2/bond/investor-holdings | มูลค่าตราสารแยกตามประเภทผู้ลงทุน |

### Fund — `references/fund.md` (v2, paginated)
| Method & Path | Purpose |
|---|---|
| GET /v2/fund/general-info/amcs | รายชื่อบลจ. |
| GET /v2/fund/general-info/profiles | กองทุน + ลักษณะทั่วไป (สถานะ, นโยบาย, class fund) |
| GET /v2/fund/general-info/specifications | ประเภทกองทุนตามลักษณะพิเศษ |
| GET /v2/fund/general-info/mutual-fund-fees | ค่าธรรมเนียมตามโครงการ |
| GET /v2/fund/general-info/involve-parties | ผู้เกี่ยวข้องกับกองทุน (trustee, registrar, ...) |
| GET /v2/fund/factsheet/urls | URL/PDF ของ Fund Factsheet |
| GET /v2/fund/factsheet/ipos | ข้อมูลการเสนอขาย (IPO) |
| GET /v2/fund/factsheet/benchmarks | ดัชนีชี้วัด |
| GET /v2/fund/factsheet/subscription-redemption-minimums | มูลค่า/จำนวนหน่วยขั้นต่ำ ซื้อ-ขาย-คงเหลือ |
| GET /v2/fund/factsheet/subscription-redemption-periods | ระยะเวลาขาย/รับซื้อคืน |
| GET /v2/fund/factsheet/risk-spectrum | ระดับความเสี่ยง |
| GET /v2/fund/factsheet/statistics | สถิติกองทุน (sharpe, beta, turnover...) |
| GET /v2/fund/factsheet/dividend-policy | นโยบายปันผล |
| GET /v2/fund/factsheet/fees | ค่าธรรมเนียมจริงที่เก็บ |
| GET /v2/fund/factsheet/performance | ผลการดำเนินงานย้อนหลัง |
| GET /v2/fund/factsheet/asset-allocation | สัดส่วนประเภททรัพย์สิน |
| GET /v2/fund/factsheet/top5-holdings | หลักทรัพย์ 5 อันดับแรก |
| GET /v2/fund/outstanding/portfolio | พอร์ตการลงทุนรายไตรมาส |
| GET /v2/fund/outstanding/portfolio-asset-type | สัดส่วนพอร์ตตามประเภทสินทรัพย์รายเดือน |
| GET /v2/fund/daily-info/nav | NAV รายวัน |
| GET /v2/fund/daily-info/dividend-history | ประวัติการจ่ายปันผล |

### PVD (Provident Fund) — `references/pvd.md` (v1, not paginated)
| Method & Path | Purpose |
|---|---|
| GET /v1/pvd/factsheet/amc | รายชื่อบลจ. ที่บริหาร PVD |
| GET /v1/pvd/factsheet/{unique_id}/fund | กองทุน PVD ภายใต้บลจ.นั้น |
| POST /v1/pvd/factsheet/fund | ค้นหากองทุน PVD ด้วยชื่อ |
| GET /v1/pvd/factsheet/{proj_id}/policy | นโยบายการลงทุน |
| GET /v1/pvd/factsheet/{proj_id}/return | ผลตอบแทนย้อนหลัง |
| GET /v1/pvd/factsheet/{proj_id}/trailreturn | ผลตอบแทนย้อนหลังแบบปักหมุด |
| GET /v1/pvd/factsheet/{proj_id}/fee | ค่าธรรมเนียม |
| GET /v1/pvd/factsheet/{proj_id}/PVDFullPort/{period} | สัดส่วนการลงทุนรายเดือน |
| GET /v1/pvd/factsheet/{proj_id}/statistics | สถิติกองทุน |
| GET /v1/pvd/factsheet/{proj_id}/top5/assettype | Top5 ประเภททรัพย์สิน |
| GET /v1/pvd/factsheet/{proj_id}/top5/securities | Top5 หลักทรัพย์ |
| GET /v1/pvd/factsheet/{proj_id}/top5/foreign | Top5 ประเทศ (ลงทุนตรง) |
| GET /v1/pvd/factsheet/{proj_id}/top5/industry | Top5 อุตสาหกรรม (ตราสารทุนตรง) |
| GET /v1/pvd/factsheet/{proj_id}/top5/issuer | Top5 ผู้ออกตราสาร (ตราสารหนี้ตรง) |
| GET /v1/pvd/factsheet/{proj_id}/nav/{nav_date} | NAV รายเดือน |

### Digital Asset — `references/digital-asset.md` (v1, not paginated)
| Method & Path | Purpose |
|---|---|
| POST /v1/digital-asset/profile/intermediary | ค้นหาผู้ประกอบธุรกิจสินทรัพย์ดิจิทัล |

### License Check — `references/license.md` (v1, not paginated)
| Method & Path | Purpose |
|---|---|
| POST /v1/license-check/licensee/person | ค้นหาบุคคลที่ได้รับความเห็นชอบ |
| GET /v1/license-check/licensee/company | นิติบุคคลที่ได้รับใบอนุญาต/จดทะเบียน |
| POST /v1/license-check/licensee/company | ค้นหานิติบุคคลด้วยชื่อ |
| GET /v1/license-check/licensee/person/{unique_id}/license | ประเภทความเห็นชอบของบุคคล |
| GET /v1/license-check/licensee/company/{unique_id}/personnel | บุคคลที่ปฏิบัติหน้าที่ในนิติบุคคลนั้น |
| GET /v1/license-check/licensee/person/{unique_id}/work_info | นิติบุคคลที่บุคคลนั้นปฏิบัติหน้าที่อยู่ |
| GET /v1/license-check/licensee/company/{unique_id}/license | ประเภทใบอนุญาตของนิติบุคคล |
| GET /v1/license-check/licensee/company/{unique_id}/business_act | สถานะการประกอบธุรกิจปัจจุบัน |
| GET /v1/license-check/licensee/{unique_id}/enforcement | รายการคดี/ความผิด |
| GET /v1/license-check/licensee/{unique_id}/enforcement/{case_id} | รายละเอียดการดำเนินการต่อคดี |
| GET /v1/license-check/licensee/investoralert/alertdetail | รายชื่อ Investor Alert |
| GET /v1/license-check/licensee/investoralert/{case_id}/alertaction | ลักษณะการกระทำของ alert case |
| GET /v1/license-check/licensee/auditors | รายชื่อผู้สอบบัญชี |
| GET /v1/license-check/licensee/auditingFirm | รายชื่อบริษัทสอบบัญชี |
| GET /v1/license-check/licensee/auditors/search/name/{person_name} | ค้นหาผู้สอบบัญชีด้วยชื่อ |

### One Report (แบบ 56-1) — `references/one_report.md` (v1, not paginated)
23 endpoints under `/v1/one-report/{sbo,sustainability,scp,cgp,fs,cgs}/{report_year}/.../{unique_id}` covering company info, R&D, revenue structure, risk management, sustainability (environment/social/CSR), governance policy, financial statements, board/executives/committees, and auditor company. See `references/one_report.md` for the full list and field schemas.

## 6. Common gotchas

- `unique_id` / `proj_id` / `bond_id` from one endpoint is the join key into related endpoints in the same category (and sometimes across categories, e.g. PVD amc `unique_id` ↔ Fund amc `unique_id` ↔ License company `unique_id` — verify the ID actually matches before assuming a cross-category join).
- Date fields are often `YYYY-MM-DD` but some legacy fields may use Buddhist Era (พ.ศ.) years — check the field description in the reference doc.
- Empty string `""` often means "no end date / still active", not missing data — don't treat it as null.
