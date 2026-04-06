#!/usr/bin/env bash
# Stop hook: Obsidian セッションログ（最小エントリ）
# Stop hookはシェルコマンドのみ使用可能（LLM不使用）
# 詳細なLLM要約はCLAUDE.mdの指示でClaudeが /obsidian-log を実行する

set -euo pipefail

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
PROJECT=$(basename "${PWD:-unknown}")
LOG_DIR="/Users/resily0808/Documents/Obsidian Vault/05_Claude-Log"
DAILY_DIR="/Users/resily0808/Documents/Obsidian Vault/01_Daily"
LOG_FILE="${LOG_DIR}/${DATE}_${PROJECT}.md"
DAILY_FILE="${DAILY_DIR}/${DATE}.md"

mkdir -p "$LOG_DIR"

# ログファイルが存在しない場合のみ基本エントリを作成
# （/obsidian-log が既に実行済みならスキップ）
if [ ! -f "$LOG_FILE" ]; then
  cat > "$LOG_FILE" << MDEOF
---
date: ${DATE}
project: ${PROJECT}
tags: [claude-log]
---

# ${PROJECT} セッション

## 要約
自動記録（詳細は /obsidian-log で上書き可能）

## キーポイント
- ${TIME} セッション終了
MDEOF
fi

# デイリーノートにリンクを追記（Python3で確実に ## メモ 直後に挿入）
LINK="[[05_Claude-Log/${DATE}_${PROJECT}|${PROJECT}]]"
if [ -f "$DAILY_FILE" ]; then
  python3 - "$DAILY_FILE" "$LINK" << 'PYEOF'
import sys

filepath = sys.argv[1]
link_text = sys.argv[2]
insert_line = f"- {link_text}"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 既にリンクが存在する場合はスキップ
if any(link_text in line for line in lines):
    sys.exit(0)

# ## メモ の直後に挿入
new_lines = []
inserted = False
for i, line in enumerate(lines):
    new_lines.append(line)
    if not inserted and line.strip() == "## メモ":
        # 次の行が空行ならその後に、そうでなければ ## メモ の直後に挿入
        new_lines.append(insert_line + "\n")
        inserted = True

# ## メモ が見つからなかった場合はファイル末尾に追記
if not inserted:
    new_lines.append(f"\n{insert_line}\n")

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
PYEOF
fi
