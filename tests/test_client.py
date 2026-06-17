import pytest
import responses

from secopendata import NotSubscribedError, SECAPIError, SECClient
from secopendata.client import BASE_URL, RateLimiter


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
