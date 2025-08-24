import csv
import re
from pathlib import Path

from pydantic import BaseModel


class Composer(BaseModel):
    full_name: str


class SheetMusic(BaseModel):
    composer: Composer
    work_identifier: str
    opus: str | None = None
    part: str
    filename: str

    @property
    def title(self) -> str:
        return f"{self.work_title} - {self.formatted_part} Part"

    @property
    def work_title(self) -> str:
        with_spaces = re.sub(r"([a-z])([A-Z])", r"\1 \2", self.work_identifier)
        with_spaces = re.sub(r"([A-Za-z])([0-9]+)", r"\1 \2", with_spaces)
        return re.sub(r" ([0-9])$", r" 0\1", with_spaces)

    @property
    def formatted_part(self) -> str:
        return re.sub(r"([A-Za-z]+)([0-9]+)", r"\1 \2", self.part)

    @property
    def formatted_opus(self) -> str | None:
        if self.opus:
            return re.sub(r"Op([0-9]+)", r"Op. \1", self.opus)
        return None


def get_full_composer_name(
    composer_last_name: str, composer_csv_path: Path
) -> Composer:
    with open(composer_csv_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            simple_surname, full_name = row
            if simple_surname == composer_last_name:
                return Composer(full_name=full_name)
    return Composer(full_name=composer_last_name.capitalize())


INSTRUMENT_FAMILIES = {
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
    "Percussion": "Percussion",
    "Harp": "Harp",
    "Piano": "Keyboard",
    "Celesta": "Keyboard",
    "Organ": "Keyboard",
}


def get_instrument_family(part: str) -> str:
    base_instrument_name = part.split(" ")[0]
    return INSTRUMENT_FAMILIES.get(base_instrument_name, base_instrument_name)


def apply_pdf_metadata(
    filepath: Path,
    title: str,
    author: str,
    subject: str,
    keywords: list[str],
    output_dir: Path | None,
) -> bool:
    import subprocess

    exiftool_args = [
        "exiftool",
        f"-Title={title}",
        f"-Author={author}",
        f"-Subject={subject}",
        f"-Keywords={",".join(keywords)}",
        "-e",
    ]

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        exiftool_args.extend(["-o", str(output_dir / f"{filepath.name}.%e")])
    else:
        exiftool_args.append("-overwrite_original")

    exiftool_args.append(str(filepath))

    try:
        subprocess.run(exiftool_args, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def parse_filename(filename: str, composer_csv_path: Path) -> SheetMusic | None:
    filename_no_ext = Path(filename).stem
    parts = filename_no_ext.split("_")

    if len(parts) == 3:
        composer_last_name, work_identifier, part = parts
        opus = None
    elif len(parts) == 4:
        composer_last_name, work_identifier, opus, part = parts
    else:
        return None

    composer = get_full_composer_name(composer_last_name, composer_csv_path)

    return SheetMusic(
        composer=composer,
        work_identifier=work_identifier,
        opus=opus,
        part=part,
        filename=filename,
    )
