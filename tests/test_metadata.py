from pathlib import Path

import pytest

from app.metadata import (
    Composer,
    SheetMusic,
    get_full_composer_name,
    get_instrument_family,
    parse_filename,
)


@pytest.fixture
def composer_csv_path() -> Path:
    return Path(__file__).parent.parent / "composers.csv"


def test_get_full_composer_name(composer_csv_path: Path):
    assert (
        get_full_composer_name("Bach", composer_csv_path).full_name
        == "Bach, Johann Sebastian"
    )
    assert (
        get_full_composer_name("Beethoven", composer_csv_path).full_name
        == "Beethoven, Ludwig van"
    )
    assert (
        get_full_composer_name("UnknownComposer", composer_csv_path).full_name
        == "Unknowncomposer"
    )


def test_sheet_music_properties():
    composer = Composer(full_name="Beethoven, Ludwig van")
    sheet_music = SheetMusic(
        composer=composer,
        work_identifier="Symphony05",
        opus="Op67",
        part="Violin1",
        filename="Beethoven_Symphony05_Op67_Violin1.pdf",
    )
    assert sheet_music.work_title == "Symphony 05"
    assert sheet_music.formatted_opus == "Op. 67"
    assert sheet_music.formatted_part == "Violin 1"
    assert sheet_music.title == "Symphony 05 - Violin 1 Part"


def test_get_instrument_family():
    assert get_instrument_family("Violin 1") == "Strings"
    assert get_instrument_family("Flute 2") == "Woodwind"
    assert get_instrument_family("UnknownInstrument") == "UnknownInstrument"


def test_parse_filename(composer_csv_path: Path):
    sheet_music = parse_filename(
        "Beethoven_Symphony05_Op67_Violin1.pdf", composer_csv_path
    )
    assert sheet_music is not None
    assert sheet_music.composer.full_name == "Beethoven, Ludwig van"
    assert sheet_music.work_identifier == "Symphony05"
    assert sheet_music.opus == "Op67"
    assert sheet_music.part == "Violin1"

    sheet_music = parse_filename(
        "VaughanWilliams_LarkAscending_Viola.pdf", composer_csv_path
    )
    assert sheet_music is not None
    assert sheet_music.composer.full_name == "Vaughan Williams, Ralph"
    assert sheet_music.work_identifier == "LarkAscending"
    assert sheet_music.opus is None
    assert sheet_music.part == "Viola"
