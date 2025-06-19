#!/bin/bash
for file in "$@"; do
	if grep -q ', ' "$file"; then
		echo "🔧 Fixing spacing in $file"
		sed -i '' 's/, \+/,/g' "$file"
	fi
done
