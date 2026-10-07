"""Unit tests for the TTS helpers (no network)."""

from __future__ import annotations

from custom_components.sonara.const import (
    ALL_VOICES,
    DEFAULT_VOICE,
    DIRECT_API_CHUNK_SIZE,
    VOICES_BY_LANGUAGE,
)
from custom_components.sonara.tts import _split_text


def test_default_voice_is_known():
    assert DEFAULT_VOICE in ALL_VOICES
    assert DEFAULT_VOICE in VOICES_BY_LANGUAGE["en_us"]


def test_voice_codes_unique():
    assert len(ALL_VOICES) == len(set(ALL_VOICES))


def test_split_short_text_is_single_chunk():
    assert _split_text("Hello there.", DIRECT_API_CHUNK_SIZE) == ["Hello there."]


def test_split_respects_chunk_size_and_keeps_words():
    text = ("The kettle is done. " * 30).strip()
    chunks = _split_text(text, 50)
    assert len(chunks) > 1
    assert all(len(c) <= 50 for c in chunks)
    # Nothing lost: the words come back in order.
    assert " ".join(chunks).split() == text.split()


def test_split_hard_cuts_unbroken_text():
    text = "x" * 130
    chunks = _split_text(text, 50)
    assert all(len(c) <= 50 for c in chunks)
    assert "".join(chunks) == text
