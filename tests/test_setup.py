"""Set up a proxy entry end to end and check the entities and service."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntryState
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
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
    VERSION,
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


SONARA_ENTITIES = {
    "tts.sonara_proxy": ("Sonara Proxy", None),
    "select.sonara_language": ("Sonara Language", "config"),
    "select.sonara_voice": ("Sonara Voice", "config"),
    "select.sonara_device": ("Sonara Device", "config"),
    "text.sonara_message": ("Sonara Message", None),
    "button.sonara_speak": ("Sonara Speak", None),
}


async def test_one_device_with_all_entities(hass, proxy_entry):
    dev_reg = dr.async_get(hass)
    ent_reg = er.async_get(hass)

    devices = dr.async_entries_for_config_entry(dev_reg, proxy_entry.entry_id)
    assert len(devices) == 1
    device = devices[0]
    assert device.identifiers == {(DOMAIN, proxy_entry.entry_id)}
    assert device.name == "Sonara"
    assert device.manufacturer == "DonTranQuiL"
    assert device.model == "TikTok TTS (proxy)"
    assert device.sw_version == VERSION
    assert device.entry_type is dr.DeviceEntryType.SERVICE
    assert device.configuration_url == "https://github.com/DonTranQuiL/sonara"

    entities = er.async_entries_for_config_entry(ent_reg, proxy_entry.entry_id)
    assert {e.entity_id for e in entities} == set(SONARA_ENTITIES)
    for entry in entities:
        name, category = SONARA_ENTITIES[entry.entity_id]
        assert entry.device_id == device.id, entry.entity_id
        assert entry.has_entity_name is True
        assert (entry.entity_category.value if entry.entity_category else None) == (
            category
        ), entry.entity_id
        assert hass.states.get(entry.entity_id).attributes["friendly_name"] == name


async def test_unique_ids_unchanged(hass, proxy_entry):
    """Existing installs must keep their entities (no duplicates)."""
    ent_reg = er.async_get(hass)
    expected = {
        "select.sonara_language": "sonara_language",
        "select.sonara_voice": "sonara_voice",
        "select.sonara_device": "sonara_device",
        "text.sonara_message": "sonara_message",
        "button.sonara_speak": "sonara_speak",
        "tts.sonara_proxy": proxy_entry.entry_id,
    }
    for entity_id, unique_id in expected.items():
        assert ent_reg.async_get(entity_id).unique_id == unique_id


async def test_legacy_url_title_is_cleaned(hass, no_card_registration):
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
    assert entry.title == "Sonara (Proxy)"
    assert entry.state is ConfigEntryState.LOADED


async def test_custom_title_is_kept(hass, no_card_registration):
    assert await async_setup_component(hass, "http", {})
    hass.config.components.add("frontend")
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Kitchen voices",
        data={CONF_API_MODE: API_MODE_PROXY, CONF_ENDPOINT: DEFAULT_PROXY_ENDPOINT},
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.title == "Kitchen voices"
