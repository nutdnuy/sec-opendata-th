"""Python client for the Thai SEC OpenAPI (api.sec.or.th)."""
from __future__ import annotations

from .client import (
    BASE_URL,
    infer_key_scope,
    NotSubscribedError,
    RateLimiter,
    SECAPIError,
    SECClient,
)
from .config import MissingKeyError, env_var_name, resolve_key
from .products import (
    REGISTRY,
    CATEGORIES,
    FundDailyInfo,
    FundFactsheet,
    Product,
    register_product,
)

__version__ = "0.1.0"

__all__ = [
    "BASE_URL",
    "infer_key_scope",
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
    "CATEGORIES",
    "register_product",
    "__version__",
]
