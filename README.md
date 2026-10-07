<div align="center">

<img src="custom_components/sonara/brand/icon.png" alt="Sonara" width="160">

# Sonara

**TikTok text-to-speech voices for Home Assistant — narrators, characters and singing voices, with a dashboard voice bench.**

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![HA](https://img.shields.io/badge/Home%20Assistant-2024.7.0+-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/DonTranQuiL/sonara)](https://github.com/DonTranQuiL/sonara/releases)
[![Issues](https://img.shields.io/github/issues/DonTranQuiL/sonara)](https://github.com/DonTranQuiL/sonara/issues)
[![Home Assistant CI](https://img.shields.io/github/actions/workflow/status/DonTranQuiL/sonara/hass-ci.yml?label=Home%20Assistant%20CI&style=for-the-badge)](https://github.com/DonTranQuiL/sonara/actions/workflows/hass-ci.yml)
[![Code Checks](https://img.shields.io/github/actions/workflow/status/DonTranQuiL/sonara/codechecker.yml?style=for-the-badge&label=CODE%20CHECKS&color=5dbb0f)](https://github.com/DonTranQuiL/sonara/actions)
[![Tests](https://img.shields.io/github/actions/workflow/status/DonTranQuiL/sonara/pytest.yml?style=for-the-badge&label=TESTS&color=5dbb0f)](https://github.com/DonTranQuiL/sonara/actions)
[![HACS Validation](https://img.shields.io/github/actions/workflow/status/DonTranQuiL/sonara/hacs.yaml?style=for-the-badge&label=HACS%20VALIDATION&color=5dbb0f)](https://github.com/DonTranQuiL/sonara/actions)
[![hassfest](https://img.shields.io/github/actions/workflow/status/DonTranQuiL/sonara/hassfest.yaml?style=for-the-badge&label=HASSFEST&color=5dbb0f)](https://github.com/DonTranQuiL/sonara/actions)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Maintainer](https://img.shields.io/badge/maintainer-%40DonTranQuiL-007ec6?style=for-the-badge)](https://github.com/DonTranQuiL)
[![Donate](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-ffdd00?style=for-the-badge)](https://ko-fi.com/DonTranQuiL)
[![Discord](https://img.shields.io/badge/Discord-join%20community-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/qaHPTTKHae)

</div>

Sonara is a Home Assistant text-to-speech (TTS) integration for TikTok's voices. It gives you a regular `tts.*` entity you can use in any automation, plus a ready-made Lovelace card to pick a language and voice, type a line and play it on any media player.

Sonara is the rebranded continuation of the TikTok TTS integration by Philipp Lüttecke and Steven Fox (see [Credits](#credits)). It is unofficial and not affiliated with or endorsed by TikTok or ByteDance.

## Features

- **106 voices in 16 language groups**: US/UK/Australian English, character voices, singing voices, French, Italian, Spanish (ES/MX), German, Portuguese (BR/PT), Indonesian, Japanese, Korean and Vietnamese
- **Two connection modes**
  - **Community proxy** (recommended): no account needed, uses the open-source proxy by [Weilbyte](https://github.com/Weilbyte/tiktok-tts). You can self-host it.
  - **Direct**: talks to TikTok's own (unofficial) speech API with your browser `sessionid` cookie and falls back across regional endpoints automatically
- **Live connection test** in the setup and options screens, so a bad URL or expired session is caught before saving
- **Standard TTS entity** (`tts.sonara_proxy` / `tts.sonara_direct`) with per-call voice override and per-language voice lists
- **Random voice**: pass `voice: random` and Sonara picks a voice from your chosen language pool (saved across restarts)
- **Lovelace voice bench** (`custom:sonara-card`), registered automatically
- **Shared helper entities** for dashboards and scripts: language, voice, output device, message and a Speak button
- **Long messages** are split on sentence and word boundaries in direct mode and joined back into one clip
- **Retries and fallback**: 2 retries per request, then the other regional endpoints (direct mode)
- **Repair issue** when TikTok rejects your session cookie in direct mode
- Options changes apply on save, no restart needed

## How it works

| Mode | Request | Account | Notes |
| --- | --- | --- | --- |
| Community proxy | `POST {endpoint}/api/generation` with `{"text", "voice"}` | None | The proxy handles long texts. Health check: `GET {endpoint}/api/status`. Default: `https://tiktok-tts.weilnet.workers.dev` |
| Direct | `POST {endpoint}/media/api/text/speech/invoke/` | TikTok `sessionid` cookie | Max ~200 characters per request, so Sonara chunks long text. Unofficial API: it can change at any time and **may violate TikTok's Terms of Service**. Use at your own risk. |

Both modes return MP3 audio to Home Assistant's TTS pipeline, so Home Assistant's normal TTS caching applies.

You can add one proxy entry and one direct entry at the same time. The helper entities and the card are shared between them.

## Installation

### HACS (recommended)

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/DonTranQuiL/sonara` as an **Integration**.
2. Search for **Sonara** and download it.
3. Restart Home Assistant.
4. **Settings → Devices & services → Add integration → Sonara**.

### Manual

1. Download the latest release and copy `custom_components/sonara` into `config/custom_components/`.
2. Restart Home Assistant.
3. **Settings → Devices & services → Add integration → Sonara**.

## Configuration

The setup wizard asks for a connection mode first.

**Community proxy**

| Field | Default | Description |
| --- | --- | --- |
| Proxy endpoint URL | `https://tiktok-tts.weilnet.workers.dev` | Must start with `http://` or `https://`. Use your own instance for better reliability. |
| Default voice | `en_us_001` | Voice used when an automation doesn't pass one. |

**Direct**

| Field | Default | Description |
| --- | --- | --- |
| API endpoint | `https://api16-normal-c-useast1a.tiktokv.com` | Tried first. The other known regional endpoints are used as fallback. |
| Session ID | — | The value of the `sessionid` cookie from a logged-in TikTok browser session (F12 → Application → Cookies). It expires; Sonara raises a repair issue when it does. |
| Default voice | `en_us_001` | Voice used when an automation doesn't pass one. |

Change any of these later with **Configure** on the integration card.

## Entities

| Entity | Type | What it does |
| --- | --- | --- |
| `tts.sonara_proxy` / `tts.sonara_direct` | TTS | The speech engine for that config entry |
| `select.sonara_language` | Select | Language group (plus **All Languages** and **Random Voice**) |
| `select.sonara_voice` | Select | Voice in the selected group. The raw voice code is in the `code` attribute |
| `select.sonara_device` | Select | Media player to speak on. Updates when players come and go |
| `text.sonara_message` | Text | The line to speak (restored after restart) |
| `button.sonara_speak` | Button | Speaks the message with the selected voice on the selected device |

The TTS entities are created per config entry. The select, text and button entities exist once, however many entries you add.

## Services

### `sonara.set_random_voices`

Sets which language groups the random voice picks from. The card calls this for you.

```yaml
action: sonara.set_random_voices
data:
  languages: [en_us, en_uk, music]
```

Codes: `en_us`, `en_uk`, `en_au`, `disney` (characters), `music` (singing), `fr`, `it`, `es`, `es_mx`, `de`, `pt_br`, `pt_pt`, `id`, `ja`, `ko`, `vi`. An empty list clears the pool.

## Lovelace card

The card resource is added automatically after Home Assistant starts. Add the card from the picker (**Sonara**) or in YAML:

```yaml
type: custom:sonara-card
```

If your dashboards are in YAML mode, add the resource yourself:

```yaml
url: /sonara/sonara-card.js
type: module
```

## Automation examples

Announce with a specific voice:

```yaml
action: tts.speak
target:
  entity_id: tts.sonara_proxy
data:
  media_player_entity_id: media_player.kitchen
  message: "The washing machine is done."
  options:
    voice: en_us_ghostface
```

Random voice from your pool:

```yaml
action: tts.speak
target:
  entity_id: tts.sonara_proxy
data:
  media_player_entity_id: media_player.living_room
  message: "Someone is at the door."
  options:
    voice: random
```

Speak whatever is in the dashboard fields:

```yaml
action: button.press
target:
  entity_id: button.sonara_speak
```

## Migrating from TikTok TTS (`tiktoktts`)

Sonara uses a new domain (`sonara`), so Home Assistant treats it as a different integration. There is no automatic migration:

1. Remove the old **TikTok TTS** integration and its `custom_components/tiktoktts` folder.
2. Install Sonara and add it again (your proxy URL or session ID is not carried over).
3. Update dashboards and automations:
   - `custom:tiktoktts-card` → `custom:sonara-card`
   - `tts.tiktoktts_proxy` / `tts.tiktoktts_direct` → `tts.sonara_proxy` / `tts.sonara_direct`
   - `select.tiktoktts_*`, `text.tiktoktts_message`, `button.tiktoktts_speak` → `select.sonara_*`, `text.sonara_message`, `button.sonara_speak`
   - `tiktoktts.set_random_voices` → `sonara.set_random_voices`
4. If the old card resource `/tiktoktts/tiktoktts-card.js` is still listed under **Settings → Dashboards → Resources**, delete it.

Voice codes did not change.

## Troubleshooting

- **"Could not connect" / timeout during setup**: the public proxy is sometimes down or rate limited. Try again later or self-host [Weilbyte's proxy](https://github.com/Weilbyte/tiktok-tts) and enter its URL.
- **"The endpoint responded but reports it is currently unavailable"**: the proxy's `/api/status` says it is not available right now.
- **Direct mode stops speaking / repair issue "Direct API session expired"**: copy a fresh `sessionid` cookie and paste it under **Configure**.
- **Sounds like the default voice**: the voice code isn't recognised and TikTok falls back to its default voice.
- **Card not found**: check that `/sonara/sonara-card.js` is in your dashboard resources (YAML mode needs it added by hand), then hard-refresh the browser.
- **Debug logging**:

```yaml
logger:
  logs:
    custom_components.sonara: debug
```

## Docs

Project docs: [dontranquil.github.io/sonara](https://dontranquil.github.io/sonara/)

## Credits

- **Philipp Lüttecke** ([@philipp-luettecke](https://github.com/philipp-luettecke/tiktoktts)): original TikTok TTS integration for Home Assistant
- **Steven Fox** ([@sfox38](https://github.com/sfox38)): extended fork that Sonara is based on (version 1.2.2)
- **Weilbyte** ([tiktok-tts](https://github.com/Weilbyte/tiktok-tts)): community TTS proxy
- **oscie57** ([tiktok-voice](https://github.com/oscie57/tiktok-voice)): voice list reference
- **DonTranQuiL**: Sonara rebrand and maintenance

## Disclaimer

Unofficial. Not affiliated with, endorsed by or connected to TikTok or ByteDance. "TikTok" is a trademark of its owner and is used here only to describe what the integration talks to. Direct mode uses an undocumented API and your own session cookie, which may violate TikTok's Terms of Service. Use at your own risk.

## Support

- Issues: [GitHub Issues](https://github.com/DonTranQuiL/sonara/issues)
- Community: [Discord](https://discord.gg/qaHPTTKHae)
- Tip jar: [Ko-fi](https://ko-fi.com/DonTranQuiL)

## License

MIT — see [LICENSE](LICENSE) and [NOTICE](NOTICE.md). The original MIT copyright notice is kept.
