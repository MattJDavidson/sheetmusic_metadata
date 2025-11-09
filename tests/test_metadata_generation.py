"""Integration tests for full metadata generation."""

import tempfile
from pathlib import Path

import pytest

from sheetmusic_metadata.composer_lookup import ComposerLookup
from sheetmusic_metadata.formatting import (
    format_opus_string,
    format_part_string,
    format_work_title,
)
from sheetmusic_metadata.instrument_family import get_instrument_family
from sheetmusic_metadata.parsing import parse_filename


@pytest.fixture
def composer_lookup():
    """Create a composer lookup with test data."""
    # Use the actual composers.csv from the project
    csv_path = Path(__file__).parent.parent / "composers.csv"
    if csv_path.exists():
        return ComposerLookup(csv_path)
    else:
        # Fallback: create a minimal test CSV
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            csv_content = """simple_surname,full_name
Beethoven,"Beethoven, Ludwig van"
Dvorak,"Dvořák, Antonín"
Tchaikovsky,"Tchaikovsky, Pyotr Ilyich"
Brahms,"Brahms, Johannes"
Sibelius,"Sibelius, Jean"
"""
            f.write(csv_content)
            f.flush()
            return ComposerLookup(Path(f.name))


def run_metadata_generation_test(
    filename: str,
    expected_composer: str,
    expected_title: str,
    expected_keywords: str,
    composer_lookup: ComposerLookup,
):
    """Helper function to test full metadata generation."""
    components = parse_filename(filename)

    actual_composer = composer_lookup.get_full_name(components.composer_last_name)

    formatted_work = format_work_title(components.work_identifier)
    formatted_part = format_part_string(components.part)
    actual_title = f"{formatted_work} - {formatted_part} Part"

    formatted_opus = format_opus_string(components.opus)
    instrument_family = get_instrument_family(formatted_part)

    all_keywords = ["Orchestral", formatted_part]
    if formatted_opus != "NoOp":
        all_keywords.append(formatted_opus)
    all_keywords.append(instrument_family)
    actual_keywords = ",".join(all_keywords)

    assert actual_composer == expected_composer
    assert actual_title == expected_title
    assert actual_keywords == expected_keywords


def test_metadata_generation_beethoven_symphony_5(composer_lookup):
    """Test metadata generation: Beethoven Symphony 5."""
    run_metadata_generation_test(
        "Beethoven_Symphony05_Op67_Violin1.pdf",
        "Beethoven, Ludwig van",
        "Symphony 05 - Violin 1 Part",
        "Orchestral,Violin 1,Op. 67,Strings",
        composer_lookup,
    )


def test_metadata_generation_dvorak_symphony_9(composer_lookup):
    """Test metadata generation: Dvo??k Symphony 9."""
    run_metadata_generation_test(
        "Dvorak_Symphony09_Op95_Cello.pdf",
        "Dvořák, Antonín",
        "Symphony 09 - Cello Part",
        "Orchestral,Cello,Op. 95,Strings",
        composer_lookup,
    )


def test_metadata_generation_tchaikovsky_symphony_6(composer_lookup):
    """Test metadata generation: Tchaikovsky Symphony 6."""
    run_metadata_generation_test(
        "Tchaikovsky_Symphony06_Op74_Clarinet1.pdf",
        "Tchaikovsky, Pyotr Ilyich",
        "Symphony 06 - Clarinet 1 Part",
        "Orchestral,Clarinet 1,Op. 74,Woodwind",
        composer_lookup,
    )


def test_metadata_generation_brahms_symphony_4(composer_lookup):
    """Test metadata generation: Brahms Symphony 4."""
    run_metadata_generation_test(
        "Brahms_Symphony04_Op98_Oboe2.pdf",
        "Brahms, Johannes",
        "Symphony 04 - Oboe 2 Part",
        "Orchestral,Oboe 2,Op. 98,Woodwind",
        composer_lookup,
    )


def test_metadata_generation_sibelius_violin_concerto(composer_lookup):
    """Test metadata generation: Sibelius Violin Concerto."""
    run_metadata_generation_test(
        "Sibelius_ViolinConcerto_Op47_Trumpet1.pdf",
        "Sibelius, Jean",
        "Violin Concerto - Trumpet 1 Part",
        "Orchestral,Trumpet 1,Op. 47,Brass",
        composer_lookup,
    )
