# Sheet Music PDF Metadata Tagger

A Python tool that automates the process of tagging PDF sheet music files with correct metadata for use in [forScore](https://forscore.co/). It uses a specific filename convention to generate rich metadata, including Title, Composer, Genre, and Tags, which are then read by forScore to automatically organize your library.

## Features

- **Automatic metadata generation** from filenames following a consistent schema
- **Composer name lookup** from CSV database with Unicode support
- **forScore-compatible formatting** - names formatted correctly to avoid splitting issues
- **Instrument family tagging** for automatic categorization
- **Parallel test execution** for faster development
- **Pre-commit hooks** for code quality

## Filename Convention

The tool relies on a strict, underscore-separated filename schema to parse information. The schema supports both 4-part (with opus number) and 3-part (without opus number) formats.

**Schema:** `ComposerLastName_WorkIdentifier_OpusOrPart_Part.pdf`

### Components

1.  **`ComposerLastName`**: The last name of the composer (e.g., `Beethoven`, `RimskyKorsakov`, `VaughanWilliams`). Must match an entry in `composers.csv`.
2.  **`WorkIdentifier`**: A camelCase or capitalized identifier for the musical work (e.g., `Symphony05`, `Scheherazade`, `LarkAscending`). The tool automatically formats this into a readable title.
3.  **`Opus` (Optional)**: The opus or catalog number (e.g., `Op67`, `Op35`). If the work has no opus number, this field should be omitted.
4.  **`Part`**: The instrument part (e.g., `Violin1`, `Flute2`, `Viola`).

### Examples

-   **4-Part (with Opus):** `Beethoven_Symphony05_Op67_Violin1.pdf`
-   **3-Part (no Opus):** `VaughanWilliams_LarkAscending_Viola.pdf`

## How it Works: forScore Integration

The tool uses `exiftool` to write to standard PDF metadata fields. forScore reads these fields upon import to categorize your scores automatically. The mapping is based on the official [forScore PDF Metadata specification](https://forscore.co/developers-pdf-metadata/).

-   **PDF Title** is constructed as `Work Title - Part Name Part`.
-   **PDF Author** is set to the composer's full name in "FirstName Surname" format (forScore sorts by the last word, so this ensures proper sorting by surname).
-   **PDF Subject** is set to "Orchestral".
-   **PDF Keywords** include the part name, opus number, and instrument family (e.g., "Strings", "Woodwind").

### Important: forScore Comma Handling

forScore splits the Author field on commas, treating each part as a separate composer. To prevent this, the tool formats composer names as "FirstName Surname" (space-separated) instead of "Surname, FirstName". This ensures:
- Names appear as single entries in forScore
- Proper sorting by surname (forScore sorts by the last word)
- No duplicate composer entries

### Enabling Automatic Metadata Fetching in forScore

To get the most out of this tool, it is recommended to enable "automatic fetching for new files" in forScore's settings panel. This feature allows forScore to automatically read the PDF metadata and categorize your files upon import.

For more details, please see the official [forScore documentation on metadata fetching](https://forscore.co/kb/fetching-pdf-metadata/).

## Recommended Folder Structure

While not required for the tool to function, organizing your sheet music into a consistent folder structure is highly recommended for both manual browsing and automated processing. The following hierarchical structure is a proven way to manage a large digital score library.

**`MySheetMusic/[Instrument]/[Category]/[Composer_LastName]/[Filename].pdf`**

### Structure Breakdown

-   **`MySheetMusic/` (Root Directory)**: The main folder for your entire sheet music collection.
-   **`[Instrument]/`**: The first level organizes music by the primary instrument.
    -   *Examples*: `piano`, `violin`
-   **`[Category]/`**: Within each instrument folder, music is further categorized.
    -   *Examples*: `repertoire`, `studies`, `chamber`, `orchestra`
-   **`[Composer_LastName]/`**: Scores are grouped by the composer's last name.
    -   *Examples*: `Beethoven`, `Czerny`, `Dvorak`
-   **`[Filename].pdf`**: The individual PDF file, named according to the tool's convention.

### Examples

**Violin**
-   **Repertoire:** `MySheetMusic/violin/repertoire/Bach/Bach_SonataNo1_BWV1001_Violin.pdf`
-   **Chamber:** `MySheetMusic/violin/chamber/Beethoven/Beethoven_StringQuartet_Op18No4_Violin1.pdf`
-   **Orchestra:** `MySheetMusic/violin/orchestra/Dvorak/Dvorak_Symphony09_Op95_Violin1.pdf`
-   **Studies:** `MySheetMusic/violin/studies/Kreutzer/Kreutzer_42Studies_Violin.pdf`

**Piano**
-   **Repertoire:** `MySheetMusic/piano/repertoire/Chopin/Chopin_BalladeNo1_Op23_Piano.pdf`
-   **Chamber:** `MySheetMusic/piano/chamber/Schubert/Schubert_PianoTrio_Op99_Piano.pdf`
-   **Orchestra:** `MySheetMusic/piano/orchestra/Stravinsky/Stravinsky_Petrushka_Piano.pdf`
-   **Studies:** `MySheetMusic/piano/studies/Czerny/Czerny_ArtOfFingerDexterity_Op740_No1_Piano.pdf`

## Installation

### Requirements

- **Python 3.13+**
- **exiftool** - For reading/writing PDF metadata
- **uv** - Fast Python package installer (recommended) or pip

### Installing Dependencies

**macOS (with Homebrew):**
```bash
brew install exiftool
```

**Other Systems:**
Please see the official [ExifTool installation instructions](https://exiftool.org/install.html).

### Installing the Tool

**Using uv (recommended):**
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the tool
uv pip install git+https://github.com/yourusername/sheetmusic-metadata.git
```

**Using pip:**
```bash
pip install git+https://github.com/yourusername/sheetmusic-metadata.git
```

## Usage

### Basic Usage

Process all PDF files in a directory:

```bash
sheetmusic-metadata --input-dir /path/to/pdfs --output-dir /path/to/output
```

### Command-Line Options

- `-i, --input-dir`: Input directory containing PDF files to process (required)
- `-o, --output-dir`: Output directory to write processed PDF files (required)
- `-t, --tag`: Add custom tags to keywords (can be used multiple times)
- `--composers-csv`: Path to composers.csv file (defaults to composers.csv in package directory)

### Examples

**Process files with custom tags:**
```bash
sheetmusic-metadata \
  --input-dir ./my-scores \
  --output-dir ./tagged-scores \
  --tag "2024 Season" \
  --tag "Chamber Music"
```

**Use custom composers CSV:**
```bash
sheetmusic-metadata \
  --input-dir ./my-scores \
  --output-dir ./tagged-scores \
  --composers-csv /path/to/custom-composers.csv
```

### Using Taskfile (Development)

If you're working with the source code, you can use the Taskfile:

```bash
# Install dependencies
task install-dev

# Run the tool
task run -- --input-dir ./my-scores --output-dir ./tagged-scores
```

## Composer Database

The tool uses `composers.csv` to map composer surnames (as they appear in filenames) to full composer names. The CSV format is:

```csv
simple_surname,full_name
Beethoven,"Beethoven, Ludwig van"
Dvorak,"Dvo??k, Anton?n"
Sibelius,"Sibelius, Jean"
```

- **`simple_surname`**: The surname as it appears in filenames (e.g., `Dvorak`, `RimskyKorsakov`)
- **`full_name`**: Full name in "Surname, FirstName" format (will be converted to "FirstName Surname" for PDF metadata)

The tool handles:
- Unicode characters (e.g., Dvo??k, Sibelius)
- Duplicate surnames (prefers more specific/complex names)
- Case-insensitive matching
- Fallback to capitalized surname if not found

## Important Note: Back Up Your Library

It is strongly recommended to back up your forScore library regularly. While this tool is designed to be safe, creating backups protects your data from accidental loss.

## Development

This project uses [Taskfile](https://taskfile.dev/) for development task automation and [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Developer Setup

To set up the development environment:

```bash
# Install development dependencies and pre-commit hooks
task install-dev
```

This will:
- Install all development dependencies (pytest, ruff, pre-commit, etc.)
- Set up pre-commit hooks for code quality
- Install system dependencies (exiftool, uv) if needed

### Available Tasks

```bash
# Run all tests in parallel
task test

# Run tests serially (for debugging)
task test-serial

# Run only unit tests
task test-unit

# Run only integration tests (requires exiftool)
task test-integration

# Run linters
task lint

# Clean build artifacts and cache files
task clean

# Install for end users (production dependencies only)
task install

# Install for developers (with dev dependencies)
task install-dev
```

### Running Tests

The test suite uses pytest with pytest-xdist for parallel execution:

```bash
# Run all tests in parallel (default)
task test

# Run tests serially
task test-serial

# Run with coverage
uv run pytest --cov=sheetmusic_metadata tests/
```

### Code Quality

The project uses:
- **ruff** for linting and formatting
- **pre-commit** hooks for automatic checks
- **pytest** for testing with parallel execution

Run linting:
```bash
task lint
```

Pre-commit hooks run automatically on `git commit`. To run manually:
```bash
uv run pre-commit run --all-files
```

## Recent Fixes

- **forScore comma splitting fix**: Composer names are now formatted as "FirstName Surname" to prevent forScore from splitting on commas
- **Duplicate composer warnings**: Warnings now only appear when duplicate composers are actually used during processing
- **Unicode support**: Full support for accented characters in composer names
- **Parallel test execution**: Tests run faster with pytest-xdist

## Support

This tool is provided as-is. For help with understanding, modifying, or extending the tool's functionality, please consult the code documentation or open an issue on GitHub.

## Contributing

Contributions are welcome! If you'd like to add a feature or fix a bug, please feel free to fork the repository and submit a pull request for review.

### Adding Composers

To add composers to the database, edit `composers.csv` following the existing format:

```csv
simple_surname,full_name
NewComposer,"NewComposer, First Name"
```

## License and Code of Conduct

This project is licensed under the terms of the `LICENSE` file.

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
