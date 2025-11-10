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


@pytest.mark.parametrize(
    "surname,expected_full_name",
    [
        ("Bach", "Bach, Johann Sebastian"),
        ("Beethoven", "Beethoven, Ludwig van"),
    ],
)
def test_get_full_name_valid_composers(
    sample_composers_csv, surname, expected_full_name
):
    """Test lookup of valid composer surnames."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name(surname)
    assert result == expected_full_name


def test_get_full_name_fallback_unknown_composer(sample_composers_csv, capsys):
    """Test fallback for a name not in the list."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("UnknownComposer")
    assert result == "Unknowncomposer"  # Capitalized first letter
    captured = capsys.readouterr()
    assert "Warning" in captured.err
    assert "UnknownComposer" in captured.err


@pytest.mark.parametrize(
    "surname_input,expected_full_name",
    [
        ("  Brahms  ", "Brahms, Johannes"),  # Whitespace handling
        ("BEETHOVEN", "Beethoven, Ludwig van"),  # Case insensitive
        ("beethoven", "Beethoven, Ludwig van"),  # Lowercase
        ("Beethoven", "Beethoven, Ludwig van"),  # Normal case
    ],
)
def test_get_full_name_normalization(
    sample_composers_csv, surname_input, expected_full_name
):
    """Test lookup handles whitespace and case normalization."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name(surname_input)
    assert result == expected_full_name


def test_get_full_name_dvorak_with_unicode(sample_composers_csv):
    """Test lookup with Unicode characters."""
    lookup = ComposerLookup(sample_composers_csv)
    result = lookup.get_full_name("Dvorak")
    assert result == "Dvo??k, Anton?n"


def test_composer_lookup_csv_not_found():
    """Test error when CSV file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        ComposerLookup(Path("/nonexistent/composers.csv"))


@pytest.mark.parametrize(
    "csv_content,surname,expected_full_name",
    [
        (
            """simple_surname,full_name
Bach,"Bach, J.S."
Bach,"Bach, Johann Sebastian"
""",
            "Bach",
            "Bach, Johann Sebastian",
        ),
        (
            """simple_surname,full_name
Mozart,"Mozart, Wolfgang"
Mozart,"Mozart, Wolfgang Amadeus"
""",
            "Mozart",
            "Mozart, Wolfgang Amadeus",
        ),
    ],
)
def test_composer_lookup_duplicate_surnames_prefers_specific(
    capsys, csv_content, surname, expected_full_name
):
    """Test handling of duplicate surnames prefers most specific/complex mapping."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        f.write(csv_content)
        f.flush()
        csv_path = Path(f.name)

    try:
        lookup = ComposerLookup(csv_path)
        result = lookup.get_full_name(surname)
        assert result == expected_full_name
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "more specific" in captured.err
    finally:
        csv_path.unlink()
