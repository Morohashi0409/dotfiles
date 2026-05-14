#!/usr/bin/env bash
# setup.sh
# dotfiles/claude/ を Claude Code のプロファイルディレクトリにシンボリックリンクで展開する
#
# 使い方:
#   bash ~/dotfiles/claude/setup.sh                  # personal (~/.claude/) のみ
#   bash ~/dotfiles/claude/setup.sh --profile arm    # ~/.claude-config/arm/ も対象
#   bash ~/dotfiles/claude/setup.sh --all            # personal + ~/.claude-config/* すべて
#
# 何をするか（各プロファイルディレクトリに対して）:
#   1. ディレクトリを作成（なければ）
#   2. dotfiles/claude/CLAUDE.md        → <profile>/CLAUDE.md
#   3. dotfiles/claude/settings.json    → <profile>/settings.json
#   4. dotfiles/claude/commands/*.md    → <profile>/commands/*.md （個別リンク）
#   5. dotfiles/claude/hooks/*.sh       → <profile>/hooks/*.sh （個別リンク）
#   6. dotfiles/claude/skills/*/        → <profile>/skills/*/ （ディレクトリ単位リンク）
#   7. dotfiles/ccstatusline/settings.json → ~/.config/ccstatusline/settings.json （personal のみ）
#
# 既存ファイルはバックアップしてからリンクを張る。
# settings.local.json はマシン固有のためコピー/リンクしない。

set -euo pipefail

DOTFILES_CLAUDE="$(cd "$(dirname "$0")" && pwd)"
DOTFILES_ROOT="$(dirname "$DOTFILES_CLAUDE")"
CLAUDE_HOME="$HOME/.claude"
CLAUDE_CONFIG_ROOT="$HOME/.claude-config"

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

# 引数解析
PROFILES=()
INCLUDE_PERSONAL=1
USAGE_ERR=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      if [[ -z "${2:-}" ]]; then
        log_err "--profile には名前が必要です (例: --profile arm)"
        USAGE_ERR=1
        break
      fi
      PROFILES+=("$2")
      shift 2
      ;;
    --all)
      # ~/.claude-config/* を全部対象に追加
      if [[ -d "$CLAUDE_CONFIG_ROOT" ]]; then
        for d in "$CLAUDE_CONFIG_ROOT"/*/; do
          [[ -d "$d" ]] || continue
          PROFILES+=("$(basename "$d")")
        done
      fi
      shift
      ;;
    -h|--help)
      sed -n '2,10p' "$0"
      exit 0
      ;;
    *)
      log_err "不明な引数: $1"
      USAGE_ERR=1
      break
      ;;
  esac
done

if [[ $USAGE_ERR -eq 1 ]]; then
  echo ""
  echo "Usage:"
  echo "  bash $0                  # personal のみ"
  echo "  bash $0 --profile <name> # 指定プロファイルも対象"
  echo "  bash $0 --all            # personal + ~/.claude-config/* すべて"
  exit 1
fi

# ----- 共通関数 -----

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

# 指定プロファイルディレクトリへ dotfiles の symlink を展開
link_into_profile() {
  local profile_root="$1"
  local profile_label="$2"

  log_head "プロファイル: $profile_label ($profile_root)"
  mkdir -p "$profile_root"

  # 1. CLAUDE.md
  if [[ -f "$DOTFILES_CLAUDE/CLAUDE.md" ]]; then
    backup_and_link "$DOTFILES_CLAUDE/CLAUDE.md" "$profile_root/CLAUDE.md"
  fi

  # 2. settings.json
  if [[ -f "$DOTFILES_CLAUDE/settings.json" ]]; then
    backup_and_link "$DOTFILES_CLAUDE/settings.json" "$profile_root/settings.json"
  fi

  # 3. commands/ — 既にディレクトリ自体が symlink ならスキップ、それ以外は個別リンク
  if [[ -d "$DOTFILES_CLAUDE/commands" ]]; then
    if [[ -L "$profile_root/commands" ]]; then
      log_ok "commands/ は既にシンボリックリンク: $(readlink "$profile_root/commands") — スキップ"
    else
      mkdir -p "$profile_root/commands"
      for src in "$DOTFILES_CLAUDE/commands"/*.md; do
        [[ -f "$src" ]] || continue
        backup_and_link "$src" "$profile_root/commands/$(basename "$src")"
      done
    fi
  fi

  # 4. hooks/
  if [[ -d "$DOTFILES_CLAUDE/hooks" ]]; then
    mkdir -p "$profile_root/hooks"
    for src in "$DOTFILES_CLAUDE/hooks"/*.sh; do
      [[ -f "$src" ]] || continue
      backup_and_link "$src" "$profile_root/hooks/$(basename "$src")"
    done
  fi

  # 5. skills/ — ディレクトリ単位
  if [[ -d "$DOTFILES_CLAUDE/skills" ]]; then
    mkdir -p "$profile_root/skills"
    for src in "$DOTFILES_CLAUDE/skills"/*/; do
      [[ -d "$src" ]] || continue
      name="$(basename "$src")"
      backup_and_link "$src" "$profile_root/skills/$name"
    done
  fi

  echo ""
}

# ----- 実行 -----

echo "=== Claude dotfiles セットアップ ==="
echo "ソース: $DOTFILES_CLAUDE"
echo ""

# personal（~/.claude/）
if [[ $INCLUDE_PERSONAL -eq 1 ]]; then
  link_into_profile "$CLAUDE_HOME" "personal"
fi

# 追加プロファイル（~/.claude-config/<name>/）
for profile in "${PROFILES[@]:-}"; do
  [[ -z "$profile" ]] && continue
  link_into_profile "$CLAUDE_CONFIG_ROOT/$profile" "$profile"
done

# ccstatusline は profile に依存せず personal の ~/.config 側のみ管理
CCSTATUSLINE_SRC="$DOTFILES_ROOT/ccstatusline/settings.json"
CCSTATUSLINE_DST="$HOME/.config/ccstatusline/settings.json"
if [[ -f "$CCSTATUSLINE_SRC" ]]; then
  log_head "ccstatusline"
  backup_and_link "$CCSTATUSLINE_SRC" "$CCSTATUSLINE_DST"
  echo ""
fi

echo "=== 完了 ==="
echo ""

# settings.local.json の案内（personal のみ）
if [[ $INCLUDE_PERSONAL -eq 1 && ! -f "$CLAUDE_HOME/settings.local.json" ]]; then
  log_warn "settings.local.json が見つかりません。"
  echo "  マシン固有の設定が必要な場合は ~/.claude/settings.local.json を作成してください。"
fi

if [[ ${#PROFILES[@]:-0} -gt 0 ]]; then
  echo ""
  echo "次のステップ（追加プロファイル）:"
  for profile in "${PROFILES[@]}"; do
    echo "  claude-$profile        # 起動 → /login で認証"
    echo "  claude-$profile /status  # アカウント確認"
  done
fi
