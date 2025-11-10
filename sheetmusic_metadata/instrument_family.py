"""Instrument family mapping for tagging."""

# Mapping of base instrument names to their families
INSTRUMENT_FAMILIES: dict[str, str] = {
    "Violin": "Strings",
    "Viola": "Strings",
    "Cello": "Strings",
    "DoubleBass": "Strings",
    "Flute": "Woodwind",
    "Oboe": "Woodwind",
    "Clarinet": "Woodwind",
    "Bassoon": "Woodwind",
    "Trumpet": "Brass",
    "Horn": "Brass",
    "Trombone": "Brass",
    "Tuba": "Brass",
    "Timpani": "Percussion",
    "Percussion": "Percussion",  # For generic percussion parts
    "Harp": "Harp",
    "Piano": "Keyboard",  # For orchestral piano parts
    "Celesta": "Keyboard",
    "Organ": "Keyboard",
}


def get_instrument_family(formatted_part_string: str) -> str:
    """
    Determine the instrument family tag for a formatted part string.

    Extracts the base instrument name (first word) and looks it up in the
    instrument families mapping.

    Args:
        formatted_part_string: Formatted part name (e.g., "Violin 1")

    Returns:
        Instrument family tag (e.g., "Strings")
        Falls back to base instrument name if not found in mapping
    """
    # Extract base instrument name (first word)
    base_instrument_name = formatted_part_string.split()[0]

    # Handle special cases that might have been formatted
    if base_instrument_name == "Double":
        # Check if it's "Double Bass"
        if "Double Bass" in formatted_part_string:
            base_instrument_name = "DoubleBass"
    elif base_instrument_name == "English":
        # Check if it's "English Horn"
        if "English Horn" in formatted_part_string:
            base_instrument_name = "EnglishHorn"

    instrument_family = INSTRUMENT_FAMILIES.get(base_instrument_name)

    if instrument_family is None:
        # Fallback: use base instrument name as tag
        print(
            f"Warning: Instrument family for '{base_instrument_name}' not found "
            "in map. Using base name as tag.",
            file=__import__("sys").stderr,
        )
        instrument_family = base_instrument_name

    return instrument_family
