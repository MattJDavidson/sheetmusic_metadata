#!/usr/bin/env bats
# shellcheck disable=SC1091

load 'test_helper.bash'

setup() {
	# Source the composer names to populate the array in this shell.
	source "$BATS_TEST_DIRNAME/../composer_names.sh"
	# Prevent the main script from sourcing the data file again.
	export COMPOSER_NAMES_PATH="/dev/null"
	# Source the main script to get access to its functions.
	source "$BATS_TEST_DIRNAME/../metadata_script.sh"
}

@test "filename parsing: Beethoven Symphony 5" {
	local filename="Beethoven_Symphony05_Op67_Violin1.pdf"

	[ "$(get_composer_from_filename "$filename")" = "Beethoven" ]
	[ "$(get_work_from_filename "$filename")" = "Symphony05" ]
	[ "$(get_opus_from_filename "$filename")" = "Op67" ]
	[ "$(get_part_from_filename "$filename")" = "Violin1" ]
}

@test "filename parsing: Rimsky-Korsakov Scheherazade" {
	local filename="Rimsky-Korsakov_Scheherazade_Op35_Flute2.pdf"

	[ "$(get_composer_from_filename "$filename")" = "Rimsky-Korsakov" ]
	[ "$(get_work_from_filename "$filename")" = "Scheherazade" ]
	[ "$(get_opus_from_filename "$filename")" = "Op35" ]
	[ "$(get_part_from_filename "$filename")" = "Flute2" ]
}

@test "filename parsing: Vaughan Williams The Lark Ascending" {
	local filename="VaughanWilliams_LarkAscending_Viola.pdf"

	[ "$(get_composer_from_filename "$filename")" = "VaughanWilliams" ]
	[ "$(get_work_from_filename "$filename")" = "LarkAscending" ]
	[ "$(get_opus_from_filename "$filename")" = "NoOp" ]
	[ "$(get_part_from_filename "$filename")" = "Viola" ]
}

@test "filename parsing: Rimsky-Korsakov Symphony 1" {
	local filename="Rimsky-Korsakov_Symphony01_Op1_Oboe1.pdf"

	[ "$(get_composer_from_filename "$filename")" = "Rimsky-Korsakov" ]
	[ "$(get_work_from_filename "$filename")" = "Symphony01" ]
	[ "$(get_opus_from_filename "$filename")" = "Op1" ]
	[ "$(get_part_from_filename "$filename")" = "Oboe1" ]
}
