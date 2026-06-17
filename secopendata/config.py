"""Subscription-key resolution for SEC OpenAPI products.

Each product on api.sec.or.th (FundFactsheet, FundDailyInfo, ...) has its own
Azure API Management subscription key. Keys are resolved in this order:

  1. An explicit value passed in code.
  2. Environment variable ``SEC_<PRODUCT>_KEY`` (product upper-cased,
     non-alphanumeric runs collapsed to ``_``). e.g. ``SEC_FUNDFACTSHEET_KEY``.
  3. Environment variable ``SEC_API_KEY`` (shared fallback for all products).
  4. ``~/.config/secopendata/keys.toml`` — a ``[keys]`` table mapping the exact
     product name to its key.

Nothing is ever hard-coded or committed.
"""
from __future__ import annotations

import os
import re
import tomllib
from pathlib import Path


def keys_file_path() -> Path:
    """Location of the optional TOML key store (override with ``SECOPENDATA_KEYS_FILE``)."""
    override = os.environ.get("SECOPENDATA_KEYS_FILE")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".config" / "secopendata" / "keys.toml"


def env_var_name(product: str) -> str:
    """Map a product name to its conventional environment variable name."""
    slug = re.sub(r"[^A-Za-z0-9]+", "_", product).strip("_").upper()
    return f"SEC_{slug}_KEY"


def _file_keys() -> dict[str, str]:
    path = keys_file_path()
    if not path.is_file():
        return {}
    with open(path, "rb") as fh:
        data = tomllib.load(fh)
    table = data.get("keys", {})
    return {str(k): str(v) for k, v in table.items()}


class MissingKeyError(RuntimeError):
    """Raised when no subscription key can be found for a product."""

    def __init__(self, product: str):
        self.product = product
        self.env_name = env_var_name(product)
        super().__init__(
            f"No subscription key for product '{product}'. Set "
            f"${self.env_name} (or $SEC_API_KEY), or add it under [keys] in "
            f"{keys_file_path()}."
        )


def resolve_key(product: str, explicit: str | None = None) -> str:
    """Return the subscription key for ``product`` or raise ``MissingKeyError``."""
    if explicit and explicit.strip():
        return explicit.strip()

    specific = os.environ.get(env_var_name(product))
    if specific and specific.strip():
        return specific.strip()

    shared = os.environ.get("SEC_API_KEY")
    if shared and shared.strip():
        return shared.strip()

    file_keys = _file_keys()
    if product in file_keys and file_keys[product].strip():
        return file_keys[product].strip()

    raise MissingKeyError(product)
