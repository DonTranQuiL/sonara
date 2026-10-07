"""Smoke tests for package constants, manifest and the rebrand."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from custom_components.sonara import const
from custom_components.sonara.const import DOMAIN, VERSION

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "sonara"


def _manifest() -> dict:
    return json.loads((COMPONENT / "manifest.json").read_text(encoding="utf-8"))


def test_domain_and_version():
    manifest = _manifest()
    assert DOMAIN == "sonara"
    assert manifest["domain"] == DOMAIN
    assert manifest["name"] == "Sonara"
    # Never hardcode the version: const and manifest must simply agree.
    assert manifest["version"] == VERSION


def test_manifest_urls_and_owner():
    manifest = _manifest()
    assert manifest["documentation"] == "https://github.com/DonTranQuiL/sonara"
    assert manifest["issue_tracker"] == "https://github.com/DonTranQuiL/sonara/issues"
    assert manifest["codeowners"] == ["@DonTranQuiL"]
    assert manifest["config_flow"] is True
    assert set(manifest["dependencies"]) == {"frontend", "http"}


def test_hacs_json():
    hacs = json.loads((ROOT / "hacs.json").read_text(encoding="utf-8"))
    assert hacs["name"] == "Sonara"
    assert hacs["content_in_root"] is False
    assert "filename" not in hacs  # no zip_release, so no filename


def test_entity_ids_use_new_domain():
    assert const.ENTITY_ID_LANGUAGE == "select.sonara_language"
    assert const.ENTITY_ID_VOICE == "select.sonara_voice"
    assert const.ENTITY_ID_DEVICE == "select.sonara_device"
    assert const.ENTITY_ID_MESSAGE == "text.sonara_message"
    assert const.ENTITY_ID_SPEAK == "button.sonara_speak"
    assert const.ENTITY_ID_TTS_PROXY == "tts.sonara_proxy"
    assert const.ENTITY_ID_TTS_DIRECT == "tts.sonara_direct"


def test_attribution_keeps_upstream_credits():
    for credit in (
        "philipp-luettecke/tiktoktts",
        "sfox38/tiktoktts",
        "Weilbyte/tiktok-tts",
        "oscie57/tiktok-voice",
    ):
        assert credit in const.ATTRIBUTION


def test_no_leftover_old_domain():
    """Only the upstream credit URLs may still mention the old domain."""
    allowed = re.compile(r"github\.com/(philipp-luettecke|sfox38)/tiktoktts")
    for path in COMPONENT.rglob("*"):
        if path.suffix not in {".py", ".json", ".yaml", ".js"}:
            continue
        text = allowed.sub("", path.read_text(encoding="utf-8"))
        assert "tiktoktts" not in text.lower(), path
        assert "TikTokTTS" not in text, path


def test_card_files_match_registration():
    from custom_components.sonara import frontend

    assert frontend._DOMAIN == DOMAIN
    assert frontend._CARD_FILENAME == "sonara-card.js"
    card = (COMPONENT / "www" / frontend._CARD_FILENAME).read_text(encoding="utf-8")
    assert 'customElements.define("sonara-card"' in card
    assert 'type:        "sonara-card"' in card
    # The card header loads the icon from the static path served by the integration.
    assert 'src="/sonara/icon.png"' in card
    assert (COMPONENT / "www" / "icon.png").is_file()


def test_brand_images_present():
    for name in ("icon.png", "dark_icon.png", "logo.png", "dark_logo.png"):
        assert (COMPONENT / "brand" / name).is_file(), name


def test_strings_and_translation_in_sync():
    strings = json.loads((COMPONENT / "strings.json").read_text(encoding="utf-8"))
    english = json.loads(
        (COMPONENT / "translations" / "en.json").read_text(encoding="utf-8")
    )
    assert strings == english


def test_services_yaml_matches_languages():
    services = yaml.safe_load((COMPONENT / "services.yaml").read_text("utf-8"))
    assert "set_random_voices" in services
    options = services["set_random_voices"]["fields"]["languages"]["selector"][
        "select"
    ]["options"]
    assert {o["value"] for o in options} == set(const.SUPPORTED_LANGUAGES)
