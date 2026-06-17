import pytest

from secopendata import env_var_name, resolve_key
from secopendata.config import MissingKeyError


def test_env_var_name():
    assert env_var_name("FundFactsheet") == "SEC_FUNDFACTSHEET_KEY"
    assert env_var_name("Fund Daily Info") == "SEC_FUND_DAILY_INFO_KEY"


def test_explicit_wins(monkeypatch):
    monkeypatch.setenv("SEC_FUNDFACTSHEET_KEY", "fromenv")
    assert resolve_key("FundFactsheet", explicit="explicit") == "explicit"


def test_product_specific_env(monkeypatch):
    monkeypatch.setenv("SEC_FUNDFACTSHEET_KEY", " abc ")
    assert resolve_key("FundFactsheet") == "abc"


def test_shared_fallback(monkeypatch):
    monkeypatch.delenv("SEC_FUNDDAILYINFO_KEY", raising=False)
    monkeypatch.setenv("SEC_API_KEY", "shared")
    assert resolve_key("FundDailyInfo") == "shared"


def test_missing_key(monkeypatch, tmp_path):
    for var in ("SEC_FUNDFACTSHEET_KEY", "SEC_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("SECOPENDATA_KEYS_FILE", str(tmp_path / "none.toml"))
    with pytest.raises(MissingKeyError) as exc:
        resolve_key("FundFactsheet")
    assert "SEC_FUNDFACTSHEET_KEY" in str(exc.value)


def test_keys_file(monkeypatch, tmp_path):
    for var in ("SEC_FUNDFACTSHEET_KEY", "SEC_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    keyfile = tmp_path / "keys.toml"
    keyfile.write_text('[keys]\nFundFactsheet = "fromfile"\n')
    monkeypatch.setenv("SECOPENDATA_KEYS_FILE", str(keyfile))
    assert resolve_key("FundFactsheet") == "fromfile"
