#!/usr/bin/env bash

set -euo pipefail

EXPECTED_FORMAT='【{emoji}: {type}】 {subject}'
SEARCH_DIR="$PWD"
CONFIG_FILE=""

while :; do
  for candidate in .git-cz.json changelog.config.js changelog.config.cjs changelog.config.json; do
    if [[ -f "$SEARCH_DIR/$candidate" ]]; then
      CONFIG_FILE="$SEARCH_DIR/$candidate"
      break 2
    fi
  done

  if [[ "$SEARCH_DIR" == "/" ]]; then
    break
  fi

  SEARCH_DIR="$(dirname "$SEARCH_DIR")"
done

if [[ -z "$CONFIG_FILE" ]]; then
  echo "No git-cz config file was found from $PWD up to /." >&2
  exit 1
fi

ACTUAL_FORMAT="$(node -p "require(process.argv[1]).format" "$CONFIG_FILE")"

if [[ "$ACTUAL_FORMAT" != "$EXPECTED_FORMAT" ]]; then
  echo "Unexpected git-cz format: $ACTUAL_FORMAT" >&2
  exit 1
fi

echo "git-cz custom config format is active."
