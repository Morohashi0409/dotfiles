#!/usr/bin/env bash
# post-commit.sh
# Claude Code の PostToolUse フック（git commit 後）
# コミット完了をmacOSに通知する

set -euo pipefail

# 最新コミット情報を取得
COMMIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
COMMIT_MSG=$(git log -1 --format="%s" 2>/dev/null || echo "")

# macOS通知（osascript が使える環境のみ）
if command -v osascript &>/dev/null; then
  osascript -e "display notification \"${COMMIT_MSG}\" with title \"Git Commit: ${COMMIT_SHA}\" sound name \"Glass\"" 2>/dev/null || true
fi

exit 0
