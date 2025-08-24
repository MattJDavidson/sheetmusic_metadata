from pathlib import Path

import pytest
from click.testing import CliRunner

from app.entrypoints.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_process_file(runner: CliRunner, tmp_path: Path):
    test_file = tmp_path / "Beethoven_Symphony05_Op67_Violin1.pdf"
    test_file.touch()

    result = runner.invoke(cli, ["process", str(test_file)])
    assert result.exit_code == 0
    assert "Processing file: Beethoven_Symphony05_Op67_Violin1.pdf" in result.output
    assert "Composer: Beethoven, Ludwig van" in result.output
    assert 'Title: "Symphony 05 - Violin 1 Part"' in result.output


def test_process_directory(runner: CliRunner, tmp_path: Path):
    (tmp_path / "Beethoven_Symphony05_Op67_Violin1.pdf").touch()
    (tmp_path / "Mozart_Symphony40_K550_Violin1.pdf").touch()

    result = runner.invoke(cli, ["process", str(tmp_path)])
    assert result.exit_code == 0
    assert "Processing file: Beethoven_Symphony05_Op67_Violin1.pdf" in result.output
    assert "Processing file: Mozart_Symphony40_K550_Violin1.pdf" in result.output
