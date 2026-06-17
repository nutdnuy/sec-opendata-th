"""Generic transport client for the Thai SEC OpenAPI (api.sec.or.th).

The SEC exposes several *products* (FundFactsheet, FundDailyInfo, ...), each
sitting behind Azure API Management and each requiring its own subscription key
sent in the ``Ocp-Apim-Subscription-Key`` header. This client deliberately
knows nothing about any product's data model: it performs authenticated,
rate-limited, retrying HTTP GETs against ``<base>/<product>/<path>`` and returns
parsed JSON. Product-specific helpers live in :mod:`secopendata.products`.
"""
from __future__ import annotations

import os
import threading
import time
from collections import deque
from typing import Any, Iterator, Mapping

import requests

from .config import resolve_key

# Gateway host. Overridable via env in case the SEC moves the gateway during the
# 2026 developer-portal migration (api-portal.sec.or.th -> secopendata.sec.or.th).
BASE_URL = os.environ.get("SEC_API_BASE_URL", "https://api.sec.or.th").rstrip("/")

# New portal limits (per the SEC Open API "Rate Limit" page):
#   - at most 5000 calls per 300 seconds
#   - keep at least 16 ms between consecutive requests
DEFAULT_CALLS = 5000
DEFAULT_PERIOD = 300.0
DEFAULT_MIN_INTERVAL = 0.016


class RateLimiter:
    """Sliding-window limiter plus a minimum gap between consecutive requests.

    Caps requests at ``calls`` in any ``period`` seconds, and additionally spaces
    consecutive requests at least ``min_interval`` seconds apart (the portal asks
    for >=16 ms between calls).
    """

    def __init__(
        self,
        calls: int = DEFAULT_CALLS,
        period: float = DEFAULT_PERIOD,
        min_interval: float = DEFAULT_MIN_INTERVAL,
    ):
        self.calls = calls
        self.period = period
        self.min_interval = min_interval
        self._hits: deque[float] = deque()
        self._last: float = 0.0
        self._lock = threading.Lock()

    def _evict(self, now: float) -> None:
        while self._hits and now - self._hits[0] >= self.period:
            self._hits.popleft()

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            self._evict(now)
            if len(self._hits) >= self.calls:
                sleep_for = self.period - (now - self._hits[0]) + 0.01
                if sleep_for > 0:
                    time.sleep(sleep_for)
                self._evict(time.monotonic())
            gap = self.min_interval - (time.monotonic() - self._last)
            if gap > 0:
                time.sleep(gap)
            stamp = time.monotonic()
            self._hits.append(stamp)
            self._last = stamp


class SECAPIError(RuntimeError):
    """A non-success HTTP response from the SEC API."""

    def __init__(self, status: int, url: str, body: str = ""):
        self.status = status
        self.url = url
        self.body = body
        suffix = f": {body}" if body else ""
        super().__init__(f"HTTP {status} from {url}{suffix}")


class NotSubscribedError(SECAPIError):
    """401/403 — the key is missing or not subscribed to this product."""


def _short(text: str, limit: int = 300) -> str:
    text = (text or "").strip().replace("\n", " ")
    return text[:limit]


def infer_key_scope(path: str) -> str:
    """Infer the subscription-key scope from an API path.

    Current SEC portal paths commonly look like ``/v1/one-report/...``. Legacy
    products look like ``/FundFactsheet/...``. The inferred scope maps to
    ``SEC_<SCOPE>_KEY`` via :func:`secopendata.config.env_var_name`.
    """
    clean = path.split("?", 1)[0].strip("/")
    parts = [part for part in clean.split("/") if part]
    if len(parts) >= 2 and parts[0].lower().startswith("v"):
        return parts[1]
    if parts:
        return parts[0]
    return "SEC"


class SECClient:
    """Authenticated, rate-limited HTTP client for SEC OpenAPI products."""

    def __init__(
        self,
        *,
        base_url: str = BASE_URL,
        calls: int = DEFAULT_CALLS,
        period: float = DEFAULT_PERIOD,
        timeout: int = 30,
        max_retries: int = 3,
        session: requests.Session | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._limiter = RateLimiter(calls, period)
        self._session = session or requests.Session()
        self._keys: dict[str, str] = {}

    # -- key handling ----------------------------------------------------
    def set_key(self, product: str, key: str) -> None:
        """Override the resolved key for a product (e.g. when passed explicitly)."""
        self._keys[product] = key.strip()

    def _key_for(self, product: str) -> str:
        if product not in self._keys:
            self._keys[product] = resolve_key(product)
        return self._keys[product]

    # -- requests --------------------------------------------------------
    def get(
        self,
        product: str,
        path: str = "",
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        """GET ``<base>/<product>/<path>`` and return parsed JSON (or ``None``).

        Returns ``None`` for HTTP 204 and for empty 200 bodies (common for funds
        with no data on a given day / closed market).
        """
        api_path = f"/{product.strip('/')}/{path.lstrip('/')}".rstrip("/")
        return self.request("GET", api_path, key_scope=product, params=params)

    def request(
        self,
        method: str,
        path: str,
        *,
        key_scope: str | None = None,
        params: Mapping[str, Any] | None = None,
        json_body: Any | None = None,
    ) -> Any:
        """Call any SEC OpenAPI path and return parsed JSON (or ``None``).

        Use this for the current portal's category paths such as
        ``/v1/one-report/fs/{report_year}/financial_statement/{unique_id}`` or
        POST endpoints under digital assets. ``key_scope`` controls which
        subscription key is resolved. If omitted it is inferred from the path.
        """
        scope = key_scope or infer_key_scope(path)
        key = self._key_for(scope)
        url = self._url_for(path)
        return self._request(method, url, key, params, json_body)

    def get_paginated(
        self,
        product: str,
        path: str = "",
        *,
        params: Mapping[str, Any] | None = None,
        page_param: str = "page",
        size_param: str = "limit",
        page_size: int = 100,
        start_page: int = 1,
        max_pages: int = 1000,
    ) -> Iterator[Any]:
        """Yield items across pages for products that support pagination.

        Works with either a bare JSON array response or an object wrapping the
        rows under ``data``/``items``/``result``. Stops when a page is empty or
        shorter than ``page_size``. Param names are configurable because the SEC
        portal is not fully consistent across products.
        """
        query = dict(params or {})
        page = start_page
        for _ in range(max_pages):
            query[page_param] = page
            query[size_param] = page_size
            data = self.get(product, path, params=query)
            if data is None:
                return
            if isinstance(data, list):
                items = data
            elif isinstance(data, Mapping):
                items = (
                    data.get("data")
                    or data.get("items")
                    or data.get("result")
                    or []
                )
                if not isinstance(items, list):
                    yield data
                    return
            else:
                yield data
                return
            for item in items:
                yield item
            if len(items) < page_size:
                return
            page += 1

    # -- internals -------------------------------------------------------
    def _url_for(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            if not path.startswith(self.base_url + "/"):
                raise ValueError(f"Refusing non-SEC API URL: {path}")
            return path
        return f"{self.base_url}/{path.lstrip('/')}".rstrip("/")

    def _request(
        self,
        method: str,
        url: str,
        key: str,
        params: Mapping[str, Any] | None,
        json_body: Any | None = None,
    ) -> Any:
        attempt = 0
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }
        verb = method.upper()
        while True:
            self._limiter.acquire()
            resp = self._session.request(
                verb,
                url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=self.timeout,
            )
            status = resp.status_code
            if status == 200:
                if not resp.content:
                    return None
                try:
                    return resp.json()
                except ValueError:
                    return resp.text
            if status == 204:
                return None
            if status in (401, 403):
                raise NotSubscribedError(status, url, _short(resp.text))
            # 421 is the SEC gateway's throttle response; 429 kept for safety.
            if status in (421, 429) or 500 <= status < 600:
                attempt += 1
                if attempt > self.max_retries:
                    raise SECAPIError(status, url, _short(resp.text))
                time.sleep(self._backoff(resp, attempt))
                continue
            raise SECAPIError(status, url, _short(resp.text))

    @staticmethod
    def _backoff(resp: requests.Response, attempt: int) -> float:
        retry_after = resp.headers.get("Retry-After")
        if retry_after:
            try:
                return max(float(retry_after), 0.0)
            except ValueError:
                pass
        return float(min(2 ** attempt, 30))
