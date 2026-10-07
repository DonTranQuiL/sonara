"""Config flow tests for Sonara (endpoint checks are mocked)."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sonara.const import (
    API_MODE_DIRECT,
    API_MODE_PROXY,
    CONF_API_MODE,
    CONF_ENDPOINT,
    CONF_SESSION_ID,
    CONF_VOICE,
    DEFAULT_PROXY_ENDPOINT,
    DEFAULT_VOICE,
    DIRECT_API_ENDPOINTS,
    DOMAIN,
)

pytestmark = pytest.mark.usefixtures("skip_deps")

PROXY_CHECK = "custom_components.sonara.config_flow._test_proxy_endpoint"
DIRECT_CHECK = "custom_components.sonara.config_flow._test_direct_endpoint"


@pytest.fixture(autouse=True)
def no_setup():
    with (
        patch("custom_components.sonara.async_setup", return_value=True),
        patch("custom_components.sonara.async_setup_entry", return_value=True),
    ):
        yield


async def _start(hass, mode):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    return await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_MODE: mode}
    )


async def test_proxy_flow_creates_entry(hass):
    result = await _start(hass, API_MODE_PROXY)
    assert result["step_id"] == "proxy"
    with patch(PROXY_CHECK, return_value=None):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ENDPOINT: DEFAULT_PROXY_ENDPOINT + "/", CONF_VOICE: DEFAULT_VOICE},
        )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Sonara (Proxy)"
    assert result["data"] == {
        CONF_API_MODE: API_MODE_PROXY,
        CONF_ENDPOINT: DEFAULT_PROXY_ENDPOINT,
        CONF_VOICE: DEFAULT_VOICE,
    }


async def test_proxy_flow_rejects_bad_scheme(hass):
    result = await _start(hass, API_MODE_PROXY)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_ENDPOINT: "ftp://example", CONF_VOICE: DEFAULT_VOICE}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_url_scheme"}


async def test_proxy_flow_shows_endpoint_error(hass):
    result = await _start(hass, API_MODE_PROXY)
    with patch(PROXY_CHECK, return_value="endpoint_unavailable"):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ENDPOINT: DEFAULT_PROXY_ENDPOINT, CONF_VOICE: DEFAULT_VOICE},
        )
    assert result["errors"] == {"base": "endpoint_unavailable"}


async def test_proxy_flow_aborts_when_proxy_exists(hass):
    MockConfigEntry(
        domain=DOMAIN,
        data={CONF_API_MODE: API_MODE_PROXY, CONF_ENDPOINT: DEFAULT_PROXY_ENDPOINT},
    ).add_to_hass(hass)
    result = await _start(hass, API_MODE_PROXY)
    with patch(PROXY_CHECK, return_value=None):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ENDPOINT: DEFAULT_PROXY_ENDPOINT, CONF_VOICE: DEFAULT_VOICE},
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_direct_flow_creates_entry(hass):
    result = await _start(hass, API_MODE_DIRECT)
    assert result["step_id"] == "direct"
    with patch(DIRECT_CHECK, return_value=None):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_ENDPOINT: DIRECT_API_ENDPOINTS[0],
                CONF_SESSION_ID: "  abc123  ",
                CONF_VOICE: DEFAULT_VOICE,
            },
        )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Sonara (Direct)"
    assert result["data"][CONF_SESSION_ID] == "abc123"
    assert result["data"][CONF_API_MODE] == API_MODE_DIRECT


async def test_direct_flow_rejected_session(hass):
    result = await _start(hass, API_MODE_DIRECT)
    with patch(DIRECT_CHECK, return_value="direct_api_rejected"):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_ENDPOINT: DIRECT_API_ENDPOINTS[0],
                CONF_SESSION_ID: "expired",
                CONF_VOICE: DEFAULT_VOICE,
            },
        )
    assert result["errors"] == {"base": "direct_api_rejected"}
