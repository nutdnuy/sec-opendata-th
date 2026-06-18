from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "export_fund_research_data.py"
SPEC = importlib.util.spec_from_file_location("fund_research_exporter", SCRIPT_PATH)
assert SPEC and SPEC.loader
exporter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = exporter
SPEC.loader.exec_module(exporter)


class FakeClient:
    def __init__(self, pages):
        self.pages = list(pages)
        self.calls = []

    def request(self, method, path, *, key_scope=None, params=None, json_body=None):
        self.calls.append(
            {
                "method": method,
                "path": path,
                "key_scope": key_scope,
                "params": dict(params or {}),
            }
        )
        if not self.pages:
            raise AssertionError("unexpected extra request")
        return self.pages.pop(0)


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def read_csv_rows(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_export_endpoint_writes_jsonl_csv_and_progress_incrementally(tmp_path):
    client = FakeClient(
        [
            {
                "message": "success",
                "page_size": 2,
                "next_cursor": "abc",
                "items": [{"proj_id": "A", "nested": {"x": 1}}],
            },
            {
                "message": "success",
                "page_size": 2,
                "next_cursor": "",
                "items": [{"proj_id": "B", "new_field": 2}],
            },
        ]
    )

    state = exporter.export_endpoint(
        client,
        exporter.ENDPOINTS["performance"],
        tmp_path,
        {"latest": "true"},
        page_size=2,
        max_pages=10,
        max_rows=0,
        resume=False,
        overwrite=False,
        quiet=True,
    )

    assert state["complete"] is True
    assert state["rows_written"] == 2
    assert state["pages_completed"] == 2
    assert client.calls[0]["params"] == {"latest": "true", "page_size": 2, "next_cursor": ""}
    assert client.calls[1]["params"] == {"latest": "true", "page_size": 2, "next_cursor": "abc"}

    assert read_jsonl(tmp_path / "performance.jsonl") == [
        {"nested": {"x": 1}, "proj_id": "A"},
        {"new_field": 2, "proj_id": "B"},
    ]

    csv_rows = read_csv_rows(tmp_path / "performance.csv")
    assert csv_rows[0]["proj_id"] == "A"
    assert csv_rows[0]["nested"] == '{"x":1}'
    assert csv_rows[1]["proj_id"] == "B"
    assert csv_rows[1]["new_field"] == "2"

    progress = json.loads((tmp_path / "performance.progress.json").read_text(encoding="utf-8"))
    assert progress["next_cursor"] == ""
    assert progress["stop_reason"] == "complete"
    assert "Ocp-Apim-Subscription-Key" not in json.dumps(progress)


def test_resume_truncates_uncommitted_jsonl_and_rebuilds_csv(tmp_path):
    first_client = FakeClient(
        [
            {
                "message": "success",
                "page_size": 1,
                "next_cursor": "abc",
                "items": [{"proj_id": "A"}],
            }
        ]
    )
    first_state = exporter.export_endpoint(
        first_client,
        exporter.ENDPOINTS["performance"],
        tmp_path,
        {},
        page_size=1,
        max_pages=1,
        max_rows=0,
        resume=False,
        overwrite=False,
        quiet=True,
    )
    assert first_state["stop_reason"] == "max_pages"

    with (tmp_path / "performance.jsonl").open("a", encoding="utf-8") as fh:
        fh.write('{"proj_id":"UNCOMMITTED"}\n')
    with (tmp_path / "performance.csv").open("a", encoding="utf-8") as fh:
        fh.write("UNCOMMITTED\n")

    second_client = FakeClient(
        [
            {
                "message": "success",
                "page_size": 1,
                "next_cursor": "",
                "items": [{"proj_id": "B"}],
            }
        ]
    )
    final_state = exporter.export_endpoint(
        second_client,
        exporter.ENDPOINTS["performance"],
        tmp_path,
        {},
        page_size=1,
        max_pages=10,
        max_rows=0,
        resume=True,
        overwrite=False,
        quiet=True,
    )

    assert final_state["complete"] is True
    assert second_client.calls[0]["params"]["next_cursor"] == "abc"
    assert read_jsonl(tmp_path / "performance.jsonl") == [{"proj_id": "A"}, {"proj_id": "B"}]
    assert [row["proj_id"] for row in read_csv_rows(tmp_path / "performance.csv")] == ["A", "B"]
