"""Set up a proxy entry end to end and check the entities and service."""

from __future__ import annotations

import pytest
from homeassistant.config_entries import ConfigEntryState
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
    HASS_DATA_RANDOM_LANGS,
    SERVICE_SET_RANDOM_VOICES,
)


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


async def test_entities_created(hass, proxy_entry):
    assert proxy_entry.state is ConfigEntryState.LOADED
    for entity_id in (
        "tts.sonara_proxy",
        "select.sonara_language",
        "select.sonara_voice",
        "select.sonara_device",
        "text.sonara_message",
        "button.sonara_speak",
    ):
        assert hass.states.get(entity_id) is not None, entity_id
    assert hass.states.get("tts.sonara_proxy").attributes["friendly_name"] == (
        "Sonara Proxy"
    )


async def test_set_random_voices_filters_unknown(hass, proxy_entry):
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SET_RANDOM_VOICES,
        {"languages": ["en_us", "xx_bogus", "ja"]},
        blocking=True,
    )
    assert hass.data[DOMAIN][HASS_DATA_RANDOM_LANGS] == ["en_us", "ja"]


async def test_unload(hass, proxy_entry):
    assert await hass.config_entries.async_unload(proxy_entry.entry_id)
    await hass.async_block_till_done()
    assert proxy_entry.state is ConfigEntryState.NOT_LOADED
