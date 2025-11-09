"""Formatting functions for work titles, part names, and opus numbers."""

import re


def format_work_title(work_identifier: str) -> str:
    """
    Format work identifier into a readable title.

    Applies:
    1. CamelCase spacing (adds spaces before capital letters)
    2. Number spacing (adds spaces before numbers)
    3. Single-digit padding (pads single-digit numbers with leading zero)

    Args:
        work_identifier: Raw work identifier from filename (e.g., "Symphony05")

    Returns:
        Formatted work title (e.g., "Symphony 05")
    """
    # Add space for camelCase: ([a-z])([A-Z]) -> \1 \2
    with_spaces = re.sub(r"([a-z])([A-Z])", r"\1 \2", work_identifier)

    # Add space before numbers: ([A-Za-z])([0-9]+) -> \1 \2
    with_spaces = re.sub(r"([A-Za-z])([0-9]+)", r"\1 \2", with_spaces)

    # Pad single-digit numbers with leading zero:  ([0-9])$ ->  0\1
    formatted = re.sub(r" ([0-9])$", r" 0\1", with_spaces)

    return formatted


def format_part_string(raw_part: str) -> str:
    """
    Format raw part string for display and tagging.

    Handles:
    - Adding spaces between instrument names and numbers (e.g., "Violin1" -> "Violin 1")
    - Special compound names: "DoubleBass" -> "Double Bass", "EnglishHorn" -> "English Horn"
    - Piccolo special case: "Piccolo" -> " Piccolo" (adds leading space)

    Args:
        raw_part: Raw part identifier from filename (e.g., "Violin1")

    Returns:
        Formatted part name (e.g., "Violin 1")
    """
    # Add space before numbers: ([A-Za-z]+)([0-9]+) -> \1 \2
    formatted = re.sub(r"([A-Za-z]+)([0-9]+)", r"\1 \2", raw_part)

    # Handle special compound names
    formatted = formatted.replace("DoubleBass", "Double Bass")
    formatted = formatted.replace("EnglishHorn", "English Horn")

    # Piccolo special case: add leading space
    formatted = formatted.replace("Piccolo", " Piccolo")

    return formatted


def format_opus_string(raw_opus: str) -> str:
    """
    Format opus number string.

    Converts "Op67" -> "Op. 67" (adds period and space after "Op").

    Args:
        raw_opus: Raw opus identifier from filename (e.g., "Op67")

    Returns:
        Formatted opus string (e.g., "Op. 67")
        Returns "NoOp" unchanged if opus is "NoOp"
    """
    if raw_opus == "NoOp":
        return raw_opus

    # Format: Op([0-9]+) -> Op. \1
    formatted = re.sub(r"Op([0-9]+)", r"Op. \1", raw_opus)

    return formatted
