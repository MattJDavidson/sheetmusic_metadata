#!/usr/bin/env bats
# shellcheck disable=SC1091,SC2154

load 'test_helper'
# Source the main script to have access to its functions.
source "$BATS_TEST_DIRNAME/../metadata_script.sh"

@test "get_full_composer_name: lookup 'Bach' and get 'Bach, Johann Sebastian'" {
	run get_full_composer_name "Bach"
	[ "$status" -eq 0 ]
	[ "$output" = "Bach, Johann Sebastian" ]
}

@test "get_full_composer_name: lookup 'Beethoven' and get 'Beethoven, Ludwig van'" {
	run get_full_composer_name "Beethoven"
	[ "$status" -eq 0 ]
	[ "$output" = "Beethoven, Ludwig van" ]
}

@test "get_full_composer_name: fallback for a name not in the list" {
	run get_full_composer_name "UnknownComposer"
	[ "$status" -eq 0 ]
	# It should capitalize the first letter and print a warning.
	[[ "$output" == *"UnknownComposer"* ]]
	[[ "$output" == *"Warning: Full name for 'UnknownComposer' not found in map. Using 'UnknownComposer'."* ]]
}

@test "get_full_composer_name: handles leading/trailing whitespace in lookup key" {
	run get_full_composer_name "  Brahms  "
	[ "$status" -eq 0 ]
	[ "$output" = "Brahms, Johannes" ]
}
