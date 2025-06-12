#!/usr/bin/env bats
# shellcheck disable=SC2154

load 'test_helper.bash'

# Load the script and its dependencies for direct function testing.
setup() {
	# Source the composer names to populate the array in this shell.
	# shellcheck disable=SC1091
	source "$BATS_TEST_DIRNAME/../composer_names.sh"
	# Source the main script to get access to its functions.
	# shellcheck disable=SC1091
	source "$BATS_TEST_DIRNAME/../metadata_script.sh"
}

# Helper function to test the full metadata generation from a filename.
# This tests the integration of parsing, formatting, and lookup functions.
run_metadata_generation_test() {
	local filename_no_ext="${1%.*}"
	local expected_composer="$2"
	local expected_title="$3"
	local expected_keywords="$4"

	# Run the same logic as the main script's process_file function.
	parse_filename_components "$filename_no_ext"

	local actual_composer
	actual_composer=$(get_full_composer_name "$PARSED_COMPOSER_LAST_NAME")

	local formatted_work
	formatted_work=$(format_work_title "$PARSED_WORK_IDENTIFIER")
	local formatted_part
	formatted_part=$(format_part_string "$PARSED_PART")
	local actual_title="${formatted_work} - ${formatted_part} Part"

	local formatted_opus
	formatted_opus=$(format_opus_string "$PARSED_OPUS")
	local instrument_family
	instrument_family=$(get_instrument_family "$formatted_part")

	local all_keywords=("Orchestral" "${formatted_part}" "${formatted_opus}" "${instrument_family}")
	local actual_keywords
	actual_keywords=$(
		IFS=,
		echo "${all_keywords[*]}"
	)

	[ "$actual_composer" = "$expected_composer" ]
	[ "$actual_title" = "$expected_title" ]
	[ "$actual_keywords" = "$expected_keywords" ]
}

@test "metadata generation: Beethoven Symphony 5" {
	run_metadata_generation_test \
		"Beethoven_Symphony05_Op67_Violin1.pdf" \
		"Ludwig van Beethoven" \
		"Symphony 05 - Violin 1 Part" \
		"Orchestral,Violin 1,Op. 67,Strings"
}

@test "metadata generation: Dvořák Symphony 9" {
	run_metadata_generation_test \
		"Dvorak_Symphony09_Op95_Cello.pdf" \
		"Antonín Dvořák" \
		"Symphony 09 - Cello Part" \
		"Orchestral,Cello,Op. 95,Strings"
}

@test "metadata generation: Tchaikovsky Symphony 6" {
	run_metadata_generation_test \
		"Tchaikovsky_Symphony06_Op74_Clarinet1.pdf" \
		"Pyotr Ilyich Tchaikovsky" \
		"Symphony 06 - Clarinet 1 Part" \
		"Orchestral,Clarinet 1,Op. 74,Woodwind"
}

@test "metadata generation: Brahms Symphony 4" {
	run_metadata_generation_test \
		"Brahms_Symphony04_Op98_Oboe2.pdf" \
		"Johannes Brahms" \
		"Symphony 04 - Oboe 2 Part" \
		"Orchestral,Oboe 2,Op. 98,Woodwind"
}

@test "metadata generation: Sibelius Violin Concerto" {
	run_metadata_generation_test \
		"Sibelius_ViolinConcerto_Op47_Trumpet1.pdf" \
		"Jean Sibelius" \
		"Violin Concerto - Trumpet 1 Part" \
		"Orchestral,Trumpet 1,Op. 47,Brass"
}
