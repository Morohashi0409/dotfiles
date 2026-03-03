#!/usr/bin/env bash
# setup.sh
# ~/dotfiles 内の設定ファイルをホームディレクトリにシンボリックリンクで展開するセットアップスクリプト
#
# 使い方:
#   bash ~/dotfiles/setup.sh
#
# 対象:
#   1. .zshrc
#   2. .gitconfig
#   3. .claude.json
#   4. .wezterm.lua（存在する場合のみ）
#   5. config/cursor/settings.json → ~/Library/Application Support/Cursor/User/settings.json
#   6. config/obsidian/ → ~/Documents/Obsidian Vault/.obsidian（ディレクトリごとリンク）
#   7. Claude 関連は claude/setup.sh に委任

set -euo pipefail

DOTFILES="$(cd "$(dirname "$0")" && pwd)"

# カラー出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}!${NC} $*"; }
log_skip() { echo -e "${YELLOW}⏭${NC} $*"; }

backup_and_link() {
  local src="$1"
  local dst="$2"

  # ソースが存在しない場合はスキップ
  if [[ ! -e "$src" ]]; then
    log_skip "ソースが存在しません: $src"
    return
  fi

  # リンク先の親ディレクトリを作成
  mkdir -p "$(dirname "$dst")"

  # 既存ファイル/リンクがある場合の処理
  if [[ -L "$dst" ]]; then
    # すでにシンボリックリンク → 削除して再リンク
    rm "$dst"
  elif [[ -e "$dst" ]]; then
    # 実ファイルが存在 → バックアップ
    local backup="${dst}.bak_$(date +%Y%m%d_%H%M%S)"
    mv "$dst" "$backup"
    log_warn "既存ファイルをバックアップ: $backup"
  fi

  ln -snf "$src" "$dst"
  log_ok "リンク: $dst → $src"
}

echo "=== dotfiles セットアップ ==="
echo "ソース: $DOTFILES"
echo ""

# 1. .zshrc
backup_and_link "$DOTFILES/.zshrc" "$HOME/.zshrc"

# 2. .gitconfig
backup_and_link "$DOTFILES/.gitconfig" "$HOME/.gitconfig"

# 3. .claude.json
backup_and_link "$DOTFILES/.claude.json" "$HOME/.claude.json"

# 4. .wezterm.lua（存在する場合のみ）
backup_and_link "$DOTFILES/.wezterm.lua" "$HOME/.wezterm.lua"

# 5. Cursor settings.json
backup_and_link "$DOTFILES/config/cursor/settings.json" "$HOME/Library/Application Support/Cursor/User/settings.json"

# 6. Obsidian 設定ディレクトリ（ディレクトリごとリンク）
backup_and_link "$DOTFILES/config/obsidian" "$HOME/Documents/Obsidian Vault/.obsidian"

# 7. Claude 関連は claude/setup.sh に委任
if [[ -f "$DOTFILES/claude/setup.sh" ]]; then
  echo ""
  bash "$DOTFILES/claude/setup.sh"
else
  log_skip "claude/setup.sh が見つかりません"
fi

echo ""
echo "=== 完了 ==="
