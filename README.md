# Sonara

A cast of voices for the house.

Sonara is a Home Assistant custom integration that speaks through a community speech proxy, or directly against the same unofficial cloud speech API. It ships with a Lovelace bench: pick a language, pick a voice, type a line, send it to a media player.

The name is Sonara. It is not affiliated with the upstream speech service, and the integration does not use that service's trademark.

## What you get

- Config flow with a live connection test
- Proxy mode (no account) and direct mode (session cookie, regional fallback)
- One TTS entity per config entry
- Shared controls: language, voice, speaker, message, speak
- Random-voice pool saved across restarts
- Dashboard card, registered automatically: `custom:sonara-card`

## Install

1. Copy `custom_components/sonara` into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Settings → Devices & services → Add integration → **Sonara**.
4. Prefer **Community proxy** unless you are self-hosting or you already know the direct-mode risks.

HACS: add this repository as a custom integration.

## Use the card

The card registers itself after startup. Add it from the card picker as **Sonara**, or in YAML:

```yaml
type: custom:sonara-card
```

If Lovelace is in YAML mode, add the resource yourself:

```yaml
url: /sonara/sonara-card.js
type: module
```

## Entities

| Entity | What it does |
| --- | --- |
| `tts.sonara_proxy` / `tts.sonara_direct` | The speech engine for that config entry |
| `select.sonara_language` | Language group |
| `select.sonara_voice` | Voice in the selected group. Raw API code is in the `code` attribute |
| `select.sonara_device` | Media player to speak on |
| `text.sonara_message` | Line to speak |
| `button.sonara_speak` | Speaks the current message with the current voice |

Service: `sonara.set_random_voices` with a `languages` list. The card calls this for you.

Example automation:

```yaml
action: tts.speak
target:
  entity_id: tts.sonara_proxy
data:
  media_player_entity_id: media_player.kitchen
  message: "The kettle is done."
  options:
    voice: en_male_narration
```

## Modes

**Proxy.** Talks to an HTTP proxy that forwards speech requests. Default is the community proxy from [Weilbyte](https://github.com/Weilbyte/tiktok-tts). Self-host that proxy and paste your URL if the public one is down.

**Direct.** Calls the upstream speech hosts with your `sessionid` cookie and falls through regional endpoints. Unofficial. The cookie expires. Use may violate that service's terms. Sonara raises a repair issue when the session is rejected.

## Credits

Voice engine originally wrapped for Home Assistant by Philipp Lüttecke (`@philipp-luettecke`). Community proxy by Weilbyte. Extended by Steven Fox (`@sfox38`). This package is a rename and cleanup so it can be republished without the upstream trademark in the product name.

Voice codes are unchanged. Display names for a few character voices were made generic.

## Upgrading from the old name

Entity IDs and the card type changed. Update dashboards and automations:

- `custom:tiktoktts-card` → `custom:sonara-card`
- `select.tiktoktts_*` → `select.sonara_*`
- `text.tiktoktts_message` → `text.sonara_message`
- `button.tiktoktts_speak` → `button.sonara_speak`
- service domain `tiktoktts` → `sonara`

Remove the old integration before adding Sonara. They are different domains.
