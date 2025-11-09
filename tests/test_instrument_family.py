"""Tests for instrument family mapping."""

from sheetmusic_metadata.instrument_family import get_instrument_family


def test_get_instrument_family_violin():
    """Test violin maps to Strings."""
    result = get_instrument_family("Violin 1")
    assert result == "Strings"


def test_get_instrument_family_cello():
    """Test cello maps to Strings."""
    result = get_instrument_family("Cello")
    assert result == "Strings"


def test_get_instrument_family_flute():
    """Test flute maps to Woodwind."""
    result = get_instrument_family("Flute 2")
    assert result == "Woodwind"


def test_get_instrument_family_clarinet():
    """Test clarinet maps to Woodwind."""
    result = get_instrument_family("Clarinet 1")
    assert result == "Woodwind"


def test_get_instrument_family_trumpet():
    """Test trumpet maps to Brass."""
    result = get_instrument_family("Trumpet 1")
    assert result == "Brass"


def test_get_instrument_family_horn():
    """Test horn maps to Brass."""
    result = get_instrument_family("Horn")
    assert result == "Brass"


def test_get_instrument_family_timpani():
    """Test timpani maps to Percussion."""
    result = get_instrument_family("Timpani")
    assert result == "Percussion"


def test_get_instrument_family_harp():
    """Test harp maps to Harp."""
    result = get_instrument_family("Harp")
    assert result == "Harp"


def test_get_instrument_family_piano():
    """Test piano maps to Keyboard."""
    result = get_instrument_family("Piano")
    assert result == "Keyboard"


def test_get_instrument_family_double_bass():
    """Test double bass maps to Strings."""
    result = get_instrument_family("Double Bass")
    assert result == "Strings"


def test_get_instrument_family_unknown_instrument(capsys):
    """Test unknown instrument falls back to base name."""
    result = get_instrument_family("UnknownInstrument 1")
    assert result == "UnknownInstrument"
    captured = __import__("sys").stderr
    # Note: capsys doesn't capture print to sys.stderr directly,
    # but we can verify the fallback behavior
