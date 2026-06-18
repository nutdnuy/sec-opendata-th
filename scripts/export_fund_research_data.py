#!/usr/bin/env python3
"""Export SEC Open Data v2 fund research endpoints to JSONL and CSV.

The exporter is intentionally standalone so research pulls can be resumed
without changing the core secopendata package. JSONL is the authoritative append
log. CSV is kept in sync and rebuilt from JSONL when resume recovery or schema
growth requires it.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from secopendata import MissingKeyError, NotSubscribedError, SECAPIError, SECClient


MIN_INTERVAL_SECONDS = 0.020
MAX_PAGE_SIZE = 100
CURSOR_PARAM = "next_cursor"
KEY_SCOPE = "fund"
STATE_VERSION = 1


@dataclass(frozen=True)
class EndpointSpec:
    name: str
    path: str
    description: str


ENDPOINTS: dict[str, EndpointSpec] = {
    "profiles": EndpointSpec(
        "profiles",
        "/v2/fund/general-info/profiles",
        "Fund profiles and general information, including fund status and policy fields.",
    ),
    "performance": EndpointSpec(
        "performance",
        "/v2/fund/factsheet/performance",
        "Historical fund performance rows from fund factsheets.",
    ),
    "benchmarks": EndpointSpec(
        "benchmarks",
        "/v2/fund/factsheet/benchmarks",
        "Fund benchmark rows from fund factsheets.",
    ),
    "nav": EndpointSpec(
        "nav",
        "/v2/fund/daily-info/nav",
        "Daily NAV rows for mutual funds.",
    ),
    "dividends": EndpointSpec(
        "dividends",
        "/v2/fund/daily-info/dividend-history",
        "Dividend history rows for total-return reconstruction.",
    ),
}


class ExportError(RuntimeError):
    """Recoverable CLI-level error with a user-facing message."""


def utc_now() -> str:
    return (
        dt.datetime.now(dt.UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def parse_query_params(pairs: Sequence[str] | None) -> dict[str, str]:
    params: dict[str, str] = {}
    for raw in pairs or []:
        if "=" not in raw:
            raise ExportError(f"--param expects KEY=VALUE, got: {raw}")
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key:
            raise ExportError(f"--param key is empty in: {raw}")
        if key in {CURSOR_PARAM, "page_size"}:
            raise ExportError(f"{key} is controlled by the exporter; do not pass it via --param.")
        params[key] = value
    return params


def selected_endpoints(name: str) -> list[EndpointSpec]:
    if name == "all":
        return [ENDPOINTS[key] for key in ("profiles", "performance", "benchmarks", "nav", "dividends")]
    return [ENDPOINTS[name]]


def request_fingerprint(spec: EndpointSpec, params: Mapping[str, str], page_size: int) -> str:
    payload = {
        "state_version": STATE_VERSION,
        "endpoint": spec.name,
        "path": spec.path,
        "key_scope": KEY_SCOPE,
        "cursor_param": CURSOR_PARAM,
        "page_size": page_size,
        "params": dict(sorted(params.items())),
    }
    encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def state_template(
    spec: EndpointSpec,
    output_dir: Path,
    params: Mapping[str, str],
    page_size: int,
    fingerprint: str,
) -> dict[str, Any]:
    now = utc_now()
    return {
        "state_version": STATE_VERSION,
        "endpoint": spec.name,
        "path": spec.path,
        "key_scope": KEY_SCOPE,
        "params": dict(sorted(params.items())),
        "page_size": page_size,
        "cursor_param": CURSOR_PARAM,
        "request_fingerprint": fingerprint,
        "next_cursor": "",
        "pages_completed": 0,
        "rows_written": 0,
        "jsonl_offset": 0,
        "csv_fieldnames": [],
        "complete": False,
        "stop_reason": "",
        "created_at": now,
        "updated_at": now,
        "outputs": {
            "jsonl": str(output_dir / f"{spec.name}.jsonl"),
            "csv": str(output_dir / f"{spec.name}.csv"),
            "progress": str(output_dir / f"{spec.name}.progress.json"),
        },
    }


def output_paths(output_dir: Path, spec: EndpointSpec) -> dict[str, Path]:
    return {
        "jsonl": output_dir / f"{spec.name}.jsonl",
        "csv": output_dir / f"{spec.name}.csv",
        "progress": output_dir / f"{spec.name}.progress.json",
    }


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ExportError(f"Progress file is not a JSON object: {path}")
    return data


def atomic_write_json(path: Path, data: Mapping[str, Any]) -> None:
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def prepare_state(
    spec: EndpointSpec,
    output_dir: Path,
    params: Mapping[str, str],
    page_size: int,
    *,
    resume: bool,
    overwrite: bool,
) -> tuple[dict[str, Any], dict[str, Path]]:
    paths = output_paths(output_dir, spec)
    fingerprint = request_fingerprint(spec, params, page_size)

    if resume and overwrite:
        raise ExportError("Use either --resume or --overwrite, not both.")

    if overwrite:
        for path in paths.values():
            path.unlink(missing_ok=True)

    existing = [path for path in paths.values() if path.exists()]
    if resume:
        if paths["progress"].exists():
            state = load_json(paths["progress"])
            if state.get("request_fingerprint") != fingerprint:
                raise ExportError(
                    f"{spec.name}: progress fingerprint differs from this request. "
                    "Use matching --param/--page-size values, or start over with --overwrite."
                )
            return state, paths
        if existing:
            raise ExportError(
                f"{spec.name}: output files exist but no progress file was found; "
                "move them aside or use --overwrite."
            )
        return state_template(spec, output_dir, params, page_size, fingerprint), paths

    if existing:
        names = ", ".join(path.name for path in existing)
        raise ExportError(
            f"{spec.name}: output already exists ({names}). "
            "Use --resume to continue or --overwrite to replace."
        )

    return state_template(spec, output_dir, params, page_size, fingerprint), paths


def truncate_jsonl_to_committed_offset(path: Path, offset: int) -> None:
    if not path.exists():
        if offset:
            raise ExportError(f"Expected JSONL offset {offset}, but {path} does not exist.")
        return
    size = path.stat().st_size
    if size < offset:
        raise ExportError(f"{path.name} is shorter than committed offset {offset}.")
    if size > offset:
        with path.open("ab") as fh:
            fh.truncate(offset)


def iter_jsonl(path: Path) -> Iterable[Any]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                yield json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ExportError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":"))


def flatten_record(record: Any) -> dict[str, Any]:
    if isinstance(record, Mapping):
        return {str(key): csv_value(value) for key, value in record.items()}
    return {"value": csv_value(record)}


def merged_fieldnames(existing: Sequence[str], records: Sequence[Any]) -> list[str]:
    fields = list(existing)
    seen = set(fields)
    for record in records:
        for key in flatten_record(record):
            if key not in seen:
                fields.append(key)
                seen.add(key)
    return fields


def append_jsonl(path: Path, records: Sequence[Any]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for record in records:
            json.dump(record, fh, ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":"))
            fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    return path.stat().st_size


def write_csv_rows(path: Path, fieldnames: Sequence[str], records: Iterable[Any], *, append: bool) -> None:
    mode = "a" if append else "w"
    with path.open(mode, newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if not append:
            writer.writeheader()
        for record in records:
            writer.writerow(flatten_record(record))
        fh.flush()
        os.fsync(fh.fileno())


def rebuild_csv_from_jsonl(jsonl_path: Path, csv_path: Path, fieldnames: Sequence[str]) -> None:
    tmp = csv_path.with_name(csv_path.name + ".tmp")
    if not fieldnames:
        csv_path.unlink(missing_ok=True)
        tmp.unlink(missing_ok=True)
        return
    write_csv_rows(tmp, fieldnames, iter_jsonl(jsonl_path), append=False)
    os.replace(tmp, csv_path)


def recover_outputs(paths: Mapping[str, Path], state: Mapping[str, Any]) -> list[str]:
    offset = int(state.get("jsonl_offset") or 0)
    truncate_jsonl_to_committed_offset(paths["jsonl"], offset)
    fieldnames = merged_fieldnames(state.get("csv_fieldnames") or [], list(iter_jsonl(paths["jsonl"])))
    rebuild_csv_from_jsonl(paths["jsonl"], paths["csv"], fieldnames)
    return fieldnames


def commit_records(
    paths: Mapping[str, Path],
    state: dict[str, Any],
    records: Sequence[Any],
) -> None:
    expected_offset = int(state.get("jsonl_offset") or 0)
    actual_offset = paths["jsonl"].stat().st_size if paths["jsonl"].exists() else 0
    if actual_offset != expected_offset:
        raise ExportError(
            f"{paths['jsonl'].name} size {actual_offset} does not match committed offset "
            f"{expected_offset}; retry with --resume to recover."
        )

    offset_after = append_jsonl(paths["jsonl"], records) if records else expected_offset
    old_fields = list(state.get("csv_fieldnames") or [])
    new_fields = merged_fieldnames(old_fields, records)

    if new_fields:
        if new_fields != old_fields or not paths["csv"].exists():
            rebuild_csv_from_jsonl(paths["jsonl"], paths["csv"], new_fields)
        elif records:
            write_csv_rows(paths["csv"], new_fields, records, append=True)

    state["jsonl_offset"] = offset_after
    state["csv_fieldnames"] = new_fields


def parse_page(data: Any) -> tuple[list[Any], str]:
    if data is None:
        return [], ""
    if isinstance(data, Mapping):
        if "items" not in data:
            return [dict(data)], ""
        items = data.get("items")
        if items is None:
            records: list[Any] = []
        elif isinstance(items, list):
            records = items
        else:
            raise ExportError("SEC v2 response field 'items' is not a list.")
        return records, str(data.get(CURSOR_PARAM) or "")
    if isinstance(data, list):
        return data, ""
    return [data], ""


def effective_page_size(page_size: int, max_rows: int, rows_written: int) -> int:
    if max_rows <= 0:
        return page_size
    remaining = max_rows - rows_written
    if remaining <= 0:
        return 0
    return min(page_size, remaining)


def emit(message: str, *, quiet: bool) -> None:
    if not quiet:
        print(message, file=sys.stderr)


def export_endpoint(
    client: SECClient,
    spec: EndpointSpec,
    output_dir: Path,
    params: Mapping[str, str],
    *,
    page_size: int,
    max_pages: int,
    max_rows: int,
    resume: bool,
    overwrite: bool,
    quiet: bool,
) -> dict[str, Any]:
    state, paths = prepare_state(
        spec,
        output_dir,
        params,
        page_size,
        resume=resume,
        overwrite=overwrite,
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    recovered_fields = recover_outputs(paths, state)
    if recovered_fields != state.get("csv_fieldnames"):
        state["csv_fieldnames"] = recovered_fields

    if state.get("complete"):
        emit(f"{spec.name}: already complete ({state.get('rows_written', 0)} rows).", quiet=quiet)
        return state

    while True:
        rows_written = int(state.get("rows_written") or 0)
        pages_completed = int(state.get("pages_completed") or 0)

        if max_rows > 0 and rows_written >= max_rows:
            state["stop_reason"] = "max_rows"
            state["updated_at"] = utc_now()
            atomic_write_json(paths["progress"], state)
            emit(f"{spec.name}: stopped at max_rows={max_rows}.", quiet=quiet)
            return state

        if pages_completed >= max_pages:
            state["stop_reason"] = "max_pages"
            state["updated_at"] = utc_now()
            atomic_write_json(paths["progress"], state)
            emit(f"{spec.name}: stopped at max_pages={max_pages}.", quiet=quiet)
            return state

        requested_page_size = effective_page_size(page_size, max_rows, rows_written)
        if requested_page_size <= 0:
            state["stop_reason"] = "max_rows"
            state["updated_at"] = utc_now()
            atomic_write_json(paths["progress"], state)
            return state

        cursor = str(state.get("next_cursor") or "")
        query = dict(params)
        query["page_size"] = requested_page_size
        query[CURSOR_PARAM] = cursor

        data = client.request("GET", spec.path, key_scope=KEY_SCOPE, params=query)
        records, next_cursor = parse_page(data)
        if next_cursor and next_cursor == cursor:
            raise ExportError(f"{spec.name}: SEC returned the same cursor twice; stopping to avoid a loop.")

        commit_records(paths, state, records)

        state["next_cursor"] = next_cursor
        state["pages_completed"] = pages_completed + 1
        state["rows_written"] = rows_written + len(records)
        state["updated_at"] = utc_now()
        if not next_cursor:
            state["complete"] = True
            state["stop_reason"] = "complete"

        atomic_write_json(paths["progress"], state)
        cursor_state = "more" if next_cursor else "end"
        emit(
            f"{spec.name}: page {state['pages_completed']} committed, "
            f"rows={state['rows_written']}, cursor={cursor_state}.",
            quiet=quiet,
        )

        if state.get("complete"):
            return state


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return parsed


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be >= 0")
    return parsed


def page_size_arg(value: str) -> int:
    parsed = positive_int(value)
    if parsed > MAX_PAGE_SIZE:
        raise argparse.ArgumentTypeError(f"must be <= {MAX_PAGE_SIZE} for SEC v2 fund endpoints")
    return parsed


def min_interval_arg(value: str) -> float:
    parsed = float(value)
    if parsed < MIN_INTERVAL_SECONDS * 1000:
        raise argparse.ArgumentTypeError("must be >= 20")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export SEC Open Data v2 fund endpoints for active-vs-passive research. "
            "Writes <endpoint>.jsonl, <endpoint>.csv, and <endpoint>.progress.json "
            "incrementally under --output-dir."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--endpoint",
        choices=["all", *ENDPOINTS.keys()],
        default="all",
        help="endpoint to export; 'all' runs profiles, performance, benchmarks, nav, then dividends",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="directory for JSONL, CSV, and progress metadata files",
    )
    parser.add_argument(
        "--page-size",
        type=page_size_arg,
        default=100,
        help="SEC cursor page size; v2 fund endpoints support 1-100",
    )
    parser.add_argument(
        "--max-pages",
        type=positive_int,
        default=1000,
        help="maximum total pages to fetch per endpoint, including resumed pages",
    )
    parser.add_argument(
        "--max-rows",
        type=non_negative_int,
        default=0,
        help="maximum total rows to write per endpoint; 0 means no row cap",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="resume from <endpoint>.progress.json and recover uncommitted JSONL/CSV data",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="delete existing output files for the selected endpoint(s) before starting",
    )
    parser.add_argument(
        "--param",
        action="append",
        metavar="KEY=VALUE",
        help=(
            "repeatable endpoint query parameter. Examples: latest=true, "
            "start_date=2024-01-01, end_date=2024-12-31, proj_id=M0001_2550, "
            "start_nav_date=2024-01-01. Do not pass page_size or next_cursor."
        ),
    )
    parser.add_argument(
        "--min-interval-ms",
        type=min_interval_arg,
        default=20.0,
        help="minimum delay between SEC requests in milliseconds; must be at least 20",
    )
    parser.add_argument("--timeout", type=positive_int, default=30, help="HTTP timeout in seconds")
    parser.add_argument(
        "--calls",
        type=positive_int,
        default=5000,
        help="rate-limit window call cap passed to SECClient",
    )
    parser.add_argument(
        "--period",
        type=positive_int,
        default=300,
        help="rate-limit window period in seconds passed to SECClient",
    )
    parser.add_argument("--quiet", action="store_true", help="suppress progress logs")
    return parser


def build_client(args: argparse.Namespace) -> SECClient:
    # SECClient defaults to the portal's 16 ms floor. This exporter is stricter
    # because large research pulls should leave a little more gateway headroom.
    return SECClient(
        calls=args.calls,
        period=float(args.period),
        min_interval=args.min_interval_ms / 1000.0,
        timeout=args.timeout,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        params = parse_query_params(args.param)
        client = build_client(args)
        results: list[dict[str, Any]] = []
        for spec in selected_endpoints(args.endpoint):
            results.append(
                export_endpoint(
                    client,
                    spec,
                    args.output_dir,
                    params,
                    page_size=args.page_size,
                    max_pages=args.max_pages,
                    max_rows=args.max_rows,
                    resume=args.resume,
                    overwrite=args.overwrite,
                    quiet=args.quiet,
                )
            )
        summary = [
            {
                "endpoint": state["endpoint"],
                "rows_written": state["rows_written"],
                "pages_completed": state["pages_completed"],
                "complete": state["complete"],
                "stop_reason": state["stop_reason"],
            }
            for state in results
        ]
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except MissingKeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    except NotSubscribedError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 4
    except SECAPIError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 5
    except ExportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
