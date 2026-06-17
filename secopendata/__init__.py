"""Python client for the Thai SEC OpenAPI (api.sec.or.th)."""
from __future__ import annotations

from .client import (
    BASE_URL,
    NotSubscribedError,
    RateLimiter,
    SECAPIError,
    SECClient,
)
from .config import MissingKeyError, env_var_name, resolve_key
from .products import (
    REGISTRY,
    FundDailyInfo,
    FundFactsheet,
    Product,
    register_product,
)

__version__ = "0.1.0"

__all__ = [
    "BASE_URL",
    "SECClient",
    "RateLimiter",
    "SECAPIError",
    "NotSubscribedError",
    "MissingKeyError",
    "resolve_key",
    "env_var_name",
    "FundFactsheet",
    "FundDailyInfo",
    "Product",
    "REGISTRY",
    "register_product",
    "__version__",
]
