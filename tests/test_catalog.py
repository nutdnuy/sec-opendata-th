import gzip
import json

from secopendata.catalog import FundCatalog, build_catalog
from secopendata.cli import main


def _catalog_file(tmp_path):
    path = tmp_path / "fund_catalog.json.gz"
    payload = {
        "metadata": {"as_of": "2026-06-18", "amc_count": 2, "fund_count": 3},
        "amcs": [
            {
                "unique_id": "C1",
                "comp_name_th": "บริษัทหลักทรัพย์จัดการกองทุน กสิกรไทย จำกัด",
                "comp_name_en": "KASIKORN ASSET MANAGEMENT COMPANY LIMITED",
            },
            {
                "unique_id": "C2",
                "comp_name_th": "บริษัทหลักทรัพย์จัดการกองทุน ไทยพาณิชย์ จำกัด",
                "comp_name_en": "SCB ASSET MANAGEMENT COMPANY LIMITED",
            },
        ],
        "funds": [
            {
                "unique_id": "C1",
                "proj_id": "M1",
                "proj_name_th": "กองทุนเปิดเค หุ้นไทย",
                "proj_name_en": "K Thai Equity Fund",
                "proj_abbr_name": "K-THAI",
                "fund_status": "Registered",
                "fund_class_name": "main",
            },
            {
                "unique_id": "C1",
                "proj_id": "M2",
                "proj_name_th": "กองทุนเปิดเค ตราสารหนี้",
                "proj_name_en": "K Fixed Income Fund",
                "proj_abbr_name": "K-FIXED",
                "fund_status": "Liquidated",
                "fund_class_name": "main",
            },
            {
                "unique_id": "C2",
                "proj_id": "M3",
                "proj_name_th": "กองทุนเปิดไทยพาณิชย์ หุ้นไทย",
                "proj_name_en": "SCB Thai Equity Fund",
                "proj_abbr_name": "SCBSET",
                "fund_status": "Registered",
                "fund_class_name": "SCBSET-A",
            },
        ],
    }
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    return path


def test_search_amcs_matches_thai_english_and_id(tmp_path):
    catalog = FundCatalog.from_path(_catalog_file(tmp_path))

    assert catalog.search_amcs("กสิกร")[0]["unique_id"] == "C1"
    assert catalog.search_amcs("scb")[0]["unique_id"] == "C2"
    assert catalog.search_amcs("C1")[0]["comp_name_en"].startswith("KASIKORN")


def test_search_funds_prefers_exact_abbreviation_and_adds_amc_names(tmp_path):
    catalog = FundCatalog.from_path(_catalog_file(tmp_path))

    result = catalog.search_funds("k-thai")

    assert result[0]["proj_id"] == "M1"
    assert result[0]["comp_name_th"].endswith("กสิกรไทย จำกัด")


def test_search_funds_filters_by_amc_and_registered_status(tmp_path):
    catalog = FundCatalog.from_path(_catalog_file(tmp_path))

    result = catalog.search_funds("หุ้นไทย", amc="scb", status="Registered")

    assert [row["proj_id"] for row in result] == ["M3"]


def test_catalog_info_returns_snapshot_metadata(tmp_path):
    catalog = FundCatalog.from_path(_catalog_file(tmp_path))

    assert catalog.info() == {
        "as_of": "2026-06-18",
        "amc_count": 2,
        "fund_count": 3,
    }


def test_fund_search_cli_is_offline_and_emits_json(tmp_path, monkeypatch, capsys):
    catalog = FundCatalog.from_path(_catalog_file(tmp_path))
    monkeypatch.setattr(FundCatalog, "bundled", classmethod(lambda cls: catalog))

    assert main(["fund-search", "SCBSET"]) == 0
    output = json.loads(capsys.readouterr().out)

    assert output[0]["proj_id"] == "M3"


def test_catalog_info_cli_emits_snapshot_date(tmp_path, monkeypatch, capsys):
    catalog = FundCatalog.from_path(_catalog_file(tmp_path))
    monkeypatch.setattr(FundCatalog, "bundled", classmethod(lambda cls: catalog))

    assert main(["catalog-info"]) == 0

    assert json.loads(capsys.readouterr().out)["as_of"] == "2026-06-18"


def test_amc_search_cli_finds_thai_name(tmp_path, monkeypatch, capsys):
    catalog = FundCatalog.from_path(_catalog_file(tmp_path))
    monkeypatch.setattr(FundCatalog, "bundled", classmethod(lambda cls: catalog))

    assert main(["amc-search", "กสิกร"]) == 0

    assert json.loads(capsys.readouterr().out)[0]["unique_id"] == "C1"


def test_build_catalog_compacts_profile_jsonl_and_deduplicates(tmp_path):
    source = tmp_path / "profiles.jsonl"
    rows = [
        {
            "unique_id": "C1",
            "comp_name_th": "บลจ. กสิกรไทย",
            "comp_name_en": "KASIKORN ASSET MANAGEMENT",
            "proj_id": "M1",
            "regis_id": "MF1",
            "proj_name_th": "กองทุนเปิดเค หุ้นไทย",
            "proj_name_en": "K Thai Equity Fund",
            "proj_abbr_name": "K-THAI",
            "fund_status": "Registered",
            "fund_class_name": "main",
            "cancel_date": None,
            "investment_policy_desc": "large field that must not be bundled",
            "last_upd_date": "2026-06-18T15:20:16.6",
        },
    ]
    source.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows * 2))
    target = tmp_path / "catalog.json.gz"

    metadata = build_catalog(source, target)
    catalog = FundCatalog.from_path(target)

    assert metadata["amc_count"] == 1
    assert metadata["fund_count"] == 1
    assert metadata["as_of"] == "2026-06-18"
    assert "investment_policy_desc" not in catalog.search_funds("K-THAI")[0]
