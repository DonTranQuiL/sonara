# Changelog

All notable changes to Sonara are documented here.

## [2.0.0] - Unreleased

### Changed
- Rebranded TikTok TTS 1.2.2 (`tiktoktts`) as **Sonara** (`sonara`). Same voices, modes and behaviour.
- New domain, entity IDs (`tts.sonara_*`, `select.sonara_*`, `text.sonara_message`, `button.sonara_speak`), service (`sonara.set_random_voices`) and Lovelace card (`custom:sonara-card`, served at `/sonara/sonara-card.js`).
- New icon and brand images.
- `asyncio.TimeoutError` replaced by the built-in `TimeoutError` (same exception on Python 3.11+); code formatted with ruff.

### Added
- `VERSION` constant kept in sync with `manifest.json`.
- Test suite, CI (hassfest, HACS, pytest, ruff, CodeQL), release tooling and docs site.

### Migration
- Existing TikTok TTS users must remove the old integration and add Sonara again. See the README.
