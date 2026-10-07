"""The sonara.speak service.

A one-call shortcut around tts.speak:

  action: sonara.speak
  data:
    message: "Dinner is ready"
    media_player_entity_id: media_player.kitchen
    voice: en_us_ghostface     # optional, per-call voice override
    engine: proxy              # optional: proxy | direct (default: proxy first)

It picks the Sonara TTS entity for you (proxy preferred over direct, the same
rule the Speak button uses), handles the "random" voice the same way the
button does (fresh voice every call, no cache), and then calls tts.speak.
Nothing about the TTS engine itself changes.
"""

from __future__ import annotations

from uuid import uuid4

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError

from .const import (
    API_MODE_DIRECT,
    API_MODE_PROXY,
    ATTR_CACHE,
    ATTR_ENGINE,
    ATTR_MEDIA_PLAYER,
    ATTR_MESSAGE,
    ATTR_VOICE,
    CONF_API_MODE,
    DOMAIN,
    ENTITY_ID_TTS_DIRECT,
    ENTITY_ID_TTS_PROXY,
    LOGGER,
    RANDOM_SEED_KEY,
    RANDOM_VOICE_CODE,
    SERVICE_SPEAK,
    TTS_SERVICE_DOMAIN,
    TTS_SERVICE_FIELD_CACHE,
    TTS_SERVICE_FIELD_MESSAGE,
    TTS_SERVICE_FIELD_OPTIONS,
    TTS_SERVICE_FIELD_PLAYER,
    TTS_SERVICE_FIELD_VOICE,
    TTS_SERVICE_SPEAK,
)

SPEAK_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Required(ATTR_MEDIA_PLAYER): cv.entity_ids,
        vol.Optional(ATTR_VOICE): cv.string,
        vol.Optional(ATTR_ENGINE): vol.In([API_MODE_PROXY, API_MODE_DIRECT]),
        vol.Optional(ATTR_CACHE): cv.boolean,
    }
)


def pick_tts_entity(hass: HomeAssistant, engine: str | None = None) -> str | None:
    """Return the Sonara TTS entity to use, or None when none is loaded.

    With no engine given, proxy is preferred over direct (same as the Speak
    button). Only LOADED config entries count, so a removed entry is never used.
    """
    loaded_modes = {
        entry.data.get(CONF_API_MODE, API_MODE_PROXY)
        for entry in hass.config_entries.async_entries(DOMAIN)
        if entry.state is ConfigEntryState.LOADED
    }
    order = [engine] if engine else [API_MODE_PROXY, API_MODE_DIRECT]
    for mode in order:
        if mode in loaded_modes:
            return (
                ENTITY_ID_TTS_DIRECT if mode == API_MODE_DIRECT else ENTITY_ID_TTS_PROXY
            )
    return None


def build_speak_call(data: dict, tts_entity: str) -> tuple[dict, dict]:
    """Translate sonara.speak data into (service_data, target) for tts.speak."""
    message = data[ATTR_MESSAGE].strip()
    voice = (data.get(ATTR_VOICE) or "").strip()
    is_random = voice == RANDOM_VOICE_CODE

    options: dict[str, str] = {}
    if voice:
        options[TTS_SERVICE_FIELD_VOICE] = voice
    if is_random:
        # Same trick as the Speak button: a unique seed forces a cache miss so
        # every call really gets a new random voice.
        options[RANDOM_SEED_KEY] = str(uuid4())

    service_data = {
        TTS_SERVICE_FIELD_PLAYER: data[ATTR_MEDIA_PLAYER],
        TTS_SERVICE_FIELD_MESSAGE: message,
        TTS_SERVICE_FIELD_CACHE: data.get(ATTR_CACHE, not is_random),
    }
    if options:
        service_data[TTS_SERVICE_FIELD_OPTIONS] = options
    return service_data, {"entity_id": tts_entity}


def async_register_speak_service(hass: HomeAssistant) -> None:
    """Register sonara.speak (idempotent)."""
    if hass.services.has_service(DOMAIN, SERVICE_SPEAK):
        return

    async def _handle_speak(call: ServiceCall) -> None:
        if not call.data[ATTR_MESSAGE].strip():
            raise ServiceValidationError("Sonara: the message is empty.")
        engine = call.data.get(ATTR_ENGINE)
        tts_entity = pick_tts_entity(hass, engine)
        if tts_entity is None:
            raise ServiceValidationError(
                f"Sonara: no loaded {engine or 'Sonara'} connection to speak with. "
                "Add or enable the integration first."
            )
        service_data, target = build_speak_call(dict(call.data), tts_entity)
        LOGGER.debug(
            "sonara.speak: entity=%s players=%s voice=%s",
            tts_entity,
            service_data[TTS_SERVICE_FIELD_PLAYER],
            call.data.get(ATTR_VOICE, "(default)"),
        )
        await hass.services.async_call(
            TTS_SERVICE_DOMAIN,
            TTS_SERVICE_SPEAK,
            service_data,
            target=target,
            blocking=True,
        )

    hass.services.async_register(
        DOMAIN, SERVICE_SPEAK, _handle_speak, schema=SPEAK_SCHEMA
    )
