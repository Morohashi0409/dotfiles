#!/usr/bin/env bash
# notification.sh
# Claude Code の Notification / Stop フック
# REST API を呼び出して外部オートメーションをトリガーする

set -euo pipefail

# REST API を呼び出す（バックグラウンド + タイムアウト）
curl -k -s -X POST https://local.jmw.nz:41443/haptic/sharp_collision \
  --max-time 1 --connect-timeout 0.5 > /dev/null 2>&1 & disown

exit 0
