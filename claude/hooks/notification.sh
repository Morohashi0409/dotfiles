#!/usr/bin/env bash
# notification.sh
# Claude Code の Notification / Stop フック
# REST API を呼び出して外部オートメーションをトリガーする

set -euo pipefail

# REST API を呼び出す
curl -k -s -X POST https://local.jmw.nz:41443/haptic/sharp_collision > /dev/null 2>&1 || true

exit 0
