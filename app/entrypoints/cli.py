from pathlib import Path

import click
from rich import print

from app.metadata import apply_pdf_metadata, get_instrument_family, parse_filename


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-o", "--output-dir", type=click.Path(), help="Directory to save the new file."
)
@click.option(
    "-t",
    "--tag",
    "additional_tags",
    multiple=True,
    help="Additional tags to add to the PDF keywords.",
)
def process(path: str, output_dir: str | None, additional_tags: tuple[str, ...]):
    """Processes a single file or a directory of PDF files."""
    input_path = Path(path)
    composer_csv_path = Path(__file__).parent.parent.parent / "composers.csv"

    if input_path.is_file():
        files_to_process = [input_path]
    else:
        files_to_process = list(input_path.glob("*.pdf"))

    for file in files_to_process:
        print(f"Processing file: {file.name}")
        sheet_music = parse_filename(file.name, composer_csv_path)

        if sheet_music:
            print(f"  Composer: {sheet_music.composer.full_name}")
            print(f'  Title: "{sheet_music.title}"')
            keywords = [
                "Orchestral",
                sheet_music.formatted_part,
                get_instrument_family(sheet_music.formatted_part),
                *additional_tags,
            ]
            if sheet_music.formatted_opus:
                keywords.append(sheet_music.formatted_opus)

            print(f"  Keywords (Tags): {keywords}")

            if apply_pdf_metadata(
                file,
                sheet_music.title,
                sheet_music.composer.full_name,
                "Orchestral",
                keywords,
                Path(output_dir) if output_dir else None,
            ):
                print("  Successfully applied metadata.")
            else:
                print("  Error: Failed to apply metadata.")
        else:
            print("  Skipping file due to parsing error.")


if __name__ == "__main__":
    cli()
