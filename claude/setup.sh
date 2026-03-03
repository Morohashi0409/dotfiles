#!/usr/bin/env bash
# setup.sh
# dotfiles/claude/ を ~/.claude/ にシンボリックリンクで展開するセットアップスクリプト
#
# 使い方:
#   bash ~/dotfiles/claude/setup.sh
#
# 何をするか:
#   1. ~/.claude/ ディレクトリを作成（なければ）
#   2. dotfiles/claude/CLAUDE.md        → ~/.claude/CLAUDE.md
#   3. dotfiles/claude/settings.json    → ~/.claude/settings.json
#   4. dotfiles/claude/commands/*.md    → ~/.claude/commands/*.md （個別リンク）
#   5. dotfiles/claude/hooks/*.sh       → ~/.claude/hooks/*.sh （個別リンク）
#   6. dotfiles/ccstatusline/settings.json → ~/.config/ccstatusline/settings.json
#
# 既存ファイルはバックアップしてからリンクを張る

set -euo pipefail

DOTFILES_CLAUDE="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_HOME="$HOME/.claude"

# カラー出力
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}!${NC} $*"; }
log_err()  { echo -e "${RED}✗${NC} $*"; }

backup_and_link() {
  local src="$1"
  local dst="$2"

  # 保存先ディレクトリを作成
  mkdir -p "$(dirname "$dst")"

  # 既存ファイル/リンクがある場合の処理
  if [[ -L "$dst" ]]; then
    # すでにシンボリックリンク → 更新
    rm "$dst"
  elif [[ -e "$dst" ]]; then
    # 実ファイルが存在 → バックアップ
    local backup="${dst}.bak.$(date +%Y%m%d_%H%M%S)"
    mv "$dst" "$backup"
    log_warn "既存ファイルをバックアップ: $backup"
  fi

  ln -s "$src" "$dst"
  log_ok "リンク: $dst → $src"
}

echo "=== Claude dotfiles セットアップ ==="
echo "ソース: $DOTFILES_CLAUDE"
echo "対象:   $CLAUDE_HOME"
echo ""

# ~/.claude/ ディレクトリ確保
mkdir -p "$CLAUDE_HOME"

# 1. CLAUDE.md
if [[ -f "$DOTFILES_CLAUDE/CLAUDE.md" ]]; then
  backup_and_link "$DOTFILES_CLAUDE/CLAUDE.md" "$CLAUDE_HOME/CLAUDE.md"
fi

# 2. settings.json
# ※ settings.local.json が既にある場合は上書きしない（ローカル設定を優先）
if [[ -f "$DOTFILES_CLAUDE/settings.json" ]]; then
  backup_and_link "$DOTFILES_CLAUDE/settings.json" "$CLAUDE_HOME/settings.json"
fi

# 3. commands/ — 個別にリンク（既存コマンドを残しつつ追加）
if [[ -d "$DOTFILES_CLAUDE/commands" ]]; then
  mkdir -p "$CLAUDE_HOME/commands"
  for src in "$DOTFILES_CLAUDE/commands"/*.md; do
    [[ -f "$src" ]] || continue
    dst="$CLAUDE_HOME/commands/$(basename "$src")"
    backup_and_link "$src" "$dst"
  done
fi

# 4. hooks/ — 個別にリンク
if [[ -d "$DOTFILES_CLAUDE/hooks" ]]; then
  mkdir -p "$CLAUDE_HOME/hooks"
  for src in "$DOTFILES_CLAUDE/hooks"/*.sh; do
    [[ -f "$src" ]] || continue
    dst="$CLAUDE_HOME/hooks/$(basename "$src")"
    backup_and_link "$src" "$dst"
  done
fi

# 5. ccstatusline 設定
DOTFILES_ROOT="$(dirname "$DOTFILES_CLAUDE")"
CCSTATUSLINE_SRC="$DOTFILES_ROOT/ccstatusline/settings.json"
CCSTATUSLINE_DST="$HOME/.config/ccstatusline/settings.json"
if [[ -f "$CCSTATUSLINE_SRC" ]]; then
  backup_and_link "$CCSTATUSLINE_SRC" "$CCSTATUSLINE_DST"
fi

echo ""
echo "=== 完了 ==="
echo ""
echo "現在の ~/.claude/ 構成:"
ls -la "$CLAUDE_HOME/"
echo ""

# settings.local.json が空の場合はデフォルト内容を案内
if [[ ! -f "$CLAUDE_HOME/settings.local.json" ]]; then
  log_warn "settings.local.json が見つかりません。"
  echo "  マシン固有の設定が必要な場合は ~/.claude/settings.local.json を作成してください。"
  echo "  例:"
  cat <<'EOF'
  {
    "permissions": {
      "allow": [
        "WebFetch(domain:your-internal-domain.com)"
      ]
    }
  }
EOF
fi
