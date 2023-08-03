#!/usr/bin/env bash

function main {
	local last_release=$(git tag -l | tail -n 1)
	local new_release=$(date --utc "+%y.%m%d.0")

	echo "Releasing version ${new_release}"

	sed -i "s|${last_release}|${new_release}|g" setup.py
	EMAIL=$(git config --global user.email) gbp dch --release --new-version=${new_release}

	git commit -am "Release version ${new_release}"
	git tag "${new_release}"
}

main
