# Sheet Music PDF Metadata Tagger

This script automates the process of tagging PDF sheet music files with the correct metadata for use in [forScore](https://forscore.co/). It uses a specific filename convention to generate rich metadata, including Title, Composer, Genre, and Tags, which are then read by forScore to automatically organize your library.

## Filename Convention

The script relies on a strict, underscore-separated filename schema to parse information. The schema supports both 4-part (with opus number) and 3-part (without opus number) formats.

**Schema:** `ComposerLastName_WorkIdentifier_OpusOrPart_Part.pdf`

### Components

1.  **`ComposerLastName`**: The last name of the composer (e.g., `Beethoven`, `Rimsky-Korsakov`, `VaughanWilliams`).
2.  **`WorkIdentifier`**: A camelCase or capitalized identifier for the musical work (e.g., `Symphony05`, `Scheherazade`, `LarkAscending`). The script automatically formats this into a readable title.
3.  **`Opus` (Optional)**: The opus or catalog number (e.g., `Op67`, `Op35`). If the work has no opus number, this field should be omitted.
4.  **`Part`**: The instrument part (e.g., `Violin1`, `Flute2`, `Viola`).

### Examples

-   **4-Part (with Opus):** `Beethoven_Symphony05_Op67_Violin1.pdf`
-   **3-Part (no Opus):** `VaughanWilliams_LarkAscending_Viola.pdf`

## How it Works: forScore Integration

The script uses `exiftool` to write to standard PDF metadata fields. forScore reads these fields upon import to categorize your scores automatically. The mapping is based on the official [forScore PDF Metadata specification](https://forscore.co/developers-pdf-metadata/).

-   **PDF Title** is constructed as `Work Title - Part Name`.
-   **PDF Author** is set to the composer's full name (looked up from `composers.csv`).
-   **PDF Subject** is set to a default value (e.g., "Orchestral").
-   **PDF Keywords** include the part name, opus number, and instrument family (e.g., "Strings", "Woodwind").

### Enabling Automatic Metadata Fetching in forScore

To get the most out of this script, it is recommended to enable "automatic fetching for new files" in forScore's settings panel. This feature allows forScore to automatically read the PDF metadata and categorize your files upon import.

For more details, please see the official [forScore documentation on metadata fetching](https://forscore.co/kb/fetching-pdf-metadata/).

## Installation

The only external dependency required to run this script is `exiftool`.

- **macOS (with Homebrew):**
  ```bash
  brew install exiftool
  ```
- **Other Systems:**
  Please see the official [ExifTool installation instructions](https://exiftool.org/install.html).

This project uses Python 3.13 and [`Taskfile`](https://taskfile.dev/) for dependency management and task running.

1.  **Install `Taskfile`:**
    Follow the [official installation instructions](https://taskfile.dev/installation/).

2.  **Install dependencies:**
    ```bash
    task install-dev
    ```

## Usage

Once the dependencies are installed, you can run the script using `task`.

1.  **Run on a single PDF file:**
    ```bash
    task run -- process /path/to/your/file.pdf
    ```
2.  **Run on all PDFs in a directory:**
    ```bash
    task run -- process /path/to/your/pdfs/
    ```

## Important Note: Back Up Your Library

It is strongly recommended to back up your forScore library regularly. While this script is designed to be safe, creating backups protects your data from accidental loss.

## Development

This project uses `pytest` for testing, which can be run via `task`.

### Running Tests

To run the full suite of unit tests, use the `task test` command:

```bash
task test
```

## Contributing

Contributions are welcome! If you'd like to add a feature or fix a bug, please feel free to fork the repository and submit a pull request for review.

## License and Code of Conduct

This project is licensed under the terms of the `LICENSE` file.

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
