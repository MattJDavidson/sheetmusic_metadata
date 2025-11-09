"""Integration tests for PDF metadata writing using exiftool."""

import shutil
import tempfile
from pathlib import Path

import pytest

from sheetmusic_metadata.cli import process_file
from sheetmusic_metadata.composer_lookup import ComposerLookup
from sheetmusic_metadata.pdf_metadata import read_pdf_metadata


@pytest.fixture
def minimal_pdf():
    """Get path to minimal test PDF."""
    # Try simple.pdf first (downloaded valid PDF), fallback to minimal.pdf
    simple_pdf = Path(__file__).parent.parent / "tests" / "support" / "simple.pdf"
    minimal_pdf_path = Path(__file__).parent.parent / "tests" / "support" / "minimal.pdf"
    
    if simple_pdf.exists():
        return simple_pdf
    elif minimal_pdf_path.exists():
        return minimal_pdf_path
    else:
        pytest.skip("No test PDF found in tests/support/")


@pytest.fixture
def composer_lookup():
    """Create a composer lookup with test data."""
    csv_path = Path(__file__).parent.parent / "composers.csv"
    if csv_path.exists():
        return ComposerLookup(csv_path)
    else:
        pytest.skip("composers.csv not found")


@pytest.mark.skipif(
    not shutil.which("exiftool"),
    reason="exiftool is not installed",
)
def test_pdf_metadata_writing_overwrite_original(minimal_pdf, composer_lookup):
    """Test that metadata is correctly written to PDF and can be read back."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Copy the minimal PDF with a test filename
        test_filename = "Beethoven_Symphony05_Op67_Violin1.pdf"
        test_pdf = tmp_path / test_filename
        shutil.copy2(minimal_pdf, test_pdf)

        # Process the file (this will overwrite the original)
        process_file(test_pdf, composer_lookup, output_dir=None, additional_tags=None)

        # Read back the metadata using exiftool
        metadata = read_pdf_metadata(test_pdf)

        # Verify the metadata was written correctly
        assert metadata["Title"] == "Symphony 05 - Violin 1 Part"
        assert metadata["Author"] == "Beethoven, Ludwig van"
        assert metadata["Subject"] == "Orchestral"
        assert "Orchestral" in metadata["Keywords"]
        assert "Violin 1" in metadata["Keywords"]
        assert "Op. 67" in metadata["Keywords"]
        assert "Strings" in metadata["Keywords"]


@pytest.mark.skipif(
    not shutil.which("exiftool"),
    reason="exiftool is not installed",
)
def test_pdf_metadata_writing_output_directory(minimal_pdf, composer_lookup):
    """Test that metadata is correctly written to PDF in output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()
        output_dir.mkdir()

        # Copy the minimal PDF with a test filename
        test_filename = "Dvorak_Symphony09_Op95_Cello.pdf"
        test_pdf = input_dir / test_filename
        shutil.copy2(minimal_pdf, test_pdf)

        # Process the file (this will write to output directory)
        process_file(
            test_pdf, composer_lookup, output_dir=output_dir, additional_tags=None
        )

        # Check that output file was created
        output_pdf = output_dir / test_filename
        assert output_pdf.exists()

        # Read back the metadata using exiftool
        metadata = read_pdf_metadata(output_pdf)

        # Verify the metadata was written correctly
        assert metadata["Title"] == "Symphony 09 - Cello Part"
        assert metadata["Author"] == "Dvořák, Antonín"
        assert metadata["Subject"] == "Orchestral"
        assert "Orchestral" in metadata["Keywords"]
        assert "Cello" in metadata["Keywords"]
        assert "Op. 95" in metadata["Keywords"]
        assert "Strings" in metadata["Keywords"]

        # Verify original file still exists and wasn't modified
        assert test_pdf.exists()


@pytest.mark.skipif(
    not shutil.which("exiftool"),
    reason="exiftool is not installed",
)
def test_pdf_metadata_writing_with_custom_tags(minimal_pdf, composer_lookup):
    """Test that custom tags are included in keywords."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Copy the minimal PDF with a test filename
        test_filename = "Brahms_Symphony04_Op98_Oboe2.pdf"
        test_pdf = tmp_path / test_filename
        shutil.copy2(minimal_pdf, test_pdf)

        # Process the file with custom tags
        custom_tags = ["Chamber Music", "2024 Season"]
        process_file(
            test_pdf, composer_lookup, output_dir=None, additional_tags=custom_tags
        )

        # Read back the metadata using exiftool
        metadata = read_pdf_metadata(test_pdf)

        # Verify the metadata was written correctly
        assert metadata["Title"] == "Symphony 04 - Oboe 2 Part"
        assert metadata["Author"] == "Brahms, Johannes"
        assert metadata["Subject"] == "Orchestral"
        keywords = metadata["Keywords"]
        assert "Orchestral" in keywords
        assert "Oboe 2" in keywords
        assert "Op. 98" in keywords
        assert "Woodwind" in keywords
        assert "Chamber Music" in keywords
        assert "2024 Season" in keywords


@pytest.mark.skipif(
    not shutil.which("exiftool"),
    reason="exiftool is not installed",
)
def test_pdf_metadata_writing_3_part_schema(minimal_pdf, composer_lookup):
    """Test metadata writing with 3-part schema (no opus)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Copy the minimal PDF with a test filename (3-part schema)
        test_filename = "VaughanWilliams_LarkAscending_Viola.pdf"
        test_pdf = tmp_path / test_filename
        shutil.copy2(minimal_pdf, test_pdf)

        # Process the file
        process_file(test_pdf, composer_lookup, output_dir=None, additional_tags=None)

        # Read back the metadata using exiftool
        metadata = read_pdf_metadata(test_pdf)

        # Verify the metadata was written correctly
        assert metadata["Title"] == "Lark Ascending - Viola Part"
        assert metadata["Author"] == "Vaughan Williams, Ralph"
        assert metadata["Subject"] == "Orchestral"
        keywords = metadata["Keywords"]
        assert "Orchestral" in keywords
        assert "Viola" in keywords
        assert "Strings" in keywords
        # Opus should not be in keywords for 3-part schema
        assert "Op." not in keywords
