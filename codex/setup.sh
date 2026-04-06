#!/usr/bin/env bash
# setup.sh
# dotfiles/claude/skills/ を ~/.codex/skills/ にシンボリックリンクで展開するセットアップスクリプト
#
# 使い方:
#   bash ~/dotfiles/codex/setup.sh
#
# 何をするか:
#   1. ~/.codex/skills/ ディレクトリを作成（なければ）
#   2. dotfiles/claude/skills/*/ → ~/.codex/skills/*/ （ディレクトリ単位リンク）
#   3. Claude plugin cache の最新 superpowers/skills → ~/.agents/skills/superpowers
#
# 既存ファイルはバックアップしてからリンクを張る

set -euo pipefail

DOTFILES_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOTFILES_CLAUDE_SKILLS="$DOTFILES_ROOT/claude/skills"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CODEX_SKILLS_HOME="$CODEX_HOME/skills"
AGENTS_SKILLS_HOME="$HOME/.agents/skills"
CLAUDE_SUPERPOWERS_CACHE_ROOT="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}!${NC} $*"; }

backup_and_link() {
  local src="$1"
  local dst="$2"

  mkdir -p "$(dirname "$dst")"

  if [[ -L "$dst" ]]; then
    rm "$dst"
  elif [[ -e "$dst" ]]; then
    local backup="${dst}.bak.$(date +%Y%m%d_%H%M%S)"
    mv "$dst" "$backup"
    log_warn "既存ファイルをバックアップ: $backup"
  fi

  ln -s "$src" "$dst"
  log_ok "リンク: $dst → $src"
}

echo "=== Codex skills セットアップ ==="
echo "ソース: $DOTFILES_CLAUDE_SKILLS"
echo "対象:   $CODEX_SKILLS_HOME"
echo ""

mkdir -p "$CODEX_SKILLS_HOME"

if [[ ! -d "$DOTFILES_CLAUDE_SKILLS" ]]; then
  echo "Claude skills ディレクトリが見つかりません: $DOTFILES_CLAUDE_SKILLS" >&2
  exit 1
fi

for src in "$DOTFILES_CLAUDE_SKILLS"/*/; do
  [[ -d "$src" ]] || continue
  name="$(basename "$src")"
  dst="$CODEX_SKILLS_HOME/$name"
  backup_and_link "$src" "$dst"
done

latest_superpowers_dir() {
  local root="$1"
  [[ -d "$root" ]] || return 1

  find "$root" -mindepth 1 -maxdepth 1 -type d | sort -V | tail -n 1
}

superpowers_root="$(latest_superpowers_dir "$CLAUDE_SUPERPOWERS_CACHE_ROOT" || true)"
if [[ -n "${superpowers_root:-}" && -d "$superpowers_root/skills" ]]; then
  mkdir -p "$AGENTS_SKILLS_HOME"
  backup_and_link "$superpowers_root/skills" "$AGENTS_SKILLS_HOME/superpowers"
  log_ok "superpowers を有効化: $AGENTS_SKILLS_HOME/superpowers"
else
  log_warn "Claude plugin cache に superpowers が見つからないためスキップ"
fi

echo ""
echo "=== 完了 ==="
echo ""
echo "現在の ~/.codex/skills 構成:"
ls -la "$CODEX_SKILLS_HOME"
echo ""
echo "現在の ~/.agents/skills 構成:"
ls -la "$AGENTS_SKILLS_HOME" 2>/dev/null || true
