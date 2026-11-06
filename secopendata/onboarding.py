"""Interactive, local-only SEC subscription-key setup."""
from __future__ import annotations

import getpass
import json
import os
import sys
import tempfile
import tomllib
import warnings
from pathlib import Path

from .config import env_var_name, keys_file_path
from .products import CATEGORIES, REGISTRY


class OnboardingError(RuntimeError):
    """An actionable setup failure that never includes a secret value."""


SCOPES = tuple(CATEGORIES) + tuple(REGISTRY)
ALIASES = {"debt": "bond", "provident-fund": "pvd"}


def _read_keys(*, for_write: bool = False) -> dict[str, str]:
    path = keys_file_path()
    if not path.exists():
        return {}
    try:
        with path.open("rb") as stream:
            data = tomllib.load(stream)
    except (OSError, ValueError):
        raise OnboardingError("Cannot read keys.toml; check its permissions and TOML syntax.") from None
    keys = data.get("keys", {})
    if not isinstance(keys, dict):
        raise OnboardingError("keys.toml must contain a [keys] table.")
    if for_write and (set(data) - {"keys"} or any(
        not isinstance(value, str) for value in keys.values()
    )):
        raise OnboardingError("keys.toml must contain only a [keys] table of string values.")
    return {str(name): str(value) for name, value in keys.items()}


def key_status(scope: str) -> dict:
    """Return credential presence and provenance, without returning a key."""
    source = None
    for name in (env_var_name(scope), "SEC_API_KEY"):
        if os.environ.get(name, "").strip():
            source = name
            break
    if source is None and _read_keys().get(scope, "").strip():
        source = "keys.toml"
    return {
        "scope": scope,
        "configured": source is not None,
        "source": source,
        "keys_file": str(keys_file_path()),
        "api_verified": False,
    }


def _check_destination(path: Path) -> None:
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise OnboardingError("Refusing to save through a symlink; choose a regular keys.toml path.")
    if path.exists() and not path.is_file():
        raise OnboardingError("The key-store destination must be a regular file.")


def _toml_string(value: str) -> str:
    # JSON escapes match TOML basic strings, except JSON permits a literal DEL.
    return json.dumps(value, ensure_ascii=False).replace("\x7f", "\\u007f")


def _save_key(scope: str, key: str) -> None:
    path = keys_file_path()
    _check_destination(path)
    keys = _read_keys(for_write=True)
    keys[scope] = key
    contents = "[keys]\n" + "".join(
        f"{_toml_string(name)} = {_toml_string(value)}\n"
        for name, value in keys.items()
    )
    temporary = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=".keys-", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            os.chmod(temporary, 0o600)
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        _check_destination(path)
        os.replace(temporary, path)
    except OSError:
        raise OnboardingError("Could not save keys.toml; check directory permissions.") from None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _require_terminal() -> None:
    if not sys.stdin.isatty():
        raise OnboardingError(
            "Hidden key entry requires your interactive terminal. "
            "Run `python -m secopendata onBording` there; "
            "do not paste a key into chat, command arguments, or a pipe."
        )


def run_onboarding(scope: str | None, *, status: bool = False, replace: bool = False) -> dict:
    try:
        if scope is None and not status:
            _require_terminal()
            print("SEC Open Data key scopes: " + ", ".join(SCOPES), file=sys.stderr)
            print("Choose the scope matching your subscription [fund]: ", end="", file=sys.stderr)
            scope = input().strip() or "fund"
            if scope not in SCOPES:
                raise OnboardingError("Unknown scope. Run `secopendata categories` to list scopes.")
        scope = ALIASES.get(scope, scope) if scope else "fund"
        current = key_status(scope)
        if status:
            return current
        if current["configured"] and not replace:
            return {**current, "saved": False}
        _require_terminal()
        _check_destination(keys_file_path())
        _read_keys(for_write=True)  # Validate before asking the user to enter a secret.
        print(
            "Get a subscription key for this scope from "
            "https://secopendata.sec.or.th/sec-open-apis\n"
            f"The key will be stored locally in {keys_file_path()}.",
            file=sys.stderr,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            key = getpass.getpass(prompt=f"Subscription key for {scope} (hidden): ", stream=sys.stderr).strip()
        if not key or any(ord(character) < 32 or ord(character) == 127 for character in key):
            raise OnboardingError("A nonempty, single-line subscription key is required.")
        try:
            key.encode("utf-8")
        except UnicodeEncodeError:
            raise OnboardingError("The subscription key contains invalid text.") from None
        _save_key(scope, key)
        result = key_status(scope)
        if result["source"] != "keys.toml":
            print(
                f"Warning: {result['source']} overrides the saved key. "
                "Unset that environment variable to use keys.toml.",
                file=sys.stderr,
            )
        print("Local configuration saved; API access has not been verified.", file=sys.stderr)
        return {**result, "saved": True}
    except (EOFError, KeyboardInterrupt):
        raise OnboardingError("Setup cancelled; no new key was saved.") from None
    except getpass.GetPassWarning:
        raise OnboardingError("Cannot hide terminal input; no key was saved.") from None
