"""Composer name lookup from CSV file."""

import csv
import sys
from pathlib import Path
from typing import Optional


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
        self._load_composers()

    def _load_composers(self) -> None:
        """Load composer mappings from CSV file."""
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"composers.csv not found at {self.csv_path}"
            )

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
                        print(
                            f"Warning: Multiple entries for '{simple_surname}'. "
                            f"Using more specific '{full_name}' (was '{existing_name}').",
                            file=sys.stderr,
                        )
                    else:
                        # Existing name is more specific - keep it
                        print(
                            f"Warning: Multiple entries for '{simple_surname}'. "
                            f"Using more specific '{existing_name}' (ignoring '{full_name}').",
                            file=sys.stderr,
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
