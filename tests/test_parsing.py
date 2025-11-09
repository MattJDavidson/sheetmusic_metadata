"""Tests for filename parsing."""

import pytest

from sheetmusic_metadata.parsing import parse_filename


def test_filename_parsing_beethoven_symphony_5():
    """Test parsing Beethoven Symphony 5 filename."""
    components = parse_filename("Beethoven_Symphony05_Op67_Violin1.pdf")

    assert components.composer_last_name == "Beethoven"
    assert components.work_identifier == "Symphony05"
    assert components.opus == "Op67"
    assert components.part == "Violin1"


def test_filename_parsing_rimsky_korsakov_scheherazade():
    """Test parsing Rimsky-Korsakov Scheherazade filename."""
    components = parse_filename("RimskyKorsakov_Scheherazade_Op35_Flute2.pdf")

    assert components.composer_last_name == "RimskyKorsakov"
    assert components.work_identifier == "Scheherazade"
    assert components.opus == "Op35"
    assert components.part == "Flute2"


def test_filename_parsing_vaughan_williams_lark_ascending():
    """Test parsing Vaughan Williams The Lark Ascending filename (3-part schema)."""
    components = parse_filename("VaughanWilliams_LarkAscending_Viola.pdf")

    assert components.composer_last_name == "VaughanWilliams"
    assert components.work_identifier == "LarkAscending"
    assert components.opus == "NoOp"
    assert components.part == "Viola"


def test_filename_parsing_rimsky_korsakov_symphony_1():
    """Test parsing Rimsky-Korsakov Symphony 1 filename."""
    components = parse_filename("RimskyKorsakov_Symphony01_Op1_Oboe1.pdf")

    assert components.composer_last_name == "RimskyKorsakov"
    assert components.work_identifier == "Symphony01"
    assert components.opus == "Op1"
    assert components.part == "Oboe1"


def test_filename_parsing_without_extension():
    """Test parsing filename without .pdf extension."""
    components = parse_filename("Beethoven_Symphony05_Op67_Violin1")

    assert components.composer_last_name == "Beethoven"
    assert components.work_identifier == "Symphony05"
    assert components.opus == "Op67"
    assert components.part == "Violin1"


def test_filename_parsing_invalid_too_few_parts():
    """Test parsing fails with too few parts."""
    with pytest.raises(ValueError, match="does not match the expected schema"):
        parse_filename("Beethoven_Symphony05.pdf")


def test_filename_parsing_invalid_too_many_parts():
    """Test parsing fails with too many parts."""
    with pytest.raises(ValueError, match="does not match the expected schema"):
        parse_filename("Beethoven_Symphony05_Op67_Violin1_Extra.pdf")


def test_filename_parsing_invalid_empty_composer():
    """Test parsing fails with empty composer."""
    with pytest.raises(ValueError, match="missing one of the required components"):
        parse_filename("_Symphony05_Op67_Violin1.pdf")


def test_filename_parsing_invalid_empty_work():
    """Test parsing fails with empty work."""
    with pytest.raises(ValueError, match="missing one of the required components"):
        parse_filename("Beethoven__Op67_Violin1.pdf")


def test_filename_parsing_invalid_empty_part():
    """Test parsing fails with empty part."""
    with pytest.raises(ValueError, match="missing one of the required components"):
        parse_filename("Beethoven_Symphony05_Op67_.pdf")
