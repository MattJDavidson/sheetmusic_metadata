"""Tests for formatting functions."""

import pytest

from sheetmusic_metadata.formatting import (
    format_opus_string,
    format_part_string,
    format_work_title,
)


@pytest.mark.parametrize(
    "input_title,expected_output",
    [
        ("Symphony5", "Symphony 05"),  # Adds leading zero to single digit
        ("Symphony09", "Symphony 09"),  # Preserves double digit
        ("ViolinConcerto", "Violin Concerto"),  # Adds space for camelCase
        ("ViolinConcertoNo1", "Violin Concerto No 01"),  # Handles multiple camelCase
    ],
)
def test_format_work_title(input_title, expected_output):
    """Test work title formatting with various inputs."""
    result = format_work_title(input_title)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_opus,expected_output",
    [
        ("Op1", "Op. 1"),  # Single digit opus
        ("Op67", "Op. 67"),  # Double digit opus
        ("NoOp", "NoOp"),  # No opus
    ],
)
def test_format_opus_string(input_opus, expected_output):
    """Test opus string formatting with various inputs."""
    result = format_opus_string(input_opus)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_part,expected_output",
    [
        ("Violin1", "Violin 1"),  # Adds space before numbers
        ("DoubleBass", "Double Bass"),  # Special case: DoubleBass
        ("EnglishHorn", "English Horn"),  # Special case: EnglishHorn
        ("Piccolo", " Piccolo"),  # Special case: Piccolo (leading space)
        ("Violin1Part2", "Violin 1Part 2"),  # Multiple numbers
    ],
)
def test_format_part_string(input_part, expected_output):
    """Test part string formatting with various inputs."""
    result = format_part_string(input_part)
    assert result == expected_output
