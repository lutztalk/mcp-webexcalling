"""Tests for configuration resolution (env vars + .env precedence)."""

import pytest

from mcp_webexcalling import config


@pytest.fixture(autouse=True)
def _clear_cache():
    config.reset_settings_cache()
    yield
    config.reset_settings_cache()


def test_token_from_environment(monkeypatch):
    monkeypatch.setenv("WEBEX_ACCESS_TOKEN", "env-token")
    settings = config.get_settings()
    assert settings.webex_access_token == "env-token"


def test_missing_token_raises_value_error(monkeypatch, tmp_path):
    monkeypatch.delenv("WEBEX_ACCESS_TOKEN", raising=False)
    # Point at an empty dir so no real .env is picked up.
    monkeypatch.setattr(config, "find_env_file", lambda: str(tmp_path / ".env"))
    config.Settings.model_config["env_file"] = str(tmp_path / ".env")
    with pytest.raises(ValueError):
        config.get_settings()


def test_require_token_false_does_not_raise(monkeypatch, tmp_path):
    monkeypatch.delenv("WEBEX_ACCESS_TOKEN", raising=False)
    config.Settings.model_config["env_file"] = str(tmp_path / ".env")
    settings = config.get_settings(require_token=False)
    assert settings.webex_access_token == ""


def test_http_setting_defaults(monkeypatch):
    monkeypatch.setenv("WEBEX_ACCESS_TOKEN", "env-token")
    settings = config.get_settings()
    assert settings.webex_request_timeout == 30.0
    assert settings.webex_max_retries == 3
    assert settings.webex_base_url.startswith("https://")


def test_http_settings_overridable(monkeypatch):
    monkeypatch.setenv("WEBEX_ACCESS_TOKEN", "env-token")
    monkeypatch.setenv("WEBEX_MAX_RETRIES", "7")
    monkeypatch.setenv("WEBEX_REQUEST_TIMEOUT", "12.5")
    settings = config.get_settings()
    assert settings.webex_max_retries == 7
    assert settings.webex_request_timeout == 12.5
