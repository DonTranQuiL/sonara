# Changelog

All notable changes to Sonara are documented here.

## [2.0.0] - Unreleased

### Changed
- Rebranded TikTok TTS 1.2.2 (`tiktoktts`) as **Sonara** (`sonara`). Same voices, modes and behaviour.
- New domain, entity IDs (`tts.sonara_*`, `select.sonara_*`, `text.sonara_message`, `button.sonara_speak`), service (`sonara.set_random_voices`) and Lovelace card (`custom:sonara-card`, served at `/sonara/sonara-card.js`).
- New icon and brand images.
- `asyncio.TimeoutError` replaced by the built-in `TimeoutError` (same exception on Python 3.11+); code formatted with ruff.

### Added
- One **Sonara** service device per config entry (manufacturer DonTranQuiL, model `TikTok TTS (proxy)` / `TikTok TTS (direct)`, software version, link to the repo). All Sonara entities are linked to it.
- Entity names come from translations (`has_entity_name`), with icons from `icons.json`. Friendly names stay "Sonara Proxy", "Sonara Voice", etc.
- `sonara.speak` service: speak on one or more media players with an optional per-call `voice` (including `random`), `engine` (proxy/direct) and `cache`. Wraps `tts.speak`; the TTS engine itself is unchanged.
- Config entry diagnostics with the session cookie and message text redacted.
- `VERSION` constant kept in sync with `manifest.json`.
- Test suite, CI (hassfest, HACS, pytest, ruff, CodeQL), release tooling and docs site.

### Migration
- Config entry titles are now **Sonara (Proxy)** / **Sonara (Direct)**. Entries created by an earlier 2.0.0 build that were titled after the proxy URL (`Sonara (proxy: https://…)`) or `Sonara (direct API)` are renamed automatically on the next start; titles you changed yourself are kept.
- The Language, Voice and Device selects are now *configuration* entities, so they appear under *Configuration* on the device page and auto-generated dashboards leave them out. The card and automations are not affected.
- Entity IDs and unique IDs did not change, so existing entities are kept and simply attach to the new device after a restart.
- Existing TikTok TTS users must remove the old integration and add Sonara again. See the README.
