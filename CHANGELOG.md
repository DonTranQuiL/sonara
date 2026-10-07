# Changelog

All notable changes to Sonara are documented here.

## [2.0.0] - Unreleased

### Changed
- Rebranded TikTok TTS 1.2.2 (`tiktoktts`) as **Sonara** (`sonara`). Same voices, modes and behaviour.
- New domain, entity IDs (`tts.sonara_*`, `select.sonara_*`, `text.sonara_message`, `button.sonara_speak`), service (`sonara.set_random_voices`) and Lovelace card (`custom:sonara-card`, served at `/sonara/sonara-card.js`).
- New icon and brand images.
- `asyncio.TimeoutError` replaced by the built-in `TimeoutError` (same exception on Python 3.11+); code formatted with ruff.

### Added
- `sonara.speak` service: speak on one or more media players with an optional per-call `voice` (including `random`), `engine` (proxy/direct) and `cache`. Wraps `tts.speak`; the TTS engine itself is unchanged.
- Config entry diagnostics with the session cookie and message text redacted.
- `VERSION` constant kept in sync with `manifest.json`.
- Test suite, CI (hassfest, HACS, pytest, ruff, CodeQL), release tooling and docs site.

### Migration
- Existing TikTok TTS users must remove the old integration and add Sonara again. See the README.
