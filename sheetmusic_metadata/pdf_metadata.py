"""PDF metadata writing using exiftool."""

import subprocess
import sys
from pathlib import Path


def apply_pdf_metadata(
    filepath: Path,
    pdf_title: str,
    pdf_author: str,
    pdf_subject: str,
    pdf_keywords: str,
    output_dir: Path | None = None,
) -> None:
    """
    Apply metadata to a PDF file using exiftool.

    Args:
        filepath: Path to the PDF file
        pdf_title: PDF Title metadata
        pdf_author: PDF Author metadata
        pdf_subject: PDF Subject metadata
        pdf_keywords: PDF Keywords metadata (comma-separated)
        output_dir: Optional directory to write output file to.
                    If None, overwrites the original file.

    Raises:
        FileNotFoundError: If exiftool is not installed
        subprocess.CalledProcessError: If exiftool fails
        OSError: If file operations fail
    """
    # Check if exiftool is available
    try:
        subprocess.run(
            ["exiftool", "-ver"],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise FileNotFoundError(
            "exiftool is not installed. Please install it to continue.\n"
            "On macOS with Homebrew, run: brew install exiftool"
        )

    exiftool_args = [
        f"-Title={pdf_title}",
        f"-Author={pdf_author}",
        f"-Subject={pdf_subject}",
        f"-Keywords={pdf_keywords}",
        "-e",  # Exclude these tags from reading
    ]

    if output_dir is not None:
        # Ensure the output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        # Write to a new file in the specified directory
        exiftool_args.extend(["-o", str(output_dir / f"{filepath.name}")])
    else:
        # Default behavior: overwrite the original file
        exiftool_args.append("-overwrite_original")

    exiftool_args.append(str(filepath))

    # Run exiftool
    result = subprocess.run(
        ["exiftool"] + exiftool_args,
        capture_output=True,
        text=True,
        check=False,
    )

    # Check for actual errors (not just warnings)
    # exiftool returns 0 on success, but may return 1 even with warnings
    # Look for "Error:" in stderr to distinguish from warnings
    # Also check stdout for success message: "X image files updated"
    has_error = False
    if result.returncode != 0:
        # Check if there are actual errors (not just warnings about xref tables, etc.)
        error_lines = [
            line
            for line in (result.stderr + result.stdout).split("\n")
            if line.strip().startswith("Error:")
        ]
        if error_lines:
            has_error = True
        # Check if file was actually updated
        elif "files updated" not in result.stdout:
            # No success message and non-zero return code - likely an error
            if "files weren't updated" in result.stdout or "could not be read" in result.stdout:
                has_error = True
    
    if has_error:
        raise subprocess.CalledProcessError(
            result.returncode,
            ["exiftool"] + exiftool_args,
            result.stderr + "\n" + result.stdout,
        )


def read_pdf_metadata(filepath: Path) -> dict[str, str]:
    """
    Read PDF metadata using exiftool.

    Args:
        filepath: Path to the PDF file

    Returns:
        Dictionary with metadata fields (Title, Author, Subject, Keywords)

    Raises:
        FileNotFoundError: If exiftool is not installed
        subprocess.CalledProcessError: If exiftool fails
    """
    # Check if exiftool is available
    try:
        subprocess.run(
            ["exiftool", "-ver"],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise FileNotFoundError(
            "exiftool is not installed. Please install it to continue.\n"
            "On macOS with Homebrew, run: brew install exiftool"
        )

    # Read specific metadata fields using tab-separated format
    result = subprocess.run(
        [
            "exiftool",
            "-Title",
            "-Author",
            "-Subject",
            "-Keywords",
            "-T",  # Tab-separated output
            str(filepath),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    # Parse the tab-separated output (format: "Title\tAuthor\tSubject\tKeywords")
    # Filter out warning lines
    lines = [
        line.strip()
        for line in result.stdout.strip().split("\n")
        if line.strip() and not line.strip().startswith("Warning:")
    ]

    metadata = {}
    if lines:
        # First non-warning line should be tab-separated values
        parts = lines[0].split("\t")
        if len(parts) >= 4:
            metadata["Title"] = parts[0].strip() if parts[0].strip() != "-" else ""
            metadata["Author"] = parts[1].strip() if parts[1].strip() != "-" else ""
            metadata["Subject"] = parts[2].strip() if parts[2].strip() != "-" else ""
            metadata["Keywords"] = parts[3].strip() if parts[3].strip() != "-" else ""

    # Fallback: try reading individual fields if tab format didn't work
    if not metadata or all(not v for v in metadata.values()):
        for field in ["Title", "Author", "Subject", "Keywords"]:
            field_result = subprocess.run(
                ["exiftool", f"-{field}", "-s", "-S", str(filepath)],
                capture_output=True,
                text=True,
                check=False,
            )
            if field_result.returncode == 0:
                value = field_result.stdout.strip()
                # Filter out warnings
                if value and not value.startswith("Warning:"):
                    metadata[field] = value

    return metadata
