"""Filename parsing module for extracting components from PDF filenames."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FilenameComponents:
    """Parsed components from a PDF filename."""

    composer_last_name: str
    work_identifier: str
    opus: str
    part: str


def parse_filename(filename: str) -> FilenameComponents:
    """
    Parse a PDF filename into its components.

    Supports two schemas:
    - 4-part: Composer_Work_Opus_Part.pdf
    - 3-part: Composer_Work_Part.pdf (no opus)

    Args:
        filename: The PDF filename (with or without .pdf extension)

    Returns:
        FilenameComponents with parsed values

    Raises:
        ValueError: If filename doesn't match expected schema
    """
    # Remove .pdf extension if present
    filename_no_ext = Path(filename).stem

    # Split by underscore
    parts = filename_no_ext.split("_")

    if len(parts) == 3:
        # Schema: Composer_Work_Part (no Opus)
        composer_last_name = parts[0]
        work_identifier = parts[1]
        opus = "NoOp"
        part = parts[2]
    elif len(parts) == 4:
        # Schema: Composer_Work_Opus_Part
        composer_last_name = parts[0]
        work_identifier = parts[1]
        opus = parts[2]
        part = parts[3]
    else:
        raise ValueError(
            f"Filename '{filename_no_ext}' does not match the expected schema "
            f"(3 or 4 parts). Found {len(parts)} parts."
        )

    # Basic validation: ensure essential parts are not empty
    if not composer_last_name or not work_identifier or not part:
        raise ValueError(
            f"Filename '{filename_no_ext}' is missing one of the required "
            "components (Composer, Work, Part)."
        )

    return FilenameComponents(
        composer_last_name=composer_last_name,
        work_identifier=work_identifier,
        opus=opus,
        part=part,
    )
