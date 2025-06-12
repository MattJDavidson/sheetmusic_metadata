#!/usr/bin/env bash
#
# Automates PDF metadata tagging via exiftool based on a filename schema.
#
# Schema: ComposerLastName_WorkIdentifier_Opus_Part.pdf
# Example: Dvorak_Symphony09_Op95_Violin1.pdf
#
# Prerequisites:
# - exiftool (e.g., `brew install exiftool`)
# - `composer_data.sh` in the same directory.
#
# Usage:
#   ./metadata_script.sh [-o /path/to/output_dir] [-t "Custom Tag 1"] [-t "Custom Tag 2"] [file_or_dir_path]
#   If no directory is provided, it processes PDFs in the current directory.

# --- Initial Checks ---
if ! command -v exiftool &>/dev/null; then
	echo "Error: exiftool is not installed. Please install it to continue." >&2
	echo "On macOS with Homebrew, run: brew install exiftool" >&2
	exit 1
fi

# --- Global Constants ---

# Source composer data unconditionally to populate the composer_full_names array.
# shellcheck disable=SC1090
source "$(dirname "${BASH_SOURCE[0]}")/composer_names.sh" || {
	echo "Error: composer_names.sh not found." >&2
	echo "Please ensure it's in the same directory as the script." >&2
	exit 1
}

# This allows adding a broader instrument category tag in forScore.
declare -gA INSTRUMENT_FAMILIES
INSTRUMENT_FAMILIES["Violin"]="Strings"
INSTRUMENT_FAMILIES["Viola"]="Strings"
INSTRUMENT_FAMILIES["Cello"]="Strings"
INSTRUMENT_FAMILIES["DoubleBass"]="Strings"
INSTRUMENT_FAMILIES["Flute"]="Woodwind"
INSTRUMENT_FAMILIES["Oboe"]="Woodwind"
INSTRUMENT_FAMILIES["Clarinet"]="Woodwind"
INSTRUMENT_FAMILIES["Bassoon"]="Woodwind"
INSTRUMENT_FAMILIES["Trumpet"]="Brass"
INSTRUMENT_FAMILIES["Horn"]="Brass"
INSTRUMENT_FAMILIES["Trombone"]="Brass"
INSTRUMENT_FAMILIES["Tuba"]="Brass"
INSTRUMENT_FAMILIES["Timpani"]="Percussion"
INSTRUMENT_FAMILIES["Percussion"]="Percussion" # For generic percussion parts
INSTRUMENT_FAMILIES["Harp"]="Harp"
INSTRUMENT_FAMILIES["Piano"]="Keyboard" # For orchestral piano parts
INSTRUMENT_FAMILIES["Celesta"]="Keyboard"
INSTRUMENT_FAMILIES["Organ"]="Keyboard"

# The main genre for orchestral parts will be "Orchestral".
readonly PDF_SUBJECT="Orchestral"
# Default keywords include general orchestral tags.
readonly DEFAULT_KEYWORDS="Orchestral"

# --- Functions ---

# Extracts the part identifier from the filename.
get_part_from_filename() {
	local filename_no_ext="${1%.*}"
	IFS='_' read -r -a parts <<<"$filename_no_ext"
	if [ "${#parts[@]}" -eq 4 ]; then
		echo "${parts[3]}"
	elif [ "${#parts[@]}" -eq 3 ]; then
		echo "${parts[2]}"
	fi
}

# Extracts the composer's last name from the filename.
get_composer_from_filename() {
	local filename_no_ext="${1%.*}"
	echo "$filename_no_ext" | cut -d'_' -f1
}

# Extracts the work identifier from the filename.
get_work_from_filename() {
	local filename_no_ext="${1%.*}"
	echo "$filename_no_ext" | cut -d'_' -f2
}

# Extracts the opus number from the filename.
get_opus_from_filename() {
	local filename_no_ext="${1%.*}"
	IFS='_' read -r -a parts <<<"$filename_no_ext"
	if [ "${#parts[@]}" -eq 4 ]; then
		echo "${parts[2]}"
	else
		echo "NoOp"
	fi
}

# parse_filename_components: Parses the filename into its constituent parts.
# Arguments:
#   $1 - filename without extension (e.g., "Dvorak_Symphony09_Op95_Violin1")
# Outputs:
#   Sets global variables: PARSED_COMPOSER_LAST_NAME, PARSED_WORK_IDENTIFIER, PARSED_OPUS, PARSED_PART
#   Returns 1 if parsing fails, 0 otherwise.
parse_filename_components() {
	local filename_no_ext="$1"
	IFS='_' read -r -a parts <<<"$filename_no_ext"

	if [[ ${#parts[@]} -eq 3 ]]; then
		# Schema: Composer_Work_Part (no Opus)
		PARSED_COMPOSER_LAST_NAME="${parts[0]}"
		PARSED_WORK_IDENTIFIER="${parts[1]}"
		PARSED_PART="${parts[2]}"
		PARSED_OPUS="NoOp"
	elif [[ ${#parts[@]} -eq 4 ]]; then
		# Schema: Composer_Work_Opus_Part
		PARSED_COMPOSER_LAST_NAME="${parts[0]}"
		PARSED_WORK_IDENTIFIER="${parts[1]}"
		PARSED_OPUS="${parts[2]}"
		PARSED_PART="${parts[3]}"
	else
		echo "  Error: Filename '$filename_no_ext' does not match the expected schema (3 or 4 parts)." >&2
		return 1
	fi

	# Basic validation: ensure essential parts are not empty
	if [[ -z "$PARSED_COMPOSER_LAST_NAME" || -z "$PARSED_WORK_IDENTIFIER" || -z "$PARSED_PART" ]]; then
		echo "  Error: Filename '$filename_no_ext' is missing one of the required components (Composer, Work, Part)." >&2
		return 1
	fi
	return 0
}

# Looks up the full composer name from a mapping.
get_full_composer_name() {
	local composer_last_name="$1"
	local full_name="${composer_full_names[$composer_last_name]}"

	if [[ -z "$full_name" ]]; then
		# Fallback: Capitalize first letter if not in map
		full_name="${composer_last_name^}"
		echo "  Warning: Full name for '$composer_last_name' not found in map. Using '$full_name'." >&2
	fi
	echo "$full_name"
}

# Formats the work identifier for the PDF title.
format_work_title() {
	local work_identifier="$1"
	local with_spaces
	# Add space for camelCase and before numbers.
	with_spaces=$(echo "$work_identifier" | sed -E 's/([a-z])([A-Z])/\1 \2/g; s/([A-Za-z])([0-9]+)/\1 \2/g')

	# Pad single-digit numbers with a leading zero.
	echo "$with_spaces" | sed -E 's/ ([0-9])$/ 0\1/'
}

# Formats the raw part string for display and tagging.
format_part_string() {
	local raw_part="$1"
	# Handles cases like Violin1 -> Violin 1.
	echo "$raw_part" | sed -E 's/([A-Za-z]+)([0-9]+)/\1 \2/g; s/Piccolo/ Piccolo/g; s/DoubleBass/Double Bass/g; s/EnglishHorn/English Horn/g'
}

# Formats the raw opus string for display and tagging.
format_opus_string() {
	local raw_opus="$1"
	echo "$raw_opus" | sed -E 's/Op([0-9]+)/Op. \1/g'
}

# Determines the instrument family tag.
get_instrument_family() {
	local formatted_part_string="$1"
	local base_instrument_name
	base_instrument_name=$(echo "$formatted_part_string" | cut -d' ' -f1)
	local instrument_family="${INSTRUMENT_FAMILIES[$base_instrument_name]}"

	if [[ -z "$instrument_family" ]]; then
		echo "  Warning: Instrument family for '$base_instrument_name' not found in map. Using base name as tag." >&2
		instrument_family="$base_instrument_name"
	fi
	echo "$instrument_family"
}

# Applies metadata to a PDF file using exiftool.
# Returns: 0 on success, 1 on failure.
apply_pdf_metadata() {
	local filepath="$1"
	local pdf_title="$2"
	local pdf_author="$3"
	local pdf_subject="$4"
	local pdf_keywords="$5"
	local output_dir="$6" # Optional: directory to save the new file

	local exiftool_args=(
		-Title="$pdf_title"
		-Author="$pdf_author"
		-Subject="$pdf_subject"
		-Keywords="$pdf_keywords"
		-e
	)

	if [[ -n "$output_dir" ]]; then
		# Ensure the output directory exists
		mkdir -p "$output_dir"
		# Add argument to write to a new file in the specified directory
		exiftool_args+=(-o "$output_dir/%f.%e")
	else
		# Default behavior: overwrite the original file
		exiftool_args+=(-overwrite_original)
	fi

	exiftool "${exiftool_args[@]}" "$filepath" >/dev/null

	return $?
}

process_file() {
	local filepath="$1"
	local output_dir="$2"
	shift 2
	local additional_tags=("$@")
	local filename
	filename=$(basename "$filepath")
	local filename_no_ext="${filename%.*}" # Remove .pdf extension

	echo "Processing file: $filename"

	if ! parse_filename_components "$filename_no_ext"; then
		echo "  Skipping file due to parsing error." >&2
		echo "---"
		return 1
	fi

	local full_composer_name
	full_composer_name=$(get_full_composer_name "$PARSED_COMPOSER_LAST_NAME")
	local formatted_work_title
	formatted_work_title=$(format_work_title "$PARSED_WORK_IDENTIFIER")
	local formatted_part
	formatted_part=$(format_part_string "$PARSED_PART")
	local formatted_opus
	formatted_opus=$(format_opus_string "$PARSED_OPUS")
	local instrument_family_tag
	instrument_family_tag=$(get_instrument_family "$formatted_part")

	local PDF_TITLE="${formatted_work_title} - ${formatted_part} Part"
	local all_keywords=("${DEFAULT_KEYWORDS}" "${formatted_part}" "${formatted_opus}" "${instrument_family_tag}")
	all_keywords+=("${additional_tags[@]}")
	local PDF_KEYWORDS
	PDF_KEYWORDS=$(
		IFS=,
		echo "${all_keywords[*]}"
	)

	echo "Composer: $full_composer_name"
	echo "Title: \"$PDF_TITLE\""
	echo "Keywords (Tags): \"$PDF_KEYWORDS\""

	if ! apply_pdf_metadata "$filepath" "$PDF_TITLE" "$full_composer_name" "$PDF_SUBJECT" "$PDF_KEYWORDS" "$output_dir"; then
		echo "  Error: Failed to apply metadata to '$filename'." >&2
		echo "---"
		return 1
	fi

	echo "  Successfully applied metadata."
	echo "---"
	return 0
}

# --- Main Execution ---
main() {
	local output_dir=""
	local -a additional_tags=()

	# Parse options with getopts
	while getopts ":o:t:" opt; do
		case $opt in
		o)
			output_dir="$OPTARG"
			;;
		t)
			additional_tags+=("$OPTARG")
			;;
		\?)
			echo "Invalid option: -$OPTARG" >&2
			exit 1
			;;
		:)
			echo "Option -$OPTARG requires an argument." >&2
			exit 1
			;;
		esac
	done
	shift $((OPTIND - 1))

	local path="${1:-.}" # Default to current directory if no path is provided

	if [[ ! -e "$path" ]]; then
		echo "Error: File or directory not found at '$path'" >&2
		exit 1
	fi

	local overall_status=0
	if [[ -f "$path" ]]; then
		if ! process_file "$path" "$output_dir" "${additional_tags[@]}"; then
			overall_status=1
		fi
	elif [[ -d "$path" ]]; then
		echo "Processing all PDF files in directory: $path"
		while IFS= read -r -d '' file; do
			if ! process_file "$file" "$output_dir" "${additional_tags[@]}"; then
				overall_status=1 # If any file fails, the final exit code will be 1
			fi
		done < <(find "$path" -maxdepth 1 -type f -name "*.pdf" -print0)
	else
		echo "Error: Path '$path' is not a file or a directory." >&2
		exit 1
	fi

	exit $overall_status
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
	main "$@"
fi
