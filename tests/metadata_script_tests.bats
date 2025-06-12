#!/usr/bin/env bats

load 'test_helper.bash'

# Creates a fixtures directory for tests. Runs once per file.
setup_file() {
	mkdir -p "tests/fixtures"
}

# Cleans up the fixtures directory. Runs once per file.
teardown_file() {
	rm -rf "tests/fixtures"
}

setup() {
	# Point to the actual composer names file to allow for correct lookups.
	export COMPOSER_NAMES_PATH="$BATS_TEST_DIRNAME/../composer_names.sh"
}

teardown() {
	# Unset the variable to ensure a clean state for the next test.
	unset COMPOSer_NAMES_PATH
}

# Helper function to run a test for a given filename and expected metadata.
# This approach isolates filename parsing from composer full name lookups.
run_parsing_test() {
	local filename="$1"
	local expected_composer="$2"
	local expected_title="$3"
	local expected_keywords="$4"

	touch "tests/fixtures/$filename"

	run bash "$BATS_TEST_DIRNAME/../metadata_script.sh" "tests/fixtures"

	[ "$status" -eq 0 ]
	echo "$output" | grep "Composer: $expected_composer"
	echo "$output" | grep "Title: \"$expected_title\""
	echo "$output" | grep "Keywords (Tags): \"$expected_keywords\""

	# Clean up the specific file after the test
	rm "tests/fixtures/$filename"
}

@test "filename parsing: Beethoven Symphony 5" {
	run_parsing_test \
		"Beethoven_Symphony05_Op67_Violin1.pdf" \
		"Ludwig van Beethoven" \
		"Symphony 05 - Violin 1 Part" \
		"Orchestral, Violin 1, Op. 67, Strings"
}

@test "filename parsing: Dvořák Symphony 9" {
	run_parsing_test \
		"Dvorak_Symphony09_Op95_Cello.pdf" \
		"Antonín Dvořák" \
		"Symphony 09 - Cello Part" \
		"Orchestral, Cello, Op. 95, Strings"
}

@test "filename parsing: Tchaikovsky Symphony 6" {
	run_parsing_test \
		"Tchaikovsky_Symphony06_Op74_Clarinet1.pdf" \
		"Pyotr Ilyich Tchaikovsky" \
		"Symphony 06 - Clarinet 1 Part" \
		"Orchestral, Clarinet 1, Op. 74, Woodwind"
}

@test "filename parsing: Brahms Symphony 4" {
	run_parsing_test \
		"Brahms_Symphony04_Op98_Oboe2.pdf" \
		"Johannes Brahms" \
		"Symphony 04 - Oboe 2 Part" \
		"Orchestral, Oboe 2, Op. 98, Woodwind"
}

@test "filename parsing: Sibelius Violin Concerto" {
	run_parsing_test \
		"Sibelius_ViolinConcerto_Op47_Trumpet1.pdf" \
		"Jean Sibelius" \
		"Violin Concerto - Trumpet 1 Part" \
		"Orchestral, Trumpet 1, Op. 47, Brass"
}
