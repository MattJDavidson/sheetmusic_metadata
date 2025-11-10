"""Tests for filename parsing."""

import pytest

from sheetmusic_metadata.parsing import parse_filename


@pytest.mark.parametrize(
    "filename,expected_composer,expected_work,expected_opus,expected_part",
    [
        # 4-part schema (with opus)
        (
            "Beethoven_Symphony05_Op67_Violin1.pdf",
            "Beethoven",
            "Symphony05",
            "Op67",
            "Violin1",
        ),
        (
            "RimskyKorsakov_Scheherazade_Op35_Flute2.pdf",
            "RimskyKorsakov",
            "Scheherazade",
            "Op35",
            "Flute2",
        ),
        (
            "RimskyKorsakov_Symphony01_Op1_Oboe1.pdf",
            "RimskyKorsakov",
            "Symphony01",
            "Op1",
            "Oboe1",
        ),
        # 3-part schema (no opus)
        (
            "VaughanWilliams_LarkAscending_Viola.pdf",
            "VaughanWilliams",
            "LarkAscending",
            "NoOp",
            "Viola",
        ),
        # Without .pdf extension
        (
            "Beethoven_Symphony05_Op67_Violin1",
            "Beethoven",
            "Symphony05",
            "Op67",
            "Violin1",
        ),
    ],
)
def test_filename_parsing_valid(
    filename, expected_composer, expected_work, expected_opus, expected_part
):
    """Test parsing valid filenames with various formats."""
    components = parse_filename(filename)
    assert components.composer_last_name == expected_composer
    assert components.work_identifier == expected_work
    assert components.opus == expected_opus
    assert components.part == expected_part


@pytest.mark.parametrize(
    "filename,expected_match",
    [
        (
            "Beethoven_Symphony05.pdf",
            "does not match the expected schema",
        ),  # Too few parts
        (
            "Beethoven_Symphony05_Op67_Violin1_Extra.pdf",
            "does not match the expected schema",
        ),  # Too many parts
        (
            "_Symphony05_Op67_Violin1.pdf",
            "missing one of the required components",
        ),  # Empty composer
        (
            "Beethoven__Op67_Violin1.pdf",
            "missing one of the required components",
        ),  # Empty work
        (
            "Beethoven_Symphony05_Op67_.pdf",
            "missing one of the required components",
        ),  # Empty part
    ],
)
def test_filename_parsing_invalid(filename, expected_match):
    """Test parsing fails with invalid filenames."""
    with pytest.raises(ValueError, match=expected_match):
        parse_filename(filename)
