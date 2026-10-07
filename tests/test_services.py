"""Tests for the sonara.speak service."""

from __future__ import annotations

import pytest
from homeassistant.exceptions import ServiceValidationError
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_mock_service,
)

from custom_components.sonara.const import (
    API_MODE_DIRECT,
    CONF_API_MODE,
    DOMAIN,
    RANDOM_SEED_KEY,
    SERVICE_SPEAK,
)
from custom_components.sonara.services import build_speak_call, pick_tts_entity


async def test_speak_with_voice_override(hass, proxy_entry):
    calls = async_mock_service(hass, "tts", "speak")
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SPEAK,
        {
            "message": "  Dinner is ready.  ",
            "media_player_entity_id": "media_player.kitchen",
            "voice": "en_us_ghostface",
        },
        blocking=True,
    )
    assert len(calls) == 1
    call = calls[0]
    assert call.data["entity_id"] in ("tts.sonara_proxy", ["tts.sonara_proxy"])
    assert call.data["media_player_entity_id"] == ["media_player.kitchen"]
    assert call.data["message"] == "Dinner is ready."
    assert call.data["cache"] is True
    assert call.data["options"] == {"voice": "en_us_ghostface"}


async def test_speak_default_voice_sends_no_options(hass, proxy_entry):
    calls = async_mock_service(hass, "tts", "speak")
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SPEAK,
        {
            "message": "Hi",
            "media_player_entity_id": ["media_player.a", "media_player.b"],
        },
        blocking=True,
    )
    assert "options" not in calls[0].data
    assert calls[0].data["media_player_entity_id"] == [
        "media_player.a",
        "media_player.b",
    ]


async def test_speak_random_voice_disables_cache(hass, proxy_entry):
    calls = async_mock_service(hass, "tts", "speak")
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SPEAK,
        {
            "message": "Hi",
            "media_player_entity_id": "media_player.a",
            "voice": "random",
        },
        blocking=True,
    )
    options = calls[0].data["options"]
    assert options["voice"] == "random"
    assert options[RANDOM_SEED_KEY]
    assert calls[0].data["cache"] is False


async def test_speak_rejects_empty_message(hass, proxy_entry):
    async_mock_service(hass, "tts", "speak")
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SPEAK,
            {"message": "   ", "media_player_entity_id": "media_player.a"},
            blocking=True,
        )


async def test_speak_unknown_engine_connection(hass, proxy_entry):
    async_mock_service(hass, "tts", "speak")
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SPEAK,
            {
                "message": "Hi",
                "media_player_entity_id": "media_player.a",
                "engine": "direct",
            },
            blocking=True,
        )


async def test_pick_tts_entity_ignores_unloaded_entries(hass):
    MockConfigEntry(domain=DOMAIN, data={CONF_API_MODE: API_MODE_DIRECT}).add_to_hass(
        hass
    )
    assert pick_tts_entity(hass) is None


def test_build_speak_call_explicit_cache():
    data, target = build_speak_call(
        {
            "message": "x",
            "media_player_entity_id": ["media_player.a"],
            "voice": "random",
            "cache": True,
        },
        "tts.sonara_direct",
    )
    assert target == {"entity_id": "tts.sonara_direct"}
    assert data["cache"] is True
