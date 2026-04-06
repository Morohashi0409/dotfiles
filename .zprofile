if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

typeset -U path PATH

if [[ -d "$HOME/.local/share/mise/shims" ]]; then
  path=("$HOME/.local/share/mise/shims" $path)
fi
