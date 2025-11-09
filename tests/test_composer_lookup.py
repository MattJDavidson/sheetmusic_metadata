"""Tests for composer lookup."""

import tempfile
from pathlib import Path

import pytest

from sheetmusic_metadata.composer_lookup import ComposerLookup


@pytest.fixture
def sample_composers_csv(tmp_path):
    """Create a temporary composers.csv file for testing."""
    csv_content = """simple_surname,full_name
Bach,"Bach, Johann Sebastian"
Beethoven,"Beethoven, Ludwig van"
Brahms,"Brahms, Johannes"
Dvorak,"Dvo??k, Anton?n"
"""
    csv_file = tmp_path / "composers.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    return csv_file


def test_get_full_name_bach(sample_composers_csv):
    """Test lookup 'Bach' and get 'Bach, Johann Sebastian'."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("Bach")
    assert result == "Bach, Johann Sebastian"


def test_get_full_name_beethoven(sample_composers_csv):
    """Test lookup 'Beethoven' and get 'Beethoven, Ludwig van'."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("Beethoven")
    assert result == "Beethoven, Ludwig van"


def test_get_full_name_fallback_unknown_composer(sample_composers_csv, capsys):
    """Test fallback for a name not in the list."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("UnknownComposer")
    assert result == "Unknowncomposer"  # Capitalized first letter
    captured = capsys.readouterr()
    assert "Warning" in captured.err
    assert "UnknownComposer" in captured.err


def test_get_full_name_handles_whitespace(sample_composers_csv):
    """Test handles leading/trailing whitespace in lookup key."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("  Brahms  ")
    assert result == "Brahms, Johannes"


def test_get_full_name_case_insensitive(sample_composers_csv):
    """Test case-insensitive lookup."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("BEETHOVEN")
    assert result == "Beethoven, Ludwig van"


def test_get_full_name_dvorak_with_unicode(sample_composers_csv):
    """Test lookup with Unicode characters."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("Dvorak")
    assert result == "Dvo??k, Anton?n"


def test_composer_lookup_csv_not_found():
    """Test error when CSV file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        ComposerLookup(Path("/nonexistent/composers.csv"))


def test_composer_lookup_duplicate_surnames_prefers_specific(capsys):
    """Test handling of duplicate surnames prefers most specific/complex mapping."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        csv_content = """simple_surname,full_name
Bach,"Bach, J.S."
Bach,"Bach, Johann Sebastian"
"""
        f.write(csv_content)
        f.flush()
        csv_path = Path(f.name)

    try:
        lookup = ComposerLookup(csv_path)
        # Should prefer the more specific/complex name (longer, without initials)
        result = lookup.get_full_name("Bach")
        assert result == "Bach, Johann Sebastian"
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "more specific" in captured.err
    finally:
        csv_path.unlink()


def test_composer_lookup_duplicate_surnames_prefers_longer(capsys):
    """Test that longer names are preferred when duplicates exist."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        csv_content = """simple_surname,full_name
Mozart,"Mozart, Wolfgang"
Mozart,"Mozart, Wolfgang Amadeus"
"""
        f.write(csv_content)
        f.flush()
        csv_path = Path(f.name)

    try:
        lookup = ComposerLookup(csv_path)
        # Should prefer the longer, more specific name
        result = lookup.get_full_name("Mozart")
        assert result == "Mozart, Wolfgang Amadeus"
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "more specific" in captured.err
    finally:
        csv_path.unlink()
