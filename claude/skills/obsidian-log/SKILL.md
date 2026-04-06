---
name: obsidian-log
description: Use when the user invokes /obsidian-log or at session end to record a concise Claude Code session summary to Obsidian Vault and link it to today's daily note. Use when user asks to log, record, or save the current AI conversation to Obsidian.
---

# obsidian-log

## Overview

会話の要約を Obsidian Vault の `05_Claude-Log/` に書き出し、当日のデイリーノートにwikiリンクを追記する。**トークン消費を最小化**するため、要約は箇条書き5行以内に留める。

## Paths

- Log dir: `/Users/resily0808/Documents/Obsidian Vault/05_Claude-Log/`
- Daily dir: `/Users/resily0808/Documents/Obsidian Vault/01_Daily/`
- Daily note: `YYYY-MM-DD.md` (today's date)

## Log File Format

ファイル名: `YYYY-MM-DD_{slug}.md`（slug = トピックを英数字ハイフンで3〜5語）

```markdown
---
date: YYYY-MM-DD
project: {作業ディレクトリのベース名}
tags: [claude-log]
---

# {トピック（日本語可）}

## 要約
{会話の目的と結果を1〜2文で}

## キーポイント
- {決定事項・学び・重要な発見}（最大5行）

## 使用スキル
- {呼び出したスキル名}（例: `obsidian-log`, `superpowers:writing-skills`）（あれば）

## 変更ファイル
- {編集・作成したファイルのパス}（あれば）

## コミット
- {git SHA と一言メッセージ}（あれば）
```

## Daily Note Linking

今日のデイリーノート (`01_Daily/YYYY-MM-DD.md`) の `## メモ` セクションを探し、その直後に1行追記する：

```
- [[05_Claude-Log/YYYY-MM-DD_{slug}|{トピック}]]
```

`## メモ` が存在しない場合はファイル末尾に追記する。同じリンクが既に存在する場合はスキップ。

## Steps

1. `date +%Y-%m-%d` で今日の日付を取得
2. 会話内容から slug（英語）とトピック名（日本語可）を決める
3. Log ファイルを Write ツールで作成（既存なら末尾に `---` セクション追加）
4. Daily note を Read し `## メモ` を探す
5. Edit ツールでリンクを1行挿入（既存リンクと重複しない場合のみ）

## Token Budget

- 要約生成: 推定 200〜500 tokens
- ファイル書き込み: 1 Read + 1 Write/Edit
- **合計目標: 1000 tokens 以内**

長い要約・会話ダンプは禁止。キーポイントは5行まで。

## Common Mistakes

- ❌ 会話全文をそのまま書き出す（トークン無駄・読みにくい）
- ❌ デイリーノートを上書きする（Editで追記のみ）
- ❌ slug に日本語・スペースを使う（ファイル名が壊れる）
- ✅ 同一日の複数セッションは別ファイル（slug で区別）
