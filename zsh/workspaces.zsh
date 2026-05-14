# workspaces.zsh
# プロジェクトディレクトリへの高速移動と WezTerm 起動ヘルパー
#
# 使い方:
#   dxp        # /Users/resily0808/dxp/dxp-2/dxp へ cd
#   wellcom    # ~/WrllCom_front2025/WellCom_front へ cd
#   dotfiles   # ~/dotfiles へ cd
#
#   wz             # 現在のディレクトリで WezTerm 新規ウィンドウ
#   wz dxp         # dxp ディレクトリで WezTerm 新規ウィンドウ
#   wz wellcom     # wellcom ディレクトリで WezTerm 新規ウィンドウ
#
# ワークスペース追加:
#   下の WORKSPACES 連想配列にエントリを追加するだけ。cd 関数 / wz 補完が自動で生えます。

# 二重 source 防止
if [[ -n "${_WORKSPACES_LOADED:-}" ]]; then
  return 0
fi
_WORKSPACES_LOADED=1

typeset -gA WORKSPACES=(
  dxp      "/Users/resily0808/dxp/dxp-2/dxp"
  wellcom  "$HOME/WrllCom_front2025/WellCom_front"
  dotfiles "$HOME/dotfiles"
)

_workspace_dir() {
  local name="$1"
  local dir="${WORKSPACES[$name]:-}"
  if [[ -z "$dir" ]]; then
    echo "workspace: '$name' は未登録です (available: ${(k)WORKSPACES})" >&2
    return 1
  fi
  if [[ ! -d "$dir" ]]; then
    echo "workspace: '$name' のディレクトリが存在しません: $dir" >&2
    return 1
  fi
  print -r -- "$dir"
}

# 各ワークスペースに対応する cd 関数を動的生成
for _ws_name in "${(@k)WORKSPACES}"; do
  eval "${_ws_name}() {
    local dir
    dir=\$(_workspace_dir ${_ws_name}) || return 1
    cd \"\$dir\"
  }"
done
unset _ws_name

# WezTerm を指定ワークスペースで起動。引数なしなら現在ディレクトリ。
wz() {
  if [[ $# -eq 0 ]]; then
    wezterm start --cwd .
    return
  fi
  local dir
  dir=$(_workspace_dir "$1") || return 1
  wezterm start --cwd "$dir"
}

# wz の tab 補完
_wz_complete() {
  local -a names
  names=("${(@k)WORKSPACES}")
  _describe 'workspace' names
}
compdef _wz_complete wz 2>/dev/null
