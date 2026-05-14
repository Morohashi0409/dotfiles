#!/usr/bin/env bash
# setup.sh
# dotfiles/cursor/ を ~/.cursor/ にシンボリックリンクで展開する
#
# 使い方:
#   bash ~/dotfiles/cursor/setup.sh
#
# 何をするか:
#   1. dotfiles/cursor/rules/*.mdc          → ~/.cursor/rules/*.mdc （個別リンク）
#   2. dotfiles/claude/skills/<obsidian>/   → ~/.cursor/skills-cursor/<obsidian>/ （ディレクトリ単位リンク）
#      対象: read-project-memory / log-feedback / thread-memory
#
# 既存ファイル/ディレクトリはバックアップしてからリンクを張る。

set -euo pipefail

DOTFILES_CURSOR="$(cd "$(dirname "$0")" && pwd)"
DOTFILES_ROOT="$(dirname "$DOTFILES_CURSOR")"
CURSOR_HOME="$HOME/.cursor"

# Obsidian AI-OS 連携の共有スキル（Claude と統一して symlink）
OBSIDIAN_SKILLS=(
  "read-project-memory"
  "log-feedback"
  "thread-memory"
)

# カラー出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}!${NC} $*"; }
log_err()  { echo -e "${RED}✗${NC} $*"; }
log_head() { echo -e "${BLUE}▶${NC} $*"; }

# symlink を張る（既存があればバックアップ）
# 引数: $1 = リンク元（実体）, $2 = リンク先
link_with_backup() {
  local src="$1"
  local dest="$2"

  if [[ ! -e "$src" ]]; then
    log_err "リンク元が存在しません: $src"
    return 1
  fi

  # 既存が同じ symlink を指していれば skip
  if [[ -L "$dest" ]]; then
    local current
    current="$(readlink "$dest")"
    if [[ "$current" == "$src" ]]; then
      log_ok "(変更なし) $dest -> $src"
      return 0
    fi
    rm "$dest"
  elif [[ -e "$dest" ]]; then
    local backup="${dest}.bak.$(date +%Y%m%d_%H%M%S)"
    mv "$dest" "$backup"
    log_warn "既存を退避: $dest -> $backup"
  fi

  ln -s "$src" "$dest"
  log_ok "$dest -> $src"
}

log_head "Cursor グローバル設定を ~/.cursor/ に展開"

# 1. rules ディレクトリ
mkdir -p "$CURSOR_HOME/rules"
log_head "rules/*.mdc を展開"
shopt -s nullglob
for rule in "$DOTFILES_CURSOR"/rules/*.mdc; do
  link_with_backup "$rule" "$CURSOR_HOME/rules/$(basename "$rule")"
done
shopt -u nullglob

# 2. Obsidian 連携スキル（Claude と同じ実体を symlink）
mkdir -p "$CURSOR_HOME/skills-cursor"
log_head "Obsidian 連携スキルを展開（Claude と統一）"
for skill in "${OBSIDIAN_SKILLS[@]}"; do
  src="$DOTFILES_ROOT/claude/skills/$skill"
  dest="$CURSOR_HOME/skills-cursor/$skill"
  if [[ ! -d "$src" ]]; then
    log_err "スキルが見つかりません: $src"
    continue
  fi
  link_with_backup "$src" "$dest"
done

echo ""
log_head "完了"
echo "  Cursor を再起動して新しいルールとスキルを読み込ませてください。"
echo "  確認: ls -la $CURSOR_HOME/rules/ $CURSOR_HOME/skills-cursor/"
