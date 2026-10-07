"""Set up a proxy entry end to end and check the entities and service."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntryState

from custom_components.sonara.const import (
    DOMAIN,
    HASS_DATA_RANDOM_LANGS,
    SERVICE_SET_RANDOM_VOICES,
)


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
