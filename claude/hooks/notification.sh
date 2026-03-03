#!/usr/bin/env bash
# notification.sh
# Claude Code の Notification フック
# タスク完了などの通知をmacOSに送る

set -euo pipefail

INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | jq -r '.message // "Claude Code からの通知"' 2>/dev/null || echo "Claude Code からの通知")
TITLE=$(echo "$INPUT" | jq -r '.title // "Claude Code"' 2>/dev/null || echo "Claude Code")

# macOS通知
if command -v osascript &>/dev/null; then
  osascript -e "display notification \"${MESSAGE}\" with title \"${TITLE}\" sound name \"Ping\"" 2>/dev/null || true
fi

exit 0
