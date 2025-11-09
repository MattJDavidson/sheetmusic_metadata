"""Tests for formatting functions."""

from sheetmusic_metadata.formatting import (
    format_opus_string,
    format_part_string,
    format_work_title,
)


def test_format_work_title_adds_leading_zero_to_single_digit():
    """Test adds leading zero to single-digit numbers."""
    result = format_work_title("Symphony5")
    assert result == "Symphony 05"


def test_format_work_title_preserves_double_digit_numbers():
    """Test preserves double-digit numbers."""
    result = format_work_title("Symphony09")
    assert result == "Symphony 09"


def test_format_work_title_adds_space_for_camelcase():
    """Test adds space for camelCase."""
    result = format_work_title("ViolinConcerto")
    assert result == "Violin Concerto"


def test_format_work_title_handles_multiple_camelcase():
    """Test handles multiple camelCase words."""
    result = format_work_title("ViolinConcertoNo1")
    assert result == "Violin Concerto No 01"


def test_format_opus_string_handles_single_digit_opus():
    """Test handles single-digit opus numbers."""
    result = format_opus_string("Op1")
    assert result == "Op. 1"


def test_format_opus_string_handles_double_digit_opus():
    """Test handles double-digit opus numbers."""
    result = format_opus_string("Op67")
    assert result == "Op. 67"


def test_format_opus_string_handles_no_opus():
    """Test handles NoOp."""
    result = format_opus_string("NoOp")
    assert result == "NoOp"


def test_format_part_string_adds_space_before_numbers():
    """Test adds space before numbers."""
    result = format_part_string("Violin1")
    assert result == "Violin 1"


def test_format_part_string_handles_double_bass():
    """Test handles DoubleBass special case."""
    result = format_part_string("DoubleBass")
    assert result == "Double Bass"


def test_format_part_string_handles_english_horn():
    """Test handles EnglishHorn special case."""
    result = format_part_string("EnglishHorn")
    assert result == "English Horn"


def test_format_part_string_handles_piccolo():
    """Test handles Piccolo special case."""
    result = format_part_string("Piccolo")
    assert result == " Piccolo"


def test_format_part_string_handles_multiple_numbers():
    """Test handles multiple numbers."""
    result = format_part_string("Violin1Part2")
    assert result == "Violin 1Part 2"
