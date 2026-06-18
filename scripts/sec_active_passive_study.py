#!/usr/bin/env python3
"""Build a Thai equity active-vs-passive study from SEC fund factsheet data."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import math
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from secopendata import SECClient


RAW_DEFAULT = Path("outputs/sec-active-passive/raw")
STUDY_DEFAULT = Path("outputs/sec-active-passive/study")
HORIZONS = ("1 year", "3 years", "5 years", "10 years")
RETURN_FUND = "ผลตอบแทนกองทุนรวม"
RETURN_BENCHMARK = "ผลตอบแทนตัวชี้วัด"
VOL_FUND = "ความผันผวนของกองทุนรวม"
VOL_BENCHMARK = "ความผันผวนของตัวชี้วัด"
POLICY_EQUITY_TH = "ตราสารทุน"
REPORT_DATE = dt.datetime.now().strftime("%Y-%m-%d %H:%M")


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
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def parse_number(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = float(value)
        return number if math.isfinite(number) else None
    text = str(value).strip().replace(",", "")
    if not text or text in {"-", "N/A", "n/a", "null", "None"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def style_bucket(style: Any) -> str:
    code = str(style or "").strip().upper()
    if code == "AM":
        return "active"
    if code == "PM":
        return "passive"
    if code == "SM":
        return "semi_passive"
    if code in {"AN", "PN"}:
        return "feeder"
    if code in {"IM", "IN", "LM", "LN"}:
        return "inverse_leveraged"
    if code == "BH":
        return "buy_hold"
    if code:
        return "other"
    return "unknown"


def is_equity_profile(row: Mapping[str, Any], *, include_foreign_equity: bool) -> bool:
    if str(row.get("policy_desc") or "").strip() != POLICY_EQUITY_TH:
        return False
    if include_foreign_equity:
        return True
    return str(row.get("invest_country_flag") or "").strip() == "3"


def load_candidates(raw_dir: Path, *, include_foreign_equity: bool = False) -> list[dict[str, Any]]:
    profiles_path = raw_dir / "profiles.jsonl"
    if not profiles_path.exists():
        raise SystemExit(f"Missing {profiles_path}. Run sec_fund_research_export.py profiles first.")

    seen: set[tuple[str, str]] = set()
    rows: list[dict[str, Any]] = []
    for profile in iter_jsonl(profiles_path):
        if not is_equity_profile(profile, include_foreign_equity=include_foreign_equity):
            continue
        proj_id = str(profile.get("proj_id") or "").strip()
        class_name = str(profile.get("fund_class_name") or "main").strip() or "main"
        if not proj_id:
            continue
        key = (proj_id, class_name)
        if key in seen:
            continue
        seen.add(key)
        row = dict(profile)
        row["_style_bucket"] = style_bucket(row.get("management_style"))
        rows.append(row)
    rows.sort(key=lambda r: (str(r.get("proj_id") or ""), str(r.get("fund_class_name") or "")))
    return rows


def fetch_cursor_rows(
    client: SECClient,
    path: str,
    params: Mapping[str, Any],
    *,
    page_size: int,
) -> list[dict[str, Any]]:
    query = dict(params)
    query["page_size"] = page_size
    cursor = ""
    rows: list[dict[str, Any]] = []
    while True:
        query["next_cursor"] = cursor
        data = client.request("GET", path, key_scope="fund", params=query)
        if data is None:
            return rows
        if not isinstance(data, Mapping):
            raise TypeError(f"{path} returned {type(data).__name__}")
        items = data.get("items") or []
        if not isinstance(items, list):
            raise TypeError(f"{path} returned non-list items")
        rows.extend(item for item in items if isinstance(item, Mapping))
        cursor = str(data.get("next_cursor") or "")
        if not cursor:
            return rows


def client_from_args(args: argparse.Namespace) -> SECClient:
    return SECClient(
        calls=args.calls,
        period=args.period,
        min_interval=args.min_interval,
        timeout=args.timeout,
        max_retries=args.max_retries,
    )


def fetch_latest(args: argparse.Namespace) -> None:
    candidates = load_candidates(args.raw_dir, include_foreign_equity=args.include_foreign_equity)
    if args.limit:
        candidates = candidates[: args.limit]
    args.out.mkdir(parents=True, exist_ok=True)

    perf_path = args.out / "latest_performance.jsonl"
    bench_path = args.out / "latest_benchmarks.jsonl"
    progress_path = args.out / "fetch_progress.json"
    if args.force:
        for path in (perf_path, bench_path, progress_path):
            path.unlink(missing_ok=True)

    progress = read_json(progress_path)
    done_perf = set(progress.get("done_performance", []))
    done_bench = set(progress.get("done_benchmarks", []))
    client = client_from_args(args)

    by_project = sorted({str(row.get("proj_id") or "") for row in candidates if row.get("proj_id")})
    for index, proj_id in enumerate(by_project, start=1):
        if proj_id in done_bench:
            continue
        started = time.monotonic()
        rows = fetch_cursor_rows(
            client,
            "/v2/fund/factsheet/benchmarks",
            {"proj_id": proj_id, "latest": "true"},
            page_size=args.page_size,
        )
        append_jsonl(bench_path, rows)
        done_bench.add(proj_id)
        progress["done_benchmarks"] = sorted(done_bench)
        progress["updated_at"] = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
        write_json(progress_path, progress)
        if not args.quiet:
            print(f"benchmarks {index}/{len(by_project)} {proj_id} rows={len(rows)} {time.monotonic()-started:.2f}s", flush=True)

    for index, row in enumerate(candidates, start=1):
        proj_id = str(row.get("proj_id") or "")
        class_name = str(row.get("fund_class_name") or "main") or "main"
        key = f"{proj_id}|{class_name}"
        if key in done_perf:
            continue
        started = time.monotonic()
        rows = fetch_cursor_rows(
            client,
            "/v2/fund/factsheet/performance",
            {"proj_id": proj_id, "fund_class_name": class_name, "latest": "true"},
            page_size=args.page_size,
        )
        tagged = []
        for item in rows:
            enriched = dict(item)
            enriched["_style_bucket"] = row["_style_bucket"]
            enriched["_fund_status"] = row.get("fund_status")
            enriched["_proj_abbr_name"] = row.get("proj_abbr_name")
            enriched["_proj_name_th"] = row.get("proj_name_th")
            enriched["_comp_name_th"] = row.get("comp_name_th")
            tagged.append(enriched)
        append_jsonl(perf_path, tagged)
        done_perf.add(key)
        progress["done_performance"] = sorted(done_perf)
        progress["updated_at"] = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
        write_json(progress_path, progress)
        if not args.quiet:
            print(f"performance {index}/{len(candidates)} {key} rows={len(rows)} {time.monotonic()-started:.2f}s", flush=True)

    write_candidates(args.out / "thai_equity_candidates.csv", candidates)
    progress["candidate_classes"] = len(candidates)
    progress["candidate_projects"] = len(by_project)
    progress["complete"] = True
    progress["completed_at"] = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    write_json(progress_path, progress)


def write_candidates(path: Path, rows: list[Mapping[str, Any]]) -> None:
    fields = [
        "proj_id",
        "fund_class_name",
        "proj_abbr_name",
        "proj_name_th",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def latest_benchmark_text(rows: Iterable[Mapping[str, Any]]) -> dict[str, str]:
    by_proj: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_proj[str(row.get("proj_id") or "")].append(row)
    out: dict[str, str] = {}
    for proj_id, items in by_proj.items():
        items.sort(key=lambda r: str(r.get("start_date") or ""), reverse=True)
        texts = [str(r.get("benchmark") or "").strip() for r in items if str(r.get("benchmark") or "").strip()]
        out[proj_id] = " | ".join(dict.fromkeys(texts[:4]))
    return out


def benchmark_family(text: str) -> str:
    upper = text.upper()
    if "SET50" in upper:
        return "SET50 TRI"
    if "SET100" in upper:
        return "SET100 TRI"
    if "MAI" in upper:
        return "MAI TRI"
    if "SET TRI" in upper or "ตลาดหลักทรัพย์แห่งประเทศไทย" in text:
        return "SET TRI"
    if "THAILAND" in upper:
        return "Thailand equity benchmark"
    return "other / composite"


def build_return_pairs(out_dir: Path) -> list[dict[str, Any]]:
    perf_rows = list(iter_jsonl(out_dir / "latest_performance.jsonl"))
    bench_text = latest_benchmark_text(iter_jsonl(out_dir / "latest_benchmarks.jsonl"))

    grouped: dict[tuple[str, str, str], dict[str, Mapping[str, Any]]] = defaultdict(dict)
    meta: dict[tuple[str, str], Mapping[str, Any]] = {}
    for row in perf_rows:
        proj_id = str(row.get("proj_id") or "")
        class_name = str(row.get("fund_class_name") or "main") or "main"
        period = str(row.get("reference_period") or "").strip()
        metric = str(row.get("performance_type_desc") or "").strip()
        if period not in HORIZONS:
            continue
        if metric in {RETURN_FUND, RETURN_BENCHMARK, VOL_FUND, VOL_BENCHMARK}:
            grouped[(proj_id, class_name, period)][metric] = row
            meta[(proj_id, class_name)] = row

    pairs: list[dict[str, Any]] = []
    for (proj_id, class_name, period), metrics in sorted(grouped.items()):
        fund = metrics.get(RETURN_FUND)
        benchmark = metrics.get(RETURN_BENCHMARK)
        if not fund or not benchmark:
            continue
        fund_ret = parse_number(fund.get("performance_value"))
        bench_ret = parse_number(benchmark.get("performance_value"))
        if fund_ret is None or bench_ret is None:
            continue
        m = meta.get((proj_id, class_name), {})
        benchmark_name = bench_text.get(proj_id, "")
        pair = {
            "proj_id": proj_id,
            "fund_class_name": class_name,
            "proj_abbr_name": m.get("_proj_abbr_name", ""),
            "proj_name_th": m.get("_proj_name_th", ""),
            "comp_name_th": m.get("_comp_name_th", ""),
            "fund_status": m.get("_fund_status", ""),
            "style_bucket": m.get("_style_bucket", ""),
            "horizon": period,
            "as_of_start_date": fund.get("start_date", ""),
            "fund_return_pct": fund_ret,
            "benchmark_return_pct": bench_ret,
            "excess_return_pct": fund_ret - bench_ret,
            "beat_benchmark": fund_ret > bench_ret,
            "benchmark_name": benchmark_name,
            "benchmark_family": benchmark_family(benchmark_name),
            "fund_vol_pct": parse_number(metrics.get(VOL_FUND, {}).get("performance_value")) if metrics.get(VOL_FUND) else None,
            "benchmark_vol_pct": parse_number(metrics.get(VOL_BENCHMARK, {}).get("performance_value")) if metrics.get(VOL_BENCHMARK) else None,
        }
        pairs.append(pair)
    return pairs


def canonical_project_pairs(pairs: list[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    by_key: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for row in pairs:
        by_key[(str(row["proj_id"]), str(row["horizon"]))].append(row)

    chosen: list[Mapping[str, Any]] = []
    for _, rows in by_key.items():
        rows = sorted(
            rows,
            key=lambda r: (
                0 if str(r.get("fund_class_name") or "").lower() == "main" else 1,
                str(r.get("fund_class_name") or ""),
            ),
        )
        chosen.append(rows[0])
    return sorted(chosen, key=lambda r: (str(r["horizon"]), str(r["proj_id"])))


def summarize(pairs: list[Mapping[str, Any]], *, project_level: bool) -> list[dict[str, Any]]:
    rows = canonical_project_pairs(pairs) if project_level else pairs
    summary: list[dict[str, Any]] = []
    for horizon in HORIZONS:
        for style in ("active", "passive", "semi_passive", "other"):
            bucket = [r for r in rows if r.get("horizon") == horizon and r.get("style_bucket") == style]
            if not bucket:
                continue
            wins = sum(1 for r in bucket if r.get("beat_benchmark") is True)
            excess = [float(r["excess_return_pct"]) for r in bucket if r.get("excess_return_pct") is not None]
            summary.append(
                {
                    "level": "project" if project_level else "class",
                    "horizon": horizon,
                    "style_bucket": style,
                    "eligible_count": len(bucket),
                    "winner_count": wins,
                    "win_rate": wins / len(bucket),
                    "median_excess_return_pct": statistics.median(excess) if excess else None,
                    "mean_excess_return_pct": statistics.fmean(excess) if excess else None,
                    "p25_excess_return_pct": percentile(excess, 25),
                    "p75_excess_return_pct": percentile(excess, 75),
                }
            )
    return summary


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    pos = (len(values) - 1) * pct / 100
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return values[int(pos)]
    return values[lower] + (values[upper] - values[lower]) * (pos - lower)


def write_csv(path: Path, rows: list[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pct(value: Any, digits: int = 1) -> str:
    number = parse_number(value)
    if number is None:
        return "n/a"
    return f"{number * 100:.{digits}f}%"


def num(value: Any, digits: int = 2, suffix: str = "") -> str:
    number = parse_number(value)
    if number is None:
        return "n/a"
    return f"{number:.{digits}f}{suffix}"


def html_escape(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def summary_lookup(summary: list[Mapping[str, Any]], *, level: str = "class") -> dict[tuple[str, str], Mapping[str, Any]]:
    return {
        (str(row["horizon"]), str(row["style_bucket"])): row
        for row in summary
        if row.get("level") == level
    }


def grouped_bar_svg(summary: list[Mapping[str, Any]], *, level: str, title: str) -> str:
    lookup = summary_lookup(summary, level=level)
    width, height = 860, 330
    margin_left, margin_right, margin_top, margin_bottom = 70, 30, 42, 58
    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom
    groups = list(HORIZONS)
    styles = [("active", "#69F0AE"), ("passive", "#03DAC6"), ("semi_passive", "#FFB74D"), ("other", "#B0BEC5")]
    slot = chart_w / len(groups)
    bar_w = min(32, slot / (len(styles) + 2))
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html_escape(title)}">',
        f'<text x="{margin_left}" y="24" class="chart-title">{html_escape(title)}</text>',
    ]
    for tick in range(0, 6):
        y = margin_top + chart_h - chart_h * tick / 5
        val = tick / 5
        parts.append(f'<line x1="{margin_left}" x2="{width-margin_right}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{margin_left-12}" y="{y+4:.1f}" text-anchor="end" class="axis">{val:.0%}</text>')
    for g_i, horizon in enumerate(groups):
        cx = margin_left + slot * g_i + slot / 2
        parts.append(f'<text x="{cx:.1f}" y="{height-24}" text-anchor="middle" class="axis strong">{horizon}</text>')
        for s_i, (style, color) in enumerate(styles):
            item = lookup.get((horizon, style))
            if not item:
                continue
            rate = float(item.get("win_rate") or 0)
            h = chart_h * max(0, min(rate, 1))
            x = cx - (len(styles) * bar_w) / 2 + s_i * bar_w
            y = margin_top + chart_h - h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w-4:.1f}" height="{h:.1f}" rx="4" fill="{color}"/>')
            parts.append(f'<text x="{x+(bar_w-4)/2:.1f}" y="{y-6:.1f}" text-anchor="middle" class="label">{rate:.0%}</text>')
    legend_x = margin_left
    for i, (style, color) in enumerate(styles):
        x = legend_x + i * 142
        parts.append(f'<rect x="{x}" y="{height-8}" width="10" height="10" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{x+16}" y="{height+1}" class="axis">{style.replace("_", " ")}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def excess_heatmap(summary: list[Mapping[str, Any]], *, level: str) -> str:
    lookup = summary_lookup(summary, level=level)
    styles = ("active", "passive", "semi_passive", "other")
    rows = []
    for style in styles:
        cells = [f"<th>{style.replace('_', ' ')}</th>"]
        for horizon in HORIZONS:
            item = lookup.get((horizon, style))
            value = item.get("median_excess_return_pct") if item else None
            number = parse_number(value)
            if number is None:
                color = "rgba(255,255,255,0.04)"
                label = "n/a"
            elif number >= 0:
                alpha = min(0.85, 0.12 + abs(number) / 12)
                color = f"rgba(0,230,118,{alpha:.2f})"
                label = f"+{number:.2f} pp"
            else:
                alpha = min(0.85, 0.12 + abs(number) / 12)
                color = f"rgba(255,82,82,{alpha:.2f})"
                label = f"{number:.2f} pp"
            cells.append(f'<td style="background:{color}"><span>{label}</span></td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    head = "".join(f"<th>{h}</th>" for h in HORIZONS)
    return f'<table class="heatmap"><thead><tr><th>Style</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def top_bottom_table(pairs: list[Mapping[str, Any]], *, horizon: str, style: str, best: bool) -> str:
    subset = [r for r in pairs if r.get("horizon") == horizon and r.get("style_bucket") == style]
    subset.sort(key=lambda r: float(r.get("excess_return_pct") or 0), reverse=best)
    rows = []
    for row in subset[:8]:
        cls = "positive" if float(row.get("excess_return_pct") or 0) >= 0 else "negative"
        rows.append(
            "<tr>"
            f"<td>{html_escape(row.get('proj_abbr_name') or row.get('proj_id'))}</td>"
            f"<td>{html_escape(row.get('fund_class_name'))}</td>"
            f"<td>{html_escape(row.get('benchmark_family'))}</td>"
            f"<td class='num {cls}'>{float(row.get('excess_return_pct') or 0):+.2f} pp</td>"
            "</tr>"
        )
    return "<table><thead><tr><th>Fund</th><th>Class</th><th>Benchmark</th><th>Excess</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def render_report(out_dir: Path, candidates: list[Mapping[str, Any]], pairs: list[Mapping[str, Any]], summary: list[Mapping[str, Any]]) -> None:
    class_summary = summary_lookup(summary, level="class")
    project_summary = summary_lookup(summary, level="project")
    active_1y = class_summary.get(("1 year", "active"), {})
    active_10y = class_summary.get(("10 years", "active"), {})
    passive_1y = class_summary.get(("1 year", "passive"), {})
    candidate_projects = len({r["proj_id"] for r in candidates})
    style_counts = Counter(r["_style_bucket"] for r in candidates)
    as_of_dates = Counter(str(r.get("as_of_start_date") or "") for r in pairs)
    common_as_of = as_of_dates.most_common(1)[0][0] if as_of_dates else "n/a"
    includes_foreign = any(str(r.get("invest_country_flag") or "").strip() != "3" for r in candidates)
    universe_text = (
        'policy_desc = "ตราสารทุน" รวมทุก invest_country_flag'
        if includes_foreign
        else 'policy_desc = "ตราสารทุน", invest_country_flag = 3'
    )

    insight_rows = []
    for horizon in HORIZONS:
        active = class_summary.get((horizon, "active"), {})
        passive = class_summary.get((horizon, "passive"), {})
        if active and passive:
            diff = float(active["win_rate"]) - float(passive["win_rate"])
            insight_rows.append(
                f"<tr><td>{horizon}</td><td>{pct(active['win_rate'])}</td><td>{pct(passive['win_rate'])}</td>"
                f"<td class='num {'positive' if diff >= 0 else 'negative'}'>{diff*100:+.1f} pp</td>"
                f"<td class='num'>{num(active.get('median_excess_return_pct'), 2, ' pp')}</td></tr>"
            )

    html_doc = f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thai Equity Funds: Active vs Passive</title>
<style>
:root {{
  --bg:#121212; --surface:#1D1D1D; --surface2:#242424; --surface3:#2E2E2E;
  --text:rgba(255,255,255,.87); --muted:rgba(255,255,255,.60); --line:rgba(255,255,255,.08);
  --green:#69F0AE; --profit:#00E676; --loss:#FF5252; --teal:#03DAC6; --warn:#FFB74D; --neutral:#B0BEC5;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:'IBM Plex Sans Thai','Inter',-apple-system,sans-serif; line-height:1.6; }}
main {{ width:min(1180px, calc(100% - 32px)); margin:0 auto; padding:32px 0 56px; }}
header {{ display:grid; grid-template-columns:1.3fr .7fr; gap:24px; align-items:end; padding:18px 0 26px; border-bottom:1px solid var(--line); }}
h1 {{ font-size:32px; line-height:1.22; margin:0 0 12px; font-weight:600; letter-spacing:0; }}
h2 {{ font-size:22px; margin:38px 0 14px; font-weight:600; }}
h3 {{ font-size:16px; margin:22px 0 10px; font-weight:600; }}
p {{ margin:0 0 14px; color:var(--muted); }}
.meta {{ color:var(--muted); font-size:13px; }}
.kpis {{ display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:12px; margin:24px 0; }}
.kpi {{ background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:16px; }}
.kpi .value {{ font-family:'JetBrains Mono','IBM Plex Mono',monospace; font-size:30px; line-height:1.1; color:var(--green); font-variant-numeric:tabular-nums; }}
.kpi .label {{ color:var(--muted); font-size:13px; margin-top:8px; }}
.panel {{ background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:18px; margin:14px 0; overflow-x:auto; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
th {{ background:var(--surface2); color:var(--text); text-align:left; font-weight:600; position:sticky; top:0; }}
th,td {{ padding:10px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
td.num, .num {{ text-align:right; font-family:'JetBrains Mono','IBM Plex Mono',monospace; font-variant-numeric:tabular-nums; white-space:nowrap; }}
.positive {{ color:var(--profit); }} .negative {{ color:var(--loss); }}
.chart-title {{ fill:var(--text); font-size:17px; font-weight:600; }}
.axis {{ fill:var(--muted); font-size:12px; }}
.axis.strong {{ fill:var(--text); }}
.label {{ fill:var(--text); font-size:11px; font-family:'JetBrains Mono','IBM Plex Mono',monospace; }}
.grid {{ stroke:rgba(255,255,255,.08); stroke-width:1; }}
.heatmap th,.heatmap td {{ text-align:center; }}
.heatmap span {{ font-family:'JetBrains Mono','IBM Plex Mono',monospace; color:var(--text); }}
.note {{ border-left:3px solid var(--warn); padding:10px 14px; background:rgba(255,183,77,.08); color:var(--muted); }}
a {{ color:var(--teal); }}
@media (max-width:820px) {{ header,.grid2 {{ grid-template-columns:1fr; }} .kpis {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
</style>
</head>
<body><main>
<header>
  <div>
    <h1>Thai Equity Funds: Active vs Passive</h1>
    <p>ศึกษากองทุนรวมหุ้นไทยจาก SEC Open Data โดยจับคู่ผลตอบแทนกองทุนกับผลตอบแทนตัวชี้วัดใน factsheet ล่าสุด แยกตาม active/passive และช่วงถือครอง 1, 3, 5, 10 ปี</p>
    <div class="meta">Generated {REPORT_DATE} Asia/Bangkok · Common factsheet effective date: {html_escape(common_as_of)}</div>
  </div>
  <div class="meta">
    Universe: {html_escape(universe_text)}.<br>
    Classification: SEC management_style, AM=active, PM=passive, SM=semi-passive.
  </div>
</header>

<section class="kpis">
  <div class="kpi"><div class="value">{len(candidates):,}</div><div class="label">share classes in Thai equity universe</div></div>
  <div class="kpi"><div class="value">{candidate_projects:,}</div><div class="label">fund projects before de-duplication</div></div>
  <div class="kpi"><div class="value">{pct(active_1y.get('win_rate'))}</div><div class="label">active class win rate, 1Y</div></div>
  <div class="kpi"><div class="value">{pct(active_10y.get('win_rate'))}</div><div class="label">active class win rate, 10Y</div></div>
</section>

<section>
  <h2>Headline Result</h2>
  <div class="panel">
    <table><thead><tr><th>Horizon</th><th>Active win rate</th><th>Passive win rate</th><th>Active - Passive</th><th>Active median excess</th></tr></thead>
    <tbody>{''.join(insight_rows)}</tbody></table>
  </div>
  <p class="note">ผลนี้เป็น factsheet-latest snapshot ไม่ใช่ rolling ทุกเดือนจาก NAV รายวัน. ข้อดีคือ benchmark return มาจากข้อมูลที่บลจ.รายงานกับ SEC ในชุดเดียวกัน จึงเทียบได้ทันที; งาน rolling start-date ยังต้องใช้ NAV + dividend หรือ historical factsheet rows เพิ่ม.</p>
</section>

<section>
  <h2>Win Rate By Horizon</h2>
  <div class="panel">{grouped_bar_svg(summary, level="class", title="Class-level beat rate versus declared benchmark")}</div>
  <div class="panel">{grouped_bar_svg(summary, level="project", title="Project-level beat rate, canonical share class")}</div>
</section>

<section>
  <h2>Median Excess Return</h2>
  <div class="panel">{excess_heatmap(summary, level="class")}</div>
</section>

<section class="grid2">
  <div>
    <h2>Best Active 5Y Excess</h2>
    <div class="panel">{top_bottom_table(pairs, horizon="5 years", style="active", best=True)}</div>
  </div>
  <div>
    <h2>Weakest Active 5Y Excess</h2>
    <div class="panel">{top_bottom_table(pairs, horizon="5 years", style="active", best=False)}</div>
  </div>
</section>

<section>
  <h2>Universe Mix</h2>
  <div class="panel">
    <table><thead><tr><th>Style bucket</th><th>Share classes</th></tr></thead><tbody>
      {''.join(f'<tr><td>{html_escape(k)}</td><td class="num">{v:,}</td></tr>' for k, v in style_counts.most_common())}
    </tbody></table>
  </div>
</section>

<section>
  <h2>Method Notes</h2>
  <p>ข้อมูลผลตอบแทนใช้ `performance_type_desc` = “ผลตอบแทนกองทุนรวม” เทียบกับ “ผลตอบแทนตัวชี้วัด” ใน endpoint `/v2/fund/factsheet/performance` พร้อม `latest=true`. หน่วยที่รายงานหลักคือ share class เพราะ class ต่างกันอาจมีค่าธรรมเนียมและนโยบายจ่ายปันผลต่างกัน; project-level ใช้ class `main` ก่อน ถ้าไม่มีใช้ชื่อ class แรกตามลำดับ.</p>
  <p>ข้อจำกัด: ยังไม่ใช่คำแนะนำลงทุน และยังไม่ใช่การพิสูจน์ว่า active/passive ดีกว่าในอนาคต. การทำ rolling “ซื้อตอนไหนก็ได้” อย่างเข้มต้องใช้ NAV รายวัน + dividend-history หรือดึง historical factsheet ทุกเดือน แล้วควบคุม survivorship bias เพิ่ม.</p>
</section>

</main></body></html>
"""
    (out_dir / "index.html").write_text(html_doc, encoding="utf-8")


def analyze(args: argparse.Namespace) -> None:
    candidates = load_candidates(args.raw_dir, include_foreign_equity=args.include_foreign_equity)
    if args.limit:
        candidates = candidates[: args.limit]
    pairs = build_return_pairs(args.out)
    if not pairs:
        raise SystemExit(f"No return pairs found in {args.out}. Run fetch-latest first.")
    summary = summarize(pairs, project_level=False) + summarize(pairs, project_level=True)
    write_csv(args.out / "latest_return_pairs.csv", pairs)
    write_csv(args.out / "summary_by_horizon_style.csv", summary)
    write_json(
        args.out / "study_manifest.json",
        {
            "generated_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
            "candidate_classes": len(candidates),
            "candidate_projects": len({r["proj_id"] for r in candidates}),
            "include_foreign_equity": args.include_foreign_equity,
            "return_pairs": len(pairs),
            "horizons": list(HORIZONS),
            "method": "SEC factsheet latest fund return versus factsheet benchmark return",
        },
    )
    render_report(args.out, candidates, pairs, summary)
    print(f"pairs={len(pairs)} summary={args.out / 'summary_by_horizon_style.csv'} report={args.out / 'index.html'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("fetch-latest", "analyze", "all"):
        p = sub.add_parser(name)
        p.add_argument("--raw-dir", type=Path, default=RAW_DEFAULT)
        p.add_argument("--out", type=Path, default=STUDY_DEFAULT)
        p.add_argument("--limit", type=int, default=0)
        p.add_argument(
            "--include-foreign-equity",
            action="store_true",
            help="include every policy_desc=ตราสารทุน fund instead of only invest_country_flag=3",
        )
        if name in {"fetch-latest", "all"}:
            p.add_argument("--page-size", type=int, default=100)
            p.add_argument("--force", action="store_true")
            p.add_argument("--quiet", action="store_true")
            p.add_argument("--calls", type=int, default=4500)
            p.add_argument("--period", type=float, default=300.0)
            p.add_argument("--min-interval", type=float, default=0.08)
            p.add_argument("--timeout", type=int, default=45)
            p.add_argument("--max-retries", type=int, default=5)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.raw_dir = args.raw_dir.resolve()
    args.out = args.out.resolve()
    try:
        if args.command == "fetch-latest":
            fetch_latest(args)
        elif args.command == "analyze":
            analyze(args)
        elif args.command == "all":
            fetch_latest(args)
            analyze(args)
        return 0
    except KeyboardInterrupt:
        print("interrupted; rerun the same command to resume", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
