#!/usr/bin/env bats
# shellcheck disable=SC1091

load 'test_helper.bash'

setup() {
	# Point to /dev/null to test functions in isolation without a composer data file.
	export COMPOSER_NAMES_PATH="/dev/null"
	source "$BATS_TEST_DIRNAME/../metadata_script.sh"
}

teardown() {
	unset COMPOSER_NAMES_PATH
}

@test "format_work_title: adds leading zero to single-digit numbers" {
	local raw_title="Symphony5"
	local expected="Symphony 05"

	result=$(format_work_title "$raw_title")

	[ "$result" = "$expected" ]
}

@test "format_work_title: preserves double-digit numbers" {
	local raw_title="Symphony09"
	local expected="Symphony 09"

	result=$(format_work_title "$raw_title")

	[ "$result" = "$expected" ]
}

@test "format_work_title: adds space for camelCase" {
	local raw_title="ViolinConcerto"
	local expected="Violin Concerto"

	result=$(format_work_title "$raw_title")

	[ "$result" = "$expected" ]
}

@test "format_opus_string: handles single-digit opus numbers" {
	local raw_opus="Op1"
	local expected="Op. 1"

	result=$(format_opus_string "$raw_opus")

	[ "$result" = "$expected" ]
}
