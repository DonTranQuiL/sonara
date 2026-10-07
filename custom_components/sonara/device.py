"""Shared device info and entry titles for Sonara.

Every Sonara entity of a config entry hangs off one service device
("Sonara"), so the integration page shows one tidy device per connection.
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .const import (
    API_MODE_DIRECT,
    API_MODE_PROXY,
    CONF_API_MODE,
    DOMAIN,
    REBRAND_REPO,
    VERSION,
)

DEVICE_NAME = "Sonara"
MANUFACTURER = "DonTranQuiL"

_MODE_LABEL = {API_MODE_PROXY: "Proxy", API_MODE_DIRECT: "Direct"}


def entry_mode(entry: ConfigEntry) -> str:
    """Return the API mode of a config entry (proxy when unset)."""
    mode = entry.data.get(CONF_API_MODE, API_MODE_PROXY)
    return mode if mode in _MODE_LABEL else API_MODE_PROXY


def entry_title(mode: str) -> str:
    """Return the config entry title for a mode, e.g. 'Sonara (Proxy)'."""
    return f"{DEVICE_NAME} ({_MODE_LABEL.get(mode, _MODE_LABEL[API_MODE_PROXY])})"


def is_legacy_title(title: str) -> bool:
    """True for the auto titles of 2.0.0 ('Sonara (proxy: <url>)', 'Sonara (direct API)')."""
    return title.startswith(f"{DEVICE_NAME} (proxy: ") or title == (
        f"{DEVICE_NAME} (direct API)"
    )


def sonara_device_info(entry: ConfigEntry) -> DeviceInfo:
    """Return the device all entities of this config entry belong to."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=DEVICE_NAME,
        manufacturer=MANUFACTURER,
        model=f"TikTok TTS ({entry_mode(entry)})",
        sw_version=VERSION,
        entry_type=DeviceEntryType.SERVICE,
        configuration_url=REBRAND_REPO,
    )
