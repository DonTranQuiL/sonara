"""Shared fixtures for Sonara tests."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sonara.const import (
    API_MODE_PROXY,
    CONF_API_MODE,
    CONF_ENDPOINT,
    CONF_VOICE,
    DEFAULT_PROXY_ENDPOINT,
    DEFAULT_VOICE,
    DOMAIN,
)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations automatically for all tests."""
    yield


@pytest.fixture
def skip_deps(hass):
    """Pretend the http/frontend dependencies are loaded.

    Sonara depends on ``frontend`` and ``http`` for its Lovelace card. Those
    pull in the full web stack, which the config-flow tests do not need.
    """
    hass.config.components.update({"http", "frontend"})
    yield


@pytest.fixture
def no_card_registration():
    """Skip the Lovelace card registration (needs a real HTTP server)."""
    with patch(
        "custom_components.sonara.JSModuleRegistration.async_register",
        return_value=None,
    ):
        yield


@pytest.fixture
async def proxy_entry(hass, no_card_registration):
    assert await async_setup_component(hass, "http", {})
    hass.config.components.add("frontend")
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=f"Sonara (proxy: {DEFAULT_PROXY_ENDPOINT})",
        data={
            CONF_API_MODE: API_MODE_PROXY,
            CONF_ENDPOINT: DEFAULT_PROXY_ENDPOINT,
            CONF_VOICE: DEFAULT_VOICE,
        },
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry
