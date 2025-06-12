#!/usr/bin/env bats
# shellcheck disable=SC1091,SC2154

load 'test_helper'

@test "composer_names.sh can be sourced and the map is populated" {
	source "$BATS_TEST_DIRNAME/../composer_names.sh"
	[ ${#composer_full_names[@]} -gt 0 ]
}

@test "Lookup 'Adams' and get 'John Adams'" {
	source "$BATS_TEST_DIRNAME/../composer_names.sh"
	[ "${composer_full_names[Adams]}" = "John Adams" ]
}
