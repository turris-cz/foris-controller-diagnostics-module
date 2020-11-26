#!/bin/sh

section() {
	echo "== $@ =="
}


subsection() {
	echo "-- $@ --"
}


file_header() {
	local file="$1"
	echo "~~ File: $1 ~~"
}


error() {
	echo "!! $@ !!"
}


dump_file() {
	local file="$1"
	file_header "$file"

	[ -f "$file" ] || {
		error "File not found"
		return 1
	}

	cat "$file"
}


check_installed() {
	local program="$1"
	which "$program" > /dev/null || {
		error "Program '$program' not found"
		return 1
	}
}


. "$1"

case "$2" in
	help)
		# remove first and last newline
		newline="
"
		help=${help##$newline}
		help=${help%%$newline}
		echo "$help"
		;;
	run)
		run
		;;
	*)
		{
			echo "Invalid usage of diagnostics module!"
			echo "Usage: ${0##*/} (help|run)"
		} >&2
		exit 1
		;;
esac
