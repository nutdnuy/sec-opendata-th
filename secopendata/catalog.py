"""Offline lookup for the bundled SEC mutual-fund and AMC snapshot."""
from __future__ import annotations

import gzip
import io
import json
import re
import unicodedata
from importlib import resources
from pathlib import Path
from typing import Any


AMC_FIELDS = ("unique_id", "comp_name_th", "comp_name_en")
FUND_FIELDS = (
    "unique_id",
    "proj_id",
    "regis_id",
    "proj_name_th",
    "proj_name_en",
    "proj_abbr_name",
    "fund_status",
    "fund_class_name",
    "fund_class_tax_incentive_type",
    "init_date",
    "regis_date",
    "cancel_date",
    "policy_desc",
)


def _normalize(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return " ".join(re.findall(r"[\wก-๙]+", text))


def _contains_all(query: str, values: list[Any]) -> bool:
    tokens = _normalize(query).split()
    haystack = " ".join(_normalize(value) for value in values)
    return all(token in haystack for token in tokens)


def build_catalog(source: str | Path, target: str | Path) -> dict[str, Any]:
    """Compact a SEC v2 profile JSONL export into the bundled lookup format."""
    amcs: dict[str, dict[str, Any]] = {}
    funds: dict[tuple[str, str], dict[str, Any]] = {}
    as_of = ""
    with Path(source).open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            row = json.loads(line)
            unique_id = str(row.get("unique_id") or "")
            if unique_id:
                amcs[unique_id] = {field: row.get(field) for field in AMC_FIELDS}
            key = (
                str(row.get("proj_id") or ""),
                str(row.get("fund_class_name") or ""),
            )
            if key[0]:
                funds[key] = {field: row.get(field) for field in FUND_FIELDS}
            as_of = max(as_of, str(row.get("last_upd_date") or "")[:10])

    amc_rows = sorted(amcs.values(), key=lambda row: str(row.get("unique_id") or ""))
    fund_rows = sorted(
        funds.values(),
        key=lambda row: (
            str(row.get("proj_id") or ""),
            str(row.get("fund_class_name") or ""),
        ),
    )
    metadata = {
        "as_of": as_of,
        "amc_count": len(amc_rows),
        "fund_count": len(fund_rows),
        "project_count": len({row.get("proj_id") for row in fund_rows}),
        "source_endpoint": "/v2/fund/general-info/profiles",
    }
    payload = {"metadata": metadata, "amcs": amc_rows, "funds": fund_rows}
    target_path = Path(target)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with io.TextIOWrapper(zipped, encoding="utf-8") as text:
                json.dump(payload, text, ensure_ascii=False, separators=(",", ":"))
    return metadata


class FundCatalog:
    """In-memory search over a compact, versioned local fund snapshot."""

    def __init__(self, payload: dict[str, Any]):
        self.payload = payload
        self.amcs = list(payload.get("amcs", []))
        self.funds = list(payload.get("funds", []))
        self._amcs_by_id = {
            str(amc.get("unique_id") or ""): amc for amc in self.amcs
        }

    @classmethod
    def from_path(cls, path: str | Path) -> "FundCatalog":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return cls(json.load(fh))

    @classmethod
    def bundled(cls) -> "FundCatalog":
        path = resources.files("secopendata").joinpath("data/fund_catalog.json.gz")
        with resources.as_file(path) as local_path:
            return cls.from_path(local_path)

    def info(self) -> dict[str, Any]:
        return dict(self.payload.get("metadata", {}))

    def search_amcs(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        matches = []
        needle = _normalize(query)
        for amc in self.amcs:
            values = [
                amc.get("unique_id"),
                amc.get("comp_name_th"),
                amc.get("comp_name_en"),
            ]
            if not query or _contains_all(query, values):
                exact = needle in {_normalize(value) for value in values}
                starts = any(_normalize(value).startswith(needle) for value in values)
                matches.append((0 if exact else 1 if starts else 2, amc))
        matches.sort(key=lambda item: (item[0], _normalize(item[1].get("comp_name_th"))))
        return [dict(amc) for _, amc in matches[: max(limit, 0)]]

    def search_funds(
        self,
        query: str,
        *,
        amc: str = "",
        status: str = "",
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        allowed_amcs = {
            row.get("unique_id") for row in self.search_amcs(amc, limit=len(self.amcs))
        } if amc else set()
        needle = _normalize(query)
        status_needle = _normalize(status)
        matches = []
        for fund in self.funds:
            if allowed_amcs and fund.get("unique_id") not in allowed_amcs:
                continue
            if status_needle and _normalize(fund.get("fund_status")) != status_needle:
                continue
            values = [
                fund.get("proj_id"),
                fund.get("regis_id"),
                fund.get("proj_abbr_name"),
                fund.get("proj_name_th"),
                fund.get("proj_name_en"),
                fund.get("fund_class_name"),
            ]
            if query and not _contains_all(query, values):
                continue
            exact = needle in {
                _normalize(fund.get("proj_id")),
                _normalize(fund.get("regis_id")),
                _normalize(fund.get("proj_abbr_name")),
                _normalize(fund.get("fund_class_name")),
            }
            starts = any(_normalize(value).startswith(needle) for value in values)
            row = dict(fund)
            row.update(self._amcs_by_id.get(str(fund.get("unique_id") or ""), {}))
            matches.append((0 if exact else 1 if starts else 2, row))
        matches.sort(
            key=lambda item: (
                item[0],
                _normalize(item[1].get("proj_abbr_name")),
                _normalize(item[1].get("fund_class_name")),
            )
        )
        return [row for _, row in matches[: max(limit, 0)]]
