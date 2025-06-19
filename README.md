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
-   **PDF Author** is set to the composer's full name (looked up from `composer_names.sh`).
-   **PDF Subject** is set to a default value (e.g., "Orchestral").
-   **PDF Keywords** include the part name, opus number, and instrument family (e.g., "Strings", "Woodwind").

### Enabling Automatic Metadata Fetching in forScore

To get the most out of this script, it is recommended to enable "automatic fetching for new files" in forScore's settings panel. This feature allows forScore to automatically read the PDF metadata and categorize your files upon import.

For more details, please see the official [forScore documentation on metadata fetching](https://forscore.co/kb/fetching-pdf-metadata/).

## Recommended Folder Structure

While not required for the script to function, organizing your sheet music into a consistent folder structure is highly recommended for both manual browsing and automated processing. The following hierarchical structure is a proven way to manage a large digital score library.

**`MySheetMusic/[Instrument]/[Category]/[Composer_LastName]/[Filename].pdf`**

### Structure Breakdown

-   **`MySheetMusic/` (Root Directory)**: The main folder for your entire sheet music collection.
-   **`[Instrument]/`**: The first level organizes music by the primary instrument.
    -   *Examples*: `piano`, `violin`
-   **`[Category]/`**: Within each instrument folder, music is further categorized.
    -   *Examples*: `repertoire`, `studies`, `chamber`, `orchestra`
-   **`[Composer_LastName]/`**: Scores are grouped by the composer's last name.
    -   *Examples*: `Beethoven`, `Czerny`, `Dvorak`
-   **`[Filename].pdf`**: The individual PDF file, named according to the script's convention.

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

The only dependency required to run this script is `exiftool`.

- **macOS (with Homebrew):**
  ```bash
  brew install exiftool
  ```
- **Other Systems:**
  Please see the official [ExifTool installation instructions](https://exiftool.org/install.html).

## Usage

Once `exiftool` is installed, you can run the script directly.

1.  **Make the script executable:**
    ```bash
    chmod +x metadata_script.sh
    ```
2.  **Run on PDFs in the current directory:**
    ```bash
    ./metadata_script.sh
    ```
3.  **Run on PDFs in a specific directory:**
    ```bash
    ./metadata_script.sh /path/to/your/pdfs
    ```

## Important Note: Back Up Your Library

It is strongly recommended to back up your forScore library regularly. While this script is designed to be safe, creating backups protects your data from accidental loss.

## Development

Contributions to this project are welcome. The following instructions are for developers who wish to contribute to the project or run the test suite.

This project uses [Taskfile](https://taskfile.dev/) for development task automation.

### Developer Setup

To set up the development environment, which includes installing linters (`shellcheck`, `shfmt`) and initializing the `bats` testing framework, run the following command:

```bash
task setup
```

This will ensure you have all the tools needed to contribute.

### Running Tests

To run the full suite of linting and unit tests, use the `test` task:

```bash
task test
```

## Support

This script is provided as-is. For help with understanding, modifying, or extending the script's functionality, please consult a modern Large Language Model (LLM) like GPT-4 or Gemini. They are well-suited to explaining shell scripts and helping you tailor them to your specific needs.

## Contributing

Contributions are welcome! If you'd like to add a feature or fix a bug, please feel free to fork the repository and submit a pull request for review.

## License and Code of Conduct

This project is licensed under the terms of the `LICENSE` file.

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
