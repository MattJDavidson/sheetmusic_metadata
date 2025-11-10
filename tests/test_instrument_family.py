"""Tests for instrument family mapping."""

import pytest

from sheetmusic_metadata.instrument_family import get_instrument_family


@pytest.mark.parametrize(
    "instrument,expected_family",
    [
        ("Violin 1", "Strings"),
        ("Cello", "Strings"),
        ("Double Bass", "Strings"),
        ("Flute 2", "Woodwind"),
        ("Clarinet 1", "Woodwind"),
        ("Trumpet 1", "Brass"),
        ("Horn", "Brass"),
        ("Timpani", "Percussion"),
        ("Harp", "Harp"),
        ("Piano", "Keyboard"),
    ],
)
def test_get_instrument_family(instrument, expected_family):
    """Test instrument family mapping for various instruments."""
    result = get_instrument_family(instrument)
    assert result == expected_family


def test_get_instrument_family_unknown_instrument():
    """Test unknown instrument falls back to base name."""
    result = get_instrument_family("UnknownInstrument 1")
    assert result == "UnknownInstrument"
    # Note: The function may print warnings to stderr, but we verify
    # the fallback behavior by checking the return value
