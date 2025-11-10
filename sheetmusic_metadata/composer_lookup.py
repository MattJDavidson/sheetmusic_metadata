"""Composer name lookup from CSV file."""

import csv
import sys
from pathlib import Path


class ComposerLookup:
    """Handles composer name lookups from CSV file."""

    def __init__(self, csv_path: Path):
        """
        Initialize composer lookup with CSV file path.

        Args:
            csv_path: Path to composers.csv file
        """
        self.csv_path = csv_path
        self._cache: dict[str, str] = {}
        self._duplicates: dict[str, tuple[str, str]] = {}
        self._load_composers()

    def _load_composers(self) -> None:
        """Load composer mappings from CSV file."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"composers.csv not found at {self.csv_path}")

        with open(self.csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                simple_surname = row["simple_surname"].strip()
                full_name = row["full_name"].strip()

                # Handle duplicate surnames
                if simple_surname.lower() in self._cache:
                    existing_name = self._cache[simple_surname.lower()]
                    # Prefer the most specific/complex mapping (longer, more detailed)
                    # This allows minimal definitions for common composers but
                    # specific ones for rarer variants
                    if self._is_more_specific(full_name, existing_name):
                        # New name is more specific - replace
                        self._cache[simple_surname.lower()] = full_name
                        # Store duplicate info for later warning when actually used
                        self._duplicates[simple_surname.lower()] = (
                            full_name,
                            existing_name,
                        )
                    else:
                        # Existing name is more specific - keep it
                        # Store duplicate info for later warning when actually used
                        self._duplicates[simple_surname.lower()] = (
                            existing_name,
                            full_name,
                        )
                else:
                    self._cache[simple_surname.lower()] = full_name

    @staticmethod
    def _has_initials(name: str) -> bool:
        """Check if a name contains initials (e.g., 'J.S.' or 'J. S.')."""
        # Simple heuristic: check for patterns like "J.S." or "J. S."
        parts = name.split()
        for part in parts:
            if len(part) <= 3 and part.endswith("."):
                return True
        return False

    @staticmethod
    def _is_more_specific(name1: str, name2: str) -> bool:
        """
        Determine if name1 is more specific/complex than name2.

        Prefers:
        1. Longer names (more characters)
        2. Names without initials (full names are more specific)
        3. Names with more words/parts

        Args:
            name1: First name to compare
            name2: Second name to compare

        Returns:
            True if name1 is more specific than name2
        """
        # Prefer longer names
        if len(name1) > len(name2):
            return True
        if len(name1) < len(name2):
            return False

        # If same length, prefer names without initials (full names)
        has_initials1 = ComposerLookup._has_initials(name1)
        has_initials2 = ComposerLookup._has_initials(name2)

        if not has_initials1 and has_initials2:
            return True
        if has_initials1 and not has_initials2:
            return False

        # If both have or don't have initials, prefer more words
        words1 = len(name1.split())
        words2 = len(name2.split())
        if words1 > words2:
            return True
        if words1 < words2:
            return False

        # If still equal, prefer name1 (newer entry)
        return True

    def get_full_name(self, composer_last_name: str) -> str:
        """
        Get full composer name from last name.

        Args:
            composer_last_name: The composer's last name as it appears in filename

        Returns:
            Full composer name in format "Surname, FirstName"
            Falls back to capitalized last name if not found
        """
        # Trim whitespace and normalize case
        clean_key = composer_last_name.strip().lower()

        # Warn about duplicates only when actually used
        if clean_key in self._duplicates:
            chosen_name, ignored_name = self._duplicates[clean_key]
            print(
                f"Warning: Multiple entries for '{composer_last_name}'. "
                f"Using more specific '{chosen_name}' (ignoring '{ignored_name}').",
                file=sys.stderr,
            )
            # Remove from duplicates so we only warn once per composer
            del self._duplicates[clean_key]

        full_name = self._cache.get(clean_key)

        if full_name is None:
            # Fallback: Capitalize first letter
            fallback_name = (
                composer_last_name[0].upper() + composer_last_name[1:].lower()
                if composer_last_name
                else composer_last_name
            )
            print(
                f"Warning: Full name for '{composer_last_name}' not found in map. "
                f"Using '{fallback_name}'.",
                file=sys.stderr,
            )
            return fallback_name

        return full_name

    def get_full_name_for_pdf(self, composer_last_name: str) -> str:
        """
        Get full composer name formatted for PDF Author field (forScore compatible).

        forScore splits the Author field on commas, treating each part as a separate
        composer. To avoid this, we use space-separated format. However, forScore sorts
        by the first word, so we need "FirstName Surname" format (reversed from CSV)
        to ensure proper sorting by surname in forScore's composer list.

        Args:
            composer_last_name: The composer's last name as it appears in filename

        Returns:
            Full composer name in format "FirstName Surname" (space-separated, reversed)
            Falls back to capitalized last name if not found
        """
        full_name = self.get_full_name(composer_last_name)

        # Convert "Surname, FirstName" to "FirstName Surname" for forScore compatibility
        # forScore sorts by first word, so we reverse the order
        if ", " in full_name:
            parts = full_name.split(", ", 1)
            if len(parts) == 2:
                surname, first_name = parts
                return f"{first_name} {surname}"

        # If no comma found (fallback case), return as-is
        return full_name.replace(", ", " ")
