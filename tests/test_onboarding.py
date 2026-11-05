import json
import os
import stat
import sys

import pytest

from secopendata.cli import main
from secopendata.config import resolve_key


@pytest.fixture(autouse=True)
def isolated_keys(monkeypatch, tmp_path):
    for name in os.environ:
        if name.startswith("SEC_") and name.endswith("_KEY"):
            monkeypatch.delenv(name)
    path = tmp_path / "config" / "keys.toml"
    monkeypatch.setenv("SECOPENDATA_KEYS_FILE", str(path))
    def no_network(*args, **kwargs):
        pytest.fail("Onboarding must not make network requests")
    monkeypatch.setattr("requests.Session.request", no_network)
    return path


def test_status_without_key_is_safe_and_does_not_write(isolated_keys, capsys):
    assert main(["onboarding", "--status", "--scope", "fund"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["configured"] is False
    assert result["source"] is None
    assert result["api_verified"] is False
    assert not isolated_keys.exists()


def test_onbording_saves_hidden_key_and_preserves_other_scope(monkeypatch, isolated_keys, capsys):
    isolated_keys.parent.mkdir()
    isolated_keys.write_text('[keys]\nbond = "existing-bond"\n')
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("getpass.getpass", lambda **kwargs: "new-fund-secret")
    assert main(["onBording", "--scope", "fund"]) == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["configured"] is True
    assert result["source"] == "keys.toml"
    assert result["saved"] is True
    assert resolve_key("fund") == "new-fund-secret"
    assert resolve_key("bond") == "existing-bond"
    assert stat.S_IMODE(isolated_keys.stat().st_mode) == 0o600
    assert "new-fund-secret" not in captured.out + captured.err
    assert "existing-bond" not in captured.out + captured.err


@pytest.mark.parametrize("variable", ["SEC_FUND_KEY", "SEC_API_KEY"])
def test_existing_environment_key_is_reused_without_prompt(monkeypatch, isolated_keys, capsys, variable):
    monkeypatch.setenv(variable, "environment-secret")
    assert main(["onboarding", "--scope", "fund"]) == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["source"] == variable
    assert result["saved"] is False
    assert not isolated_keys.exists()
    assert "environment-secret" not in captured.out + captured.err


def test_specific_environment_precedes_shared_and_file(monkeypatch, isolated_keys, capsys):
    isolated_keys.parent.mkdir()
    isolated_keys.write_text('[keys]\nfund = "file-secret"\n')
    monkeypatch.setenv("SEC_API_KEY", "shared-secret")
    monkeypatch.setenv("SEC_FUND_KEY", "specific-secret")
    assert main(["onboarding", "--scope", "fund", "--status"]) == 0
    assert json.loads(capsys.readouterr().out)["source"] == "SEC_FUND_KEY"


def test_existing_file_key_is_reused_without_prompt(monkeypatch, isolated_keys, capsys):
    isolated_keys.parent.mkdir()
    original = '[keys]\nfund = "existing-fund"\n'
    isolated_keys.write_text(original)
    assert main(["onboarding", "--scope", "fund"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["source"] == "keys.toml"
    assert result["saved"] is False
    assert isolated_keys.read_text() == original


@pytest.mark.parametrize("mode", [[], ["--status"]])
def test_existing_key_with_metadata_is_reused_without_altering_file(isolated_keys, capsys, mode):
    isolated_keys.parent.mkdir()
    original = b'# Retain user metadata and formatting.\n[keys]\nfund = "existing-fund"\n\n[metadata]\nlabel = "personal"\n'
    isolated_keys.write_bytes(original)
    assert resolve_key("fund") == "existing-fund"
    assert main(["onboarding", "--scope", "fund", *mode]) == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["configured"] is True
    assert result["source"] == "keys.toml"
    assert isolated_keys.read_bytes() == original
    assert "existing-fund" not in captured.out + captured.err


def test_replace_preserves_file_with_metadata_without_prompting(monkeypatch, isolated_keys, capsys):
    isolated_keys.parent.mkdir()
    original = b'[keys]\nfund = "existing-fund"\n[metadata]\nlabel = "personal"\n'
    isolated_keys.write_bytes(original)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    def unexpected_prompt(**kwargs):
        pytest.fail("Unsupported file format must be rejected before hidden input")
    monkeypatch.setattr("getpass.getpass", unexpected_prompt)
    assert main(["onboarding", "--scope", "fund", "--replace"]) == 2
    assert "only a [keys] table" in capsys.readouterr().err
    assert isolated_keys.read_bytes() == original


def test_replace_saves_key_and_reports_environment_override(monkeypatch, isolated_keys, capsys):
    monkeypatch.setenv("SEC_FUND_KEY", "environment-secret")
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("getpass.getpass", lambda **kwargs: "replacement-secret")
    assert main(["onboarding", "--scope", "fund", "--replace"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["source"] == "SEC_FUND_KEY"
    assert "SEC_FUND_KEY overrides" in captured.err
    assert "replacement-secret" not in captured.out + captured.err
    assert resolve_key("fund") == "environment-secret"
    monkeypatch.delenv("SEC_FUND_KEY")
    assert resolve_key("fund") == "replacement-secret"


@pytest.mark.parametrize("chosen,expected", [("", "fund"), ("debt", "bond"), ("provident-fund", "pvd"), ("FundDailyInfo", "FundDailyInfo")])
def test_interactive_scope_selection(monkeypatch, isolated_keys, capsys, chosen, expected):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda: chosen)
    monkeypatch.setattr("getpass.getpass", lambda **kwargs: "scope-secret")
    assert main(["onBording"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["scope"] == expected
    assert resolve_key(expected) == "scope-secret"


def test_noninteractive_entry_fails_without_reading_pipe(monkeypatch, isolated_keys, capsys):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    assert main(["onboarding", "--scope", "fund"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "interactive terminal" in captured.err
    assert not isolated_keys.exists()


@pytest.mark.parametrize("contents", ['[keys]\nfund = "unclosed-secret', '[keys]\nfund = 123', '[other]\nvalue = "unrelated-secret"'])
def test_invalid_file_is_not_overwritten_or_exposed(monkeypatch, isolated_keys, capsys, contents):
    isolated_keys.parent.mkdir()
    isolated_keys.write_text(contents)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    assert main(["onboarding", "--scope", "fund", "--replace"]) == 2
    captured = capsys.readouterr()
    assert isolated_keys.read_text() == contents
    assert "unclosed-secret" not in captured.err
    assert "unrelated-secret" not in captured.err
    assert captured.out == ""


def test_symlink_keyfile_is_not_overwritten(monkeypatch, isolated_keys, tmp_path, capsys):
    target = tmp_path / "original.toml"
    original = '[keys]\nfund = "existing-secret"\n'
    target.write_text(original)
    isolated_keys.parent.mkdir()
    isolated_keys.symlink_to(target)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    assert main(["onboarding", "--scope", "fund", "--replace"]) == 2
    assert "symlink" in capsys.readouterr().err
    assert isolated_keys.is_symlink()
    assert target.read_text() == original


@pytest.mark.parametrize("key", ["", "  ", "invalid\nsecret", "invalid\x00secret"])
def test_invalid_secret_is_rejected_without_saving(monkeypatch, isolated_keys, capsys, key):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("getpass.getpass", lambda **kwargs: key)
    assert main(["onboarding", "--scope", "fund"]) == 2
    assert not isolated_keys.exists()
    captured = capsys.readouterr()
    if key.strip():
        assert key not in captured.out + captured.err


@pytest.mark.parametrize("failure", [EOFError, KeyboardInterrupt])
def test_cancelled_entry_preserves_existing_keys(monkeypatch, isolated_keys, capsys, failure):
    isolated_keys.parent.mkdir()
    original = '[keys]\nfund = "existing-secret"\n'
    isolated_keys.write_text(original)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    def cancel(**kwargs):
        raise failure
    monkeypatch.setattr("getpass.getpass", cancel)
    assert main(["onboarding", "--scope", "fund", "--replace"]) == 2
    assert "cancelled" in capsys.readouterr().err
    assert isolated_keys.read_text() == original


def test_hidden_input_unavailable_does_not_fall_back(monkeypatch, isolated_keys, capsys):
    import getpass
    import warnings

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    def warn(**kwargs):
        warnings.warn("echo unavailable", getpass.GetPassWarning)
        pytest.fail("Should stop before an echoing fallback can read a key")
    monkeypatch.setattr(getpass, "getpass", warn)
    assert main(["onboarding", "--scope", "fund"]) == 2
    assert "Cannot hide" in capsys.readouterr().err
    assert not isolated_keys.exists()


def test_failed_save_preserves_existing_keys_and_removes_temporary(monkeypatch, isolated_keys, capsys):
    isolated_keys.parent.mkdir()
    original = '[keys]\nfund = "existing-secret"\n'
    isolated_keys.write_text(original)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("getpass.getpass", lambda **kwargs: "replacement-secret")
    def fail(*args):
        raise PermissionError("simulated write failure")
    monkeypatch.setattr(os, "replace", fail)
    assert main(["onboarding", "--scope", "fund", "--replace"]) == 2
    assert "Could not save" in capsys.readouterr().err
    assert isolated_keys.read_text() == original
    assert list(isolated_keys.parent.iterdir()) == [isolated_keys]


def test_existing_toml_strings_roundtrip_when_adding_scope(monkeypatch, isolated_keys, capsys):
    isolated_keys.parent.mkdir()
    isolated_keys.write_text('[keys]\nbond = "quoted \\"value\\" 😀 \\u007f"\n')
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("getpass.getpass", lambda **kwargs: "new-fund-secret")
    assert main(["onboarding", "--scope", "fund"]) == 0
    assert resolve_key("bond") == 'quoted "value" 😀 \x7f'
