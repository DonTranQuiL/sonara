"""Diagnostics for Sonara (Settings -> Devices & services -> Sonara -> Download diagnostics).

The session cookie is always redacted.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    ALL_VOICES,
    API_MODE_DIRECT,
    API_MODE_PROXY,
    CONF_API_MODE,
    CONF_SESSION_ID,
    DOMAIN,
    ENTITY_ID_DEVICE,
    ENTITY_ID_LANGUAGE,
    ENTITY_ID_MESSAGE,
    ENTITY_ID_SPEAK,
    ENTITY_ID_TTS_DIRECT,
    ENTITY_ID_TTS_PROXY,
    ENTITY_ID_VOICE,
    HASS_DATA_RANDOM_LANGS,
    SUPPORTED_LANGUAGES,
    VERSION,
)

TO_REDACT = {CONF_SESSION_ID}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return redacted diagnostics for a Sonara config entry."""
    mode = entry.data.get(CONF_API_MODE, API_MODE_PROXY)
    tts_entity = (
        ENTITY_ID_TTS_DIRECT if mode == API_MODE_DIRECT else ENTITY_ID_TTS_PROXY
    )

    entities: dict[str, Any] = {}
    for entity_id in (
        tts_entity,
        ENTITY_ID_LANGUAGE,
        ENTITY_ID_VOICE,
        ENTITY_ID_DEVICE,
        ENTITY_ID_MESSAGE,
        ENTITY_ID_SPEAK,
    ):
        state = hass.states.get(entity_id)
        if state is None:
            entities[entity_id] = None
            continue
        info: dict[str, Any] = {"state": state.state}
        if "code" in state.attributes:
            info["code"] = state.attributes["code"]
        entities[entity_id] = info
    # The message text is user content; only report whether it is set.
    message = entities.get(ENTITY_ID_MESSAGE)
    if message is not None:
        message["state"] = "set" if message["state"].strip() else "empty"

    return {
        "version": VERSION,
        "entry": {
            "title": entry.title,
            "state": str(entry.state),
            "data": async_redact_data(dict(entry.data), TO_REDACT),
        },
        "api_mode": mode,
        "loaded_entries": [
            e.data.get(CONF_API_MODE, API_MODE_PROXY)
            for e in hass.config_entries.async_entries(DOMAIN)
        ],
        "random_voice_languages": hass.data.get(DOMAIN, {}).get(
            HASS_DATA_RANDOM_LANGS, []
        ),
        "voices": len(ALL_VOICES),
        "language_groups": len(SUPPORTED_LANGUAGES),
        "entities": entities,
    }
