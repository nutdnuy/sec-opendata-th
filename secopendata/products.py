"""High-level helpers for known SEC OpenAPI products, plus a registry so new
products can be added in one line as you discover them on the developer portal.

Only two products are publicly documented today (FundFactsheet, FundDailyInfo).
Any other product is still usable immediately via ``SECClient.get(product, path)``
or by calling :func:`register_product` and writing a thin helper like the ones
below — this is what keeps the client open to "all api.sec.or.th products".
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator

from .client import SECAPIError, SECClient


@dataclass
class Product:
    name: str  # exact path segment / product id, e.g. "FundFactsheet"
    title: str = ""
    description: str = ""


@dataclass(frozen=True)
class Category:
    key_scope: str
    title: str
    description: str = ""


REGISTRY: dict[str, Product] = {}
CATEGORIES: dict[str, Category] = {}


def register_product(name: str, title: str = "", description: str = "") -> Product:
    """Register a product so tooling can list it; returns the Product."""
    product = Product(name=name, title=title or name, description=description)
    REGISTRY[name] = product
    return product


def register_category(key_scope: str, title: str, description: str = "") -> Category:
    """Register a current SEC Open Data portal category/key scope."""
    category = Category(key_scope=key_scope, title=title, description=description)
    CATEGORIES[key_scope] = category
    return category


FUND_FACTSHEET = register_product(
    "FundFactsheet",
    "Fund Factsheet",
    "AMC list, fund universe per AMC, policy, top holdings, share classes.",
)
FUND_DAILY_INFO = register_product(
    "FundDailyInfo",
    "Fund Daily Info",
    "Daily NAV history per fund / share class.",
)

register_category("digital-asset", "สินทรัพย์ดิจิทัล", "Digital asset business and market data.")
register_category("fund", "กองทุน", "Mutual fund and fund-related SEC Open Data endpoints.")
register_category("license-check", "Licence Check", "License and regulated-person checks.")
register_category("one-report", "One Report", "Listed-company One Report, financial statements, directors, executives, and governance data.")
register_category("provident-fund", "กองทุนสำรองเลี้ยงชีพ", "Provident fund data.")
register_category("debt", "ตราสารหนี้", "Debt instrument data.")
register_category("equity", "ตราสารทุน", "Equity and listed-company data.")
register_category("esg", "ESG", "ESG-related datasets.")
register_category(
    "capital-market-professional",
    "ผู้ประกอบธุรกิจและบุคลากรในตลาดทุน",
    "Capital-market business operators and professionals.",
)
register_category("investor", "ผู้ลงทุน", "Investor-related datasets.")


def _name_of(record: dict) -> str:
    for field in ("name_en", "name_th", "amc_name", "name"):
        value = record.get(field)
        if value:
            return str(value)
    return ""


def _id_of(record: dict) -> str:
    for field in ("unique_id", "amc_id", "id"):
        value = record.get(field)
        if value:
            return str(value)
    return ""


class FundFactsheet:
    """Helpers over the FundFactsheet product."""

    PRODUCT = "FundFactsheet"

    def __init__(self, client: SECClient | None = None):
        self.client = client or SECClient()

    def amc_list(self) -> list[dict]:
        return self.client.get(self.PRODUCT, "fund/amc") or []

    def funds_by_amc(self, unique_id: str) -> list[dict]:
        return self.client.get(self.PRODUCT, f"fund/amc/{unique_id}") or []

    def policy(self, proj_id: str) -> Any:
        return self.client.get(self.PRODUCT, f"fund/{proj_id}/policy")

    def top5(self, proj_id: str, period: str) -> list[dict]:
        return self.client.get(self.PRODUCT, f"fund/{proj_id}/FundTop5/{period}") or []

    def classes(self, proj_id: str) -> list[dict]:
        """Share classes; some single-class funds return 404 — treat as empty."""
        try:
            return self.client.get(self.PRODUCT, f"fund/{proj_id}/class") or []
        except SECAPIError as exc:
            if exc.status == 404:
                return []
            raise

    def find_amc(self, query: str) -> list[dict]:
        """Return AMCs whose name contains ``query`` (case-insensitive) or whose
        id matches exactly. Useful so callers can pass 'KASIKORN' instead of an id."""
        needle = query.strip().lower()
        out = []
        for amc in self.amc_list():
            if needle == _id_of(amc).lower() or needle in _name_of(amc).lower():
                out.append(amc)
        return out

    def resolve_amc_id(self, query: str) -> str | None:
        """Best-effort: turn an AMC name or id into a unique_id."""
        matches = self.find_amc(query)
        if not matches:
            return None
        return _id_of(matches[0]) or None


class FundDailyInfo:
    """Helpers over the FundDailyInfo product."""

    PRODUCT = "FundDailyInfo"

    def __init__(self, client: SECClient | None = None):
        self.client = client or SECClient()

    def daily_nav(self, proj_id: str, nav_date: str) -> Any:
        """NAV record(s) for one fund on one date (YYYY-MM-DD).

        Returns a list of per-class rows, or ``None`` when the market was closed
        / there is no data for that date.
        """
        return self.client.get(self.PRODUCT, f"{proj_id}/dailynav/{nav_date}")
