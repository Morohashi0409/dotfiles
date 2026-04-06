#!/usr/bin/env bash

set -euo pipefail

HOME_DIR="${HOME:?}"
USER_NAME="${USER:-$(id -un)}"
TERM_NAME="${TERM:-xterm-256color}"
SHELL_PATH="/bin/zsh"
BASE_PATH="/usr/bin:/bin:/usr/sbin:/sbin"

run_clean_zsh() {
  local mode_flag="$1"

  env -i \
    HOME="$HOME_DIR" \
    USER="$USER_NAME" \
    LOGNAME="$USER_NAME" \
    SHELL="$SHELL_PATH" \
    TERM="$TERM_NAME" \
    PATH="$BASE_PATH" \
    "$SHELL_PATH" "$mode_flag" 'git help -a | grep -qE "^[[:space:]]+cz$"'
}

if ! run_clean_zsh -lc; then
  echo "git cz is missing in a clean login shell (zsh -lc)." >&2
  exit 1
fi

if ! run_clean_zsh -ic; then
  echo "git cz is missing in a clean interactive shell (zsh -ic)." >&2
  exit 1
fi

echo "git cz is available in login and interactive zsh shells."
