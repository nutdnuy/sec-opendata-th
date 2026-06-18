import pytest
import responses

from secopendata import NotSubscribedError, SECAPIError, SECClient
from secopendata.client import BASE_URL, RateLimiter, infer_key_scope


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SEC_API_KEY", "test-key")
    # Tight retry budget so the 429/5xx tests stay fast.
    return SECClient(max_retries=2)


@responses.activate
def test_get_200_json(client):
    responses.add(responses.GET, f"{BASE_URL}/FundFactsheet/fund/amc",
                  json=[{"unique_id": "C1", "name_en": "ACME"}], status=200)
    out = client.get("FundFactsheet", "fund/amc")
    assert out[0]["unique_id"] == "C1"
    assert responses.calls[0].request.headers["Ocp-Apim-Subscription-Key"] == "test-key"
    assert responses.calls[0].request.headers["Cache-Control"] == "no-cache"


def test_infer_key_scope():
    assert infer_key_scope("/v1/one-report/fs/2021") == "one-report"
    assert infer_key_scope("v1/digital-asset/operators") == "digital-asset"
    assert infer_key_scope("/FundFactsheet/fund/amc") == "FundFactsheet"


@responses.activate
def test_request_current_portal_path_get(client, monkeypatch):
    monkeypatch.setenv("SEC_ONE_REPORT_KEY", "one-report-key")
    url = f"{BASE_URL}/v1/one-report/fs/2021/financial_statement/C0000000013"
    responses.add(responses.GET, url, json={"symbol": "TEST"}, status=200)
    out = client.request("GET", "/v1/one-report/fs/2021/financial_statement/C0000000013")
    assert out == {"symbol": "TEST"}
    assert responses.calls[0].request.headers["Ocp-Apim-Subscription-Key"] == "one-report-key"


@responses.activate
def test_request_current_portal_path_post(client, monkeypatch):
    monkeypatch.setenv("SEC_DIGITAL_ASSET_KEY", "digital-key")
    url = f"{BASE_URL}/v1/digital-asset/profile/intermediary"
    responses.add(responses.POST, url, json=[{"name": "operator"}], status=200)
    out = client.request(
        "POST",
        "/v1/digital-asset/profile/intermediary",
        json_body={"IntermediaryName": ""},
    )
    assert out == [{"name": "operator"}]
    assert responses.calls[0].request.body == b'{"IntermediaryName": ""}'


@responses.activate
def test_request_cursor_paginated_v2(client, monkeypatch):
    monkeypatch.setenv("SEC_FUND_KEY", "fund-key")
    url = f"{BASE_URL}/v2/fund/factsheet/performance"
    responses.add(
        responses.GET,
        url,
        json={"message": "success", "page_size": 2, "next_cursor": "abc", "items": [{"proj_id": "A"}]},
        status=200,
    )
    responses.add(
        responses.GET,
        url,
        json={"message": "success", "page_size": 2, "next_cursor": "", "items": [{"proj_id": "B"}]},
        status=200,
    )
    items = list(client.request_cursor_paginated("/v2/fund/factsheet/performance", page_size=2))
    assert items == [{"proj_id": "A"}, {"proj_id": "B"}]
    assert "page_size=2" in responses.calls[0].request.url
    assert "next_cursor=abc" in responses.calls[1].request.url


@responses.activate
def test_get_204_returns_none(client):
    responses.add(responses.GET, f"{BASE_URL}/FundDailyInfo/X/dailynav/2026-01-01", status=204)
    assert client.get("FundDailyInfo", "X/dailynav/2026-01-01") is None


@responses.activate
def test_get_empty_200_returns_none(client):
    responses.add(responses.GET, f"{BASE_URL}/FundFactsheet/x", body="", status=200)
    assert client.get("FundFactsheet", "x") is None


@responses.activate
def test_401_raises_not_subscribed(client):
    responses.add(responses.GET, f"{BASE_URL}/FundFactsheet/y", status=401, body="nope")
    with pytest.raises(NotSubscribedError) as exc:
        client.get("FundFactsheet", "y")
    assert exc.value.status == 401


@responses.activate
def test_429_then_success(client, monkeypatch):
    monkeypatch.setattr("secopendata.client.time.sleep", lambda *_: None)
    url = f"{BASE_URL}/FundFactsheet/z"
    responses.add(responses.GET, url, status=429, headers={"Retry-After": "0"})
    responses.add(responses.GET, url, json={"ok": True}, status=200)
    assert client.get("FundFactsheet", "z") == {"ok": True}


@responses.activate
def test_421_then_success(client, monkeypatch):
    monkeypatch.setattr("secopendata.client.time.sleep", lambda *_: None)
    url = f"{BASE_URL}/FundFactsheet/throttled"
    responses.add(responses.GET, url, status=421, headers={"Retry-After": "0"})
    responses.add(responses.GET, url, json={"ok": True}, status=200)
    assert client.get("FundFactsheet", "throttled") == {"ok": True}


@responses.activate
def test_500_exhausts_retries(client, monkeypatch):
    monkeypatch.setattr("secopendata.client.time.sleep", lambda *_: None)
    url = f"{BASE_URL}/FundFactsheet/boom"
    for _ in range(5):
        responses.add(responses.GET, url, status=500, body="server")
    with pytest.raises(SECAPIError) as exc:
        client.get("FundFactsheet", "boom")
    assert exc.value.status == 500


@responses.activate
def test_pagination(client):
    url = f"{BASE_URL}/SomeProduct/list"
    responses.add(responses.GET, url, json=[1, 2], status=200)  # full page
    responses.add(responses.GET, url, json=[3], status=200)     # short -> stop
    items = list(client.get_paginated("SomeProduct", "list", page_size=2))
    assert items == [1, 2, 3]


def test_rate_limiter_allows_burst_under_limit():
    rl = RateLimiter(calls=3, period=100)
    for _ in range(3):
        rl.acquire()  # should not block
    assert len(rl._hits) == 3


def test_client_accepts_custom_min_interval(monkeypatch):
    monkeypatch.setenv("SEC_API_KEY", "test-key")
    client = SECClient(min_interval=0.123)
    assert client._limiter.min_interval == 0.123
