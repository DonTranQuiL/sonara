"""Tests for config entry diagnostics."""

from __future__ import annotations

from homeassistant.components.diagnostics import REDACTED
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sonara.const import (
    API_MODE_DIRECT,
    CONF_API_MODE,
    CONF_ENDPOINT,
    CONF_SESSION_ID,
    CONF_VOICE,
    DIRECT_API_ENDPOINTS,
    DOMAIN,
    VERSION,
)
from custom_components.sonara.diagnostics import async_get_config_entry_diagnostics


async def test_diagnostics_redacts_session(hass):
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Sonara (direct API)",
        data={
            CONF_API_MODE: API_MODE_DIRECT,
            CONF_ENDPOINT: DIRECT_API_ENDPOINTS[0],
            CONF_SESSION_ID: "super-secret-cookie",
            CONF_VOICE: "en_us_001",
        },
    )
    entry.add_to_hass(hass)
    diag = await async_get_config_entry_diagnostics(hass, entry)
    assert diag["entry"]["data"][CONF_SESSION_ID] == REDACTED
    assert "super-secret-cookie" not in str(diag)
    assert diag["api_mode"] == API_MODE_DIRECT
    assert diag["version"] == VERSION
    assert diag["entities"]["tts.sonara_direct"] is None


async def test_diagnostics_loaded_proxy(hass, proxy_entry):
    hass.states.async_set("text.sonara_message", "private words")
    diag = await async_get_config_entry_diagnostics(hass, proxy_entry)
    assert diag["entities"]["tts.sonara_proxy"] is not None
    assert diag["entities"]["text.sonara_message"]["state"] == "set"
    assert "private words" not in str(diag)
    assert diag["voices"] == 106
