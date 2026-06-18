#!/usr/bin/env python3
"""Export SEC fund data for Thai equity active/passive research.

The script writes page-by-page JSONL files plus small metadata checkpoints so a
long pull can be resumed without repeating completed pages. API keys are read
from the normal secopendata environment variables, for example SEC_FUND_KEY.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Mapping

from secopendata import SECClient


DEFAULT_OUT = Path("outputs/sec-active-passive/raw")
FUND_ENDPOINTS = {
    "benchmarks": "/v2/fund/factsheet/benchmarks",
    "performance": "/v2/fund/factsheet/performance",
    "asset_allocation": "/v2/fund/factsheet/asset-allocation",
    "statistics": "/v2/fund/factsheet/statistics",
    "fees": "/v2/fund/factsheet/fees",
    "nav": "/v2/fund/daily-info/nav",
    "dividends": "/v2/fund/daily-info/dividend-history",
}
THAI_EQUITY_POLICY = "ตราสารทุน"
EXCLUDE_MANAGEMENT_STYLES = {"IM", "IN", "LM", "LN", "BH"}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def append_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":"), default=str))
            fh.write("\n")
            count += 1
    return count


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def reset_outputs(data_path: Path, meta_path: Path) -> None:
    for path in (data_path, meta_path):
        if path.exists():
            path.unlink()


def fetch_cursor_jsonl(
    client: SECClient,
    *,
    endpoint: str,
    params: Mapping[str, Any],
    data_path: Path,
    page_size: int,
    max_pages: int | None,
    force: bool,
    label: str,
) -> dict[str, Any]:
    meta_path = data_path.with_suffix(data_path.suffix + ".meta.json")
    if force:
        reset_outputs(data_path, meta_path)

    meta = read_json(meta_path)
    if meta.get("complete"):
        print(f"skip complete {label}: {meta.get('rows', 0)} rows", flush=True)
        return meta

    next_cursor = str(meta.get("next_cursor") or "")
    pages_done = int(meta.get("pages", 0))
    rows_done = int(meta.get("rows", 0))

    while True:
        if max_pages is not None and pages_done >= max_pages:
            meta.update(
                {
                    "endpoint": endpoint,
                    "params": dict(params),
                    "page_size": page_size,
                    "next_cursor": next_cursor,
                    "pages": pages_done,
                    "rows": rows_done,
                    "complete": False,
                    "stopped_at_page_limit": True,
                    "updated_at": now_iso(),
                }
            )
            write_json(meta_path, meta)
            return meta

        query = dict(params)
        query["page_size"] = page_size
        query["next_cursor"] = next_cursor
        started = time.monotonic()
        data = client.request("GET", endpoint, key_scope="fund", params=query)
        elapsed = time.monotonic() - started
        if data is None:
            items: list[dict[str, Any]] = []
            new_cursor = ""
        elif isinstance(data, Mapping):
            raw_items = data.get("items") or []
            if not isinstance(raw_items, list):
                raise TypeError(f"{label} response has non-list items")
            items = [item for item in raw_items if isinstance(item, Mapping)]
            new_cursor = str(data.get("next_cursor") or "")
        else:
            raise TypeError(f"{label} returned {type(data).__name__}, expected object")

        written = append_jsonl(data_path, items)
        pages_done += 1
        rows_done += written
        meta = {
            "endpoint": endpoint,
            "params": dict(params),
            "page_size": page_size,
            "next_cursor": new_cursor,
            "pages": pages_done,
            "rows": rows_done,
            "complete": not bool(new_cursor),
            "last_page_rows": written,
            "last_page_seconds": round(elapsed, 3),
            "updated_at": now_iso(),
        }
        write_json(meta_path, meta)
        print(
            f"{label}: page={pages_done} rows+={written} total={rows_done} "
            f"next={'yes' if new_cursor else 'no'} {elapsed:.2f}s",
            flush=True,
        )

        next_cursor = new_cursor
        if not next_cursor:
            return meta


def fetch_profiles(client: SECClient, args: argparse.Namespace) -> dict[str, Any]:
    return fetch_cursor_jsonl(
        client,
        endpoint="/v2/fund/general-info/profiles",
        params={},
        data_path=args.out / "profiles.jsonl",
        page_size=args.page_size,
        max_pages=args.max_pages,
        force=args.force,
        label="profiles",
    )


def has_thai_equity_policy(row: Mapping[str, Any], *, broad: bool) -> bool:
    policy = str(row.get("policy_desc") or "").strip()
    invest_policy = str(row.get("investment_policy_desc") or "").strip()
    if policy == THAI_EQUITY_POLICY:
        return True
    if not broad:
        return False
    text = f"{policy} {invest_policy} {row.get('proj_name_th') or ''} {row.get('proj_abbr_name') or ''}"
    include_terms = ("หุ้นไทย", "ตลาดหลักทรัพย์แห่งประเทศไทย", "SET", "SET50", "SET100", "MAI")
    exclude_terms = ("ต่างประเทศ", "Global", "China", "US", "Vietnam", "Feeder", "กองทุนหลัก")
    return any(term in text for term in include_terms) and not any(term in text for term in exclude_terms)


def classify_style(style: str) -> str:
    style = (style or "").strip().upper()
    if style == "AM":
        return "active"
    if style == "PM":
        return "passive"
    if style == "SM":
        return "semi_passive"
    if style in {"AN", "PN"}:
        return "feeder"
    if style in {"IM", "IN", "LM", "LN"}:
        return "inverse_leveraged"
    if style == "BH":
        return "buy_hold"
    if style:
        return "other"
    return "unknown"


def load_candidates(args: argparse.Namespace) -> list[dict[str, Any]]:
    profiles_path = args.out / "profiles.jsonl"
    if not profiles_path.exists():
        raise SystemExit(f"Missing {profiles_path}. Run `profiles` first.")

    seen: set[tuple[str, str]] = set()
    candidates: list[dict[str, Any]] = []
    for row in iter_jsonl(profiles_path):
        proj_id = str(row.get("proj_id") or "").strip()
        class_name = str(row.get("fund_class_name") or "main").strip() or "main"
        if not proj_id:
            continue
        if not has_thai_equity_policy(row, broad=args.broad_equity_filter):
            continue
        if args.domestic_only and str(row.get("invest_country_flag") or "").strip() != "3":
            continue
        style = str(row.get("management_style") or "").strip().upper()
        if args.exclude_special_styles and style in EXCLUDE_MANAGEMENT_STYLES:
            continue
        key = (proj_id, class_name)
        if key in seen:
            continue
        seen.add(key)
        out = dict(row)
        out["_style_bucket"] = classify_style(style)
        candidates.append(out)

    candidates.sort(key=lambda r: (str(r.get("proj_id") or ""), str(r.get("fund_class_name") or "")))
    if args.candidate_limit:
        candidates = candidates[: args.candidate_limit]
    return candidates


def write_candidates_csv(args: argparse.Namespace, candidates: list[Mapping[str, Any]]) -> Path:
    path = args.out / "thai_equity_candidates.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "proj_id",
        "fund_class_name",
        "proj_abbr_name",
        "proj_name_th",
        "unique_id",
        "comp_name_th",
        "fund_status",
        "init_date",
        "regis_date",
        "cancel_date",
        "policy_desc",
        "invest_country_flag",
        "management_style",
        "_style_bucket",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(candidates)
    return path


def fund_dirs(candidates: list[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    by_proj: dict[str, list[Mapping[str, Any]]] = {}
    for row in candidates:
        proj_id = str(row.get("proj_id") or "")
        by_proj.setdefault(proj_id, []).append(row)
    return by_proj


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())[:120]


def fetch_fund_endpoint(
    client: SECClient,
    *,
    args: argparse.Namespace,
    endpoint_name: str,
    proj_id: str,
    class_name: str | None = None,
) -> dict[str, Any]:
    endpoint = FUND_ENDPOINTS[endpoint_name]
    params: dict[str, Any] = {"proj_id": proj_id}
    if class_name and endpoint_name not in {"benchmarks", "asset_allocation", "dividends"}:
        params["fund_class_name"] = class_name
    if endpoint_name == "nav":
        if args.start_nav_date:
            params["start_nav_date"] = args.start_nav_date
        if args.end_nav_date:
            params["end_nav_date"] = args.end_nav_date

    folder = args.out / "funds" / safe_name(proj_id)
    suffix = safe_name(class_name or "all")
    data_path = folder / f"{endpoint_name}.{suffix}.jsonl"
    label = f"{endpoint_name}:{proj_id}:{class_name or 'all'}"
    return fetch_cursor_jsonl(
        client,
        endpoint=endpoint,
        params=params,
        data_path=data_path,
        page_size=args.page_size,
        max_pages=args.max_pages_per_fund,
        force=args.force,
        label=label,
    )


def fetch_funds(client: SECClient, args: argparse.Namespace) -> dict[str, Any]:
    candidates = load_candidates(args)
    candidates_path = write_candidates_csv(args, candidates)
    by_proj = fund_dirs(candidates)
    print(
        f"candidate classes={len(candidates)} projects={len(by_proj)} "
        f"summary={candidates_path}",
        flush=True,
    )

    endpoint_names = list(args.endpoint)
    summary = {
        "candidate_classes": len(candidates),
        "candidate_projects": len(by_proj),
        "endpoints": endpoint_names,
        "started_at": now_iso(),
        "projects": {},
    }
    write_json(args.out / "fund_export_manifest.json", summary)

    for proj_i, (proj_id, rows) in enumerate(by_proj.items(), start=1):
        project_summary: dict[str, Any] = {"classes": len(rows), "endpoints": {}}
        print(f"project {proj_i}/{len(by_proj)} {proj_id} classes={len(rows)}", flush=True)
        class_names = sorted({str(row.get("fund_class_name") or "main") for row in rows})
        for endpoint_name in endpoint_names:
            if endpoint_name in {"benchmarks", "asset_allocation", "dividends"}:
                meta = fetch_fund_endpoint(
                    client, args=args, endpoint_name=endpoint_name, proj_id=proj_id, class_name=None
                )
                project_summary["endpoints"][endpoint_name] = meta
                continue
            for class_name in class_names:
                meta = fetch_fund_endpoint(
                    client,
                    args=args,
                    endpoint_name=endpoint_name,
                    proj_id=proj_id,
                    class_name=class_name,
                )
                project_summary["endpoints"][f"{endpoint_name}.{class_name}"] = meta
        summary["projects"][proj_id] = project_summary
        summary["updated_at"] = now_iso()
        write_json(args.out / "fund_export_manifest.json", summary)

    summary["completed_at"] = now_iso()
    write_json(args.out / "fund_export_manifest.json", summary)
    return summary


def build_client(args: argparse.Namespace) -> SECClient:
    return SECClient(
        calls=args.calls,
        period=args.period,
        min_interval=args.min_interval,
        timeout=args.timeout,
        max_retries=args.max_retries,
    )


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--max-pages-per-fund", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--calls", type=int, default=4500)
    parser.add_argument("--period", type=float, default=300.0)
    parser.add_argument("--min-interval", type=float, default=0.08)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--max-retries", type=int, default=5)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_profiles = sub.add_parser("profiles", help="export all fund profiles")
    add_common_args(p_profiles)

    p_funds = sub.add_parser("funds", help="export per-fund datasets for Thai equity candidates")
    add_common_args(p_funds)
    p_funds.add_argument(
        "--endpoint",
        action="append",
        choices=sorted(FUND_ENDPOINTS),
        default=[],
        help="repeatable; default: benchmarks, performance, nav, dividends",
    )
    p_funds.add_argument("--candidate-limit", type=int, default=0)
    p_funds.add_argument("--broad-equity-filter", action="store_true")
    p_funds.add_argument(
        "--include-foreign-equity",
        dest="domestic_only",
        action="store_false",
        help="include equity funds whose invest_country_flag is not 3",
    )
    p_funds.set_defaults(domestic_only=True)
    p_funds.add_argument("--exclude-special-styles", action="store_true", default=True)
    p_funds.add_argument("--start-nav-date", default="")
    p_funds.add_argument("--end-nav-date", default=dt.date.today().isoformat())

    p_all = sub.add_parser("all", help="profiles, then per-fund export")
    add_common_args(p_all)
    p_all.add_argument(
        "--endpoint",
        action="append",
        choices=sorted(FUND_ENDPOINTS),
        default=[],
        help="repeatable; default: benchmarks, performance, nav, dividends",
    )
    p_all.add_argument("--candidate-limit", type=int, default=0)
    p_all.add_argument("--broad-equity-filter", action="store_true")
    p_all.add_argument(
        "--include-foreign-equity",
        dest="domestic_only",
        action="store_false",
        help="include equity funds whose invest_country_flag is not 3",
    )
    p_all.set_defaults(domestic_only=True)
    p_all.add_argument("--exclude-special-styles", action="store_true", default=True)
    p_all.add_argument("--start-nav-date", default="")
    p_all.add_argument("--end-nav-date", default=dt.date.today().isoformat())

    p_summary = sub.add_parser("summary", help="write Thai equity candidate CSV from profiles")
    add_common_args(p_summary)
    p_summary.add_argument("--candidate-limit", type=int, default=0)
    p_summary.add_argument("--broad-equity-filter", action="store_true")
    p_summary.add_argument(
        "--include-foreign-equity",
        dest="domestic_only",
        action="store_false",
        help="include equity funds whose invest_country_flag is not 3",
    )
    p_summary.set_defaults(domestic_only=True)
    p_summary.add_argument("--exclude-special-styles", action="store_true", default=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    if hasattr(args, "endpoint") and not args.endpoint:
        args.endpoint = ["benchmarks", "performance", "nav", "dividends"]

    try:
        if args.command == "profiles":
            fetch_profiles(build_client(args), args)
        elif args.command == "summary":
            candidates = load_candidates(args)
            path = write_candidates_csv(args, candidates)
            print(f"candidate classes={len(candidates)} projects={len(fund_dirs(candidates))} summary={path}")
        elif args.command == "funds":
            fetch_funds(build_client(args), args)
        elif args.command == "all":
            client = build_client(args)
            fetch_profiles(client, args)
            fetch_funds(client, args)
        return 0
    except KeyboardInterrupt:
        print("interrupted; rerun the same command to resume", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
