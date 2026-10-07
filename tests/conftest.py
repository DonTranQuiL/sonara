"""Shared fixtures for Sonara tests."""

from __future__ import annotations

from unittest.mock import patch

import pytest


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
