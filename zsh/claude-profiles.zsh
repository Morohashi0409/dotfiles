# claude-profiles.zsh
# Claude Code を複数の Anthropic アカウント間で切り替えるためのプロファイル関数
#
# 仕組み:
#   CLAUDE_CONFIG_DIR 環境変数を切り替えると、Claude Code は認証情報・履歴・todos 等を
#   そのディレクトリに保存・参照する。dotfiles の symlink は両方のプロファイルに張られて
#   いるため、CLAUDE.md / skills / commands / hooks / settings.json は共通で適用される。
#
# 使い方:
#   claude            # personal (~/.claude/)        ※既存のまま、何も変えない
#   claude-personal   # personal を明示起動
#   claude-arm        # ARM 社内アカウント (~/.claude-config/arm/)
#
# 引数はすべて claude にそのまま forward される:
#   claude-arm --dangerously-skip-permissions
#   claude-arm --model claude-sonnet-4-6
#   claude-arm /status
#
# 初回セットアップ:
#   bash ~/dotfiles/claude/setup.sh --profile arm    # symlink を張る
#   claude-arm                                       # 起動 → /login で認証

# 二重 source 防止
if [[ -n "${_CLAUDE_PROFILES_LOADED:-}" ]]; then
  return 0
fi
_CLAUDE_PROFILES_LOADED=1

# personal を明示起動（CLAUDE_CONFIG_DIR を unset して素の claude を呼ぶ）
claude-personal() {
  CLAUDE_CONFIG_DIR= command claude "$@"
}

# ARM 社内アカウント
claude-arm() {
  local profile_dir="$HOME/.claude-config/arm"
  if [[ ! -d "$profile_dir" ]]; then
    echo "claude-arm: $profile_dir が未作成です。" >&2
    echo "次を実行してください: bash ~/dotfiles/claude/setup.sh --profile arm" >&2
    return 1
  fi
  CLAUDE_CONFIG_DIR="$profile_dir" command claude "$@"
}
