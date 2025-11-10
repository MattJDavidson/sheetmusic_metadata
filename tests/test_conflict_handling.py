"""Tests for file conflict handling in output directory."""

import shutil
import tempfile
from pathlib import Path

import pytest

from sheetmusic_metadata.cli import process_file
from sheetmusic_metadata.composer_lookup import ComposerLookup
from sheetmusic_metadata.pdf_metadata import _get_unique_output_path


@pytest.fixture
def composer_lookup():
    """Create a composer lookup with test data."""
    csv_path = Path(__file__).parent.parent / "composers.csv"
    if csv_path.exists():
        return ComposerLookup(csv_path)
    else:
        pytest.skip("composers.csv not found")


@pytest.fixture
def minimal_pdf():
    """Get path to minimal test PDF."""
    simple_pdf = Path(__file__).parent.parent / "tests" / "support" / "simple.pdf"
    minimal_pdf_path = (
        Path(__file__).parent.parent / "tests" / "support" / "minimal.pdf"
    )

    if simple_pdf.exists():
        return simple_pdf
    elif minimal_pdf_path.exists():
        return minimal_pdf_path
    else:
        pytest.skip("No test PDF found in tests/support/")


@pytest.mark.skipif(
    not shutil.which("exiftool"),
    reason="exiftool is not installed",
)
def test_conflict_handling_appends_suffix(minimal_pdf, composer_lookup, capsys):
    """Test that file conflicts result in (1), (2) suffixes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()
        output_dir.mkdir()

        # Copy the minimal PDF with a test filename
        test_filename = "Beethoven_Symphony05_Op67_Violin1.pdf"
        test_pdf = input_dir / test_filename
        shutil.copy2(minimal_pdf, test_pdf)

        # Process the file first time
        output_path1 = process_file(
            test_pdf, composer_lookup, output_dir=output_dir, additional_tags=None
        )
        assert output_path1.exists()
        assert output_path1.name == test_filename

        # Create a file with the same name in output (simulating a conflict)
        conflict_file = output_dir / test_filename
        conflict_file.write_bytes(b"conflict")

        # Process again - should get (1) suffix
        output_path2 = process_file(
            test_pdf, composer_lookup, output_dir=output_dir, additional_tags=None
        )
        assert output_path2.exists()
        assert output_path2.name == "Beethoven_Symphony05_Op67_Violin1 (1).pdf"

        # Verify warning was printed
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "already exists" in captured.err
        assert "(1)" in captured.err


def test_get_unique_output_path_no_conflict():
    """Test _get_unique_output_path when no conflict exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        filename = "test.pdf"

        path, was_conflict = _get_unique_output_path(output_dir, filename)

        assert path.name == filename
        assert was_conflict is False


def test_get_unique_output_path_with_conflict():
    """Test _get_unique_output_path when conflict exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        filename = "test.pdf"

        # Create existing file
        existing_file = output_dir / filename
        existing_file.write_text("existing")

        # Get unique path
        path1, was_conflict1 = _get_unique_output_path(output_dir, filename)
        assert path1.name == "test (1).pdf"
        assert was_conflict1 is True

        # Create that file too
        path1.write_text("conflict1")

        # Get next unique path
        path2, was_conflict2 = _get_unique_output_path(output_dir, filename)
        assert path2.name == "test (2).pdf"
        assert was_conflict2 is True


@pytest.mark.skipif(
    not shutil.which("exiftool"),
    reason="exiftool is not installed",
)
def test_output_directory_created_if_not_exists(minimal_pdf, composer_lookup):
    """Test that output directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        input_dir = tmp_path / "input"
        # Create nested output directory that doesn't exist yet
        output_dir = tmp_path / "nonexistent" / "output" / "dir"
        input_dir.mkdir()

        # Verify output directory doesn't exist
        assert not output_dir.exists()

        # Copy the minimal PDF with a test filename
        test_filename = "Beethoven_Symphony05_Op67_Violin1.pdf"
        test_pdf = input_dir / test_filename
        shutil.copy2(minimal_pdf, test_pdf)

        # Process the file - should create output directory
        output_path = process_file(
            test_pdf, composer_lookup, output_dir=output_dir, additional_tags=None
        )

        # Verify output directory was created
        assert output_dir.exists()
        assert output_dir.is_dir()
        # Verify file was written
        assert output_path.exists()
