import pytest
import responses

from secopendata import FundDailyInfo, FundFactsheet, SECClient
from secopendata.client import BASE_URL


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SEC_API_KEY", "test-key")
    return SECClient()


@responses.activate
def test_amc_list(client):
    responses.add(responses.GET, f"{BASE_URL}/FundFactsheet/fund/amc",
                  json=[{"unique_id": "C1", "name_en": "KASIKORN ASSET"}], status=200)
    assert FundFactsheet(client).amc_list()[0]["name_en"] == "KASIKORN ASSET"


@responses.activate
def test_find_and_resolve_amc(client):
    responses.add(responses.GET, f"{BASE_URL}/FundFactsheet/fund/amc",
                  json=[{"unique_id": "C0000000021", "name_en": "KASIKORN ASSET MANAGEMENT"}],
                  status=200)
    ff = FundFactsheet(client)
    assert ff.resolve_amc_id("kasikorn") == "C0000000021"
    assert ff.resolve_amc_id("C0000000021") == "C0000000021"
    assert ff.resolve_amc_id("nope") is None


@responses.activate
def test_classes_404_is_empty(client):
    responses.add(responses.GET, f"{BASE_URL}/FundFactsheet/fund/P1/class", status=404)
    assert FundFactsheet(client).classes("P1") == []


@responses.activate
def test_daily_nav_path(client):
    responses.add(responses.GET, f"{BASE_URL}/FundDailyInfo/P1/dailynav/2026-06-16",
                  json=[{"last_val": 12.34}], status=200)
    out = FundDailyInfo(client).daily_nav("P1", "2026-06-16")
    assert out[0]["last_val"] == 12.34


@responses.activate
def test_daily_nav_closed_market(client):
    responses.add(responses.GET, f"{BASE_URL}/FundDailyInfo/P1/dailynav/2026-06-14", status=204)
    assert FundDailyInfo(client).daily_nav("P1", "2026-06-14") is None
