"""Command-line interface using Click."""

import sys
from pathlib import Path

import click

from sheetmusic_metadata.composer_lookup import ComposerLookup
from sheetmusic_metadata.formatting import (
    format_opus_string,
    format_part_string,
    format_work_title,
)
from sheetmusic_metadata.instrument_family import get_instrument_family
from sheetmusic_metadata.parsing import parse_filename
from sheetmusic_metadata.pdf_metadata import apply_pdf_metadata


def process_file(
    filepath: Path,
    composer_lookup: ComposerLookup,
    output_dir: Path | None = None,
    additional_tags: list[str] | None = None,
) -> Path:
    """
    Process a single PDF file and apply metadata.

    Args:
        filepath: Path to the PDF file
        composer_lookup: ComposerLookup instance
        output_dir: Optional directory to write output file to
        additional_tags: Optional list of additional tags to add to keywords

    Raises:
        ValueError: If filename parsing fails
        FileNotFoundError: If exiftool is not installed
        subprocess.CalledProcessError: If exiftool fails
    """
    filename = filepath.name
    print(f"Processing file: {filename}")

    try:
        components = parse_filename(filename)
    except ValueError as e:
        print(f"  Error: {e}", file=sys.stderr)
        print("  Skipping file due to parsing error.", file=sys.stderr)
        print("---")
        raise

    # Lookup composer name (use PDF-compatible format to avoid forScore splitting on commas)
    full_composer_name = composer_lookup.get_full_name_for_pdf(
        components.composer_last_name
    )

    # Format components
    formatted_work_title = format_work_title(components.work_identifier)
    formatted_part = format_part_string(components.part)
    formatted_opus = format_opus_string(components.opus)
    instrument_family_tag = get_instrument_family(formatted_part)

    # Build PDF metadata
    pdf_title = f"{formatted_work_title} - {formatted_part} Part"
    pdf_subject = "Orchestral"

    # Build keywords list
    keywords = ["Orchestral", formatted_part]
    if formatted_opus != "NoOp":
        keywords.append(formatted_opus)
    keywords.append(instrument_family_tag)
    if additional_tags:
        keywords.extend(additional_tags)
    pdf_keywords = ",".join(keywords)

    print(f"Composer: {full_composer_name}")
    print(f'Title: "{pdf_title}"')
    print(f'Keywords (Tags): "{pdf_keywords}"')

    try:
        output_path = apply_pdf_metadata(
            filepath,
            pdf_title,
            full_composer_name,
            pdf_subject,
            pdf_keywords,
            output_dir,
        )
        print("  Successfully applied metadata.")
    except Exception as e:
        print(f"  Error: Failed to apply metadata to '{filename}'.", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        print("---")
        raise

    print("---")
    return output_path


@click.command()
@click.option(
    "-i",
    "--input-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Input directory containing PDF files to process",
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help="Output directory to write processed PDF files (required when using --input-dir)",
)
@click.option(
    "-t",
    "--tag",
    "additional_tags",
    multiple=True,
    help="Add custom tags to the keywords field (can be used multiple times)",
)
@click.option(
    "--composers-csv",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to composers.csv file (defaults to composers.csv in script directory)",
)
def main(
    input_dir: Path | None,
    output_dir: Path,
    additional_tags: tuple[str, ...],
    composers_csv: Path | None,
) -> None:
    """
    Automates PDF metadata tagging via exiftool based on a filename schema.

    Schema: ComposerLastName_WorkIdentifier_Opus_Part.pdf
    Example: Dvorak_Symphony09_Op95_Violin1.pdf

    Processes all PDF files in the input directory and writes them to the output directory.
    If a file already exists in the output directory, a (1), (2), etc. suffix will be added.
    """
    # Determine composers.csv path
    if composers_csv is None:
        # Default to composers.csv in the script directory
        script_dir = Path(__file__).parent.parent
        composers_csv = script_dir / "composers.csv"

    if not composers_csv.exists():
        click.echo(
            f"Error: composers.csv not found at {composers_csv}",
            err=True,
        )
        sys.exit(1)

    # Initialize composer lookup
    try:
        composer_lookup = ComposerLookup(composers_csv)
    except Exception as e:
        click.echo(f"Error: Failed to load composers.csv: {e}", err=True)
        sys.exit(1)

    # Validate input directory
    if input_dir is None:
        click.echo(
            "Error: --input-dir is required. Use --input-dir to specify the directory containing PDF files.",
            err=True,
        )
        sys.exit(1)

    if not input_dir.is_dir():
        click.echo(
            f"Error: Input directory '{input_dir}' does not exist or is not a directory.",
            err=True,
        )
        sys.exit(1)

    # Create output directory if it doesn't exist
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        click.echo(
            f"Error: Failed to create output directory '{output_dir}': {e}", err=True
        )
        sys.exit(1)

    # Convert additional_tags tuple to list
    tags_list = list(additional_tags) if additional_tags else None

    overall_status = 0

    try:
        # Process all PDF files in input directory
        click.echo(f"Processing all PDF files in directory: {input_dir}")
        pdf_files = list(input_dir.glob("*.pdf"))
        if not pdf_files:
            click.echo(f"No PDF files found in {input_dir}")
            return

        for pdf_file in sorted(pdf_files):
            try:
                process_file(pdf_file, composer_lookup, output_dir, tags_list)
            except Exception:
                overall_status = 1
                # Early exit on error (as per requirements)
                sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    sys.exit(overall_status)


if __name__ == "__main__":
    main()
