#!/usr/bin/env bash
# pre-tool-use.sh
# Claude Code の PreToolUse フック
# 破壊的なコマンドを検出してブロックする

set -euo pipefail

# 標準入力から JSON を受け取る（Claude Code がフックに渡す形式）
INPUT=$(cat)

# tool_input.command を取得
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null || true)

if [[ -z "$COMMAND" ]]; then
  exit 0
fi

# ブロック対象パターン
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "rm --no-preserve-root"
  "dd if=/dev/zero"
  "dd if=/dev/random"
  "mkfs\."
  ":(){ :|:& };:"
  "chmod -R 777 /"
  "chown -R .* /"
  "> /dev/sda"
  "shred /dev/"
  "wipefs"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern" 2>/dev/null; then
    echo "ERROR: 危険なコマンドを検出してブロックしました: $COMMAND" >&2
    # exit 2 でツール実行をブロック（Claude Code の仕様）
    exit 2
  fi
done

exit 0
