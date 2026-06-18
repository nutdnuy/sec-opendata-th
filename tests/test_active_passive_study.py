from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sec_active_passive_study.py"
SPEC = importlib.util.spec_from_file_location("active_passive_study", SCRIPT_PATH)
assert SPEC and SPEC.loader
study = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = study
SPEC.loader.exec_module(study)


def write_profiles(path: Path, rows: list[dict[str, str]]) -> None:
    path.mkdir(parents=True, exist_ok=True)
    with (path / "profiles.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False))
            fh.write("\n")


def test_load_candidates_defaults_to_domestic_thai_equity(tmp_path):
    write_profiles(
        tmp_path,
        [
            {
                "proj_id": "TH_EQ",
                "fund_class_name": "A",
                "policy_desc": study.POLICY_EQUITY_TH,
                "invest_country_flag": "3",
                "management_style": "AM",
            },
            {
                "proj_id": "GLOBAL_EQ",
                "fund_class_name": "A",
                "policy_desc": study.POLICY_EQUITY_TH,
                "invest_country_flag": "1",
                "management_style": "PM",
            },
            {
                "proj_id": "NOT_EQ",
                "fund_class_name": "A",
                "policy_desc": "fixed income",
                "invest_country_flag": "3",
                "management_style": "AM",
            },
        ],
    )

    candidates = study.load_candidates(tmp_path)

    assert [row["proj_id"] for row in candidates] == ["TH_EQ"]
    assert candidates[0]["_style_bucket"] == "active"


def test_load_candidates_can_include_all_equity_funds(tmp_path):
    write_profiles(
        tmp_path,
        [
            {
                "proj_id": "TH_EQ",
                "fund_class_name": "A",
                "policy_desc": study.POLICY_EQUITY_TH,
                "invest_country_flag": "3",
                "management_style": "AM",
            },
            {
                "proj_id": "GLOBAL_EQ",
                "fund_class_name": "A",
                "policy_desc": study.POLICY_EQUITY_TH,
                "invest_country_flag": "1",
                "management_style": "PM",
            },
            {
                "proj_id": "GLOBAL_EQ",
                "fund_class_name": "A",
                "policy_desc": study.POLICY_EQUITY_TH,
                "invest_country_flag": "1",
                "management_style": "PM",
            },
        ],
    )

    candidates = study.load_candidates(tmp_path, include_foreign_equity=True)

    assert [row["proj_id"] for row in candidates] == ["GLOBAL_EQ", "TH_EQ"]
    assert {row["_style_bucket"] for row in candidates} == {"active", "passive"}
