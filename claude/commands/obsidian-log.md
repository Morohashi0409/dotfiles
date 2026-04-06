---
description: 現在の会話セッションを Obsidian の 05_Claude-Log/ に記録し、デイリーノートにリンクを追記する
globs: ["**/*"]
depends-on:
  - CLAUDE.md
---

# /obsidian-log

`/obsidian-log` が実行されたとき、**obsidian-log スキル**に従って現在の会話を Obsidian Vault へ記録する。

## トリガー条件

- ユーザーが `/obsidian-log` を明示的に実行したとき
- ユーザーが「Obsidianに記録して」「ログを保存して」など記録を依頼したとき
- セッション終了時に記録を求められたとき

## 実行内容

`obsidian-log` スキルを呼び出し、以下を実施する：

1. 今日の日付を取得（`date +%Y-%m-%d`）
2. 会話トピックから slug とタイトルを決定
3. `/Users/resily0808/Documents/Obsidian Vault/05_Claude-Log/YYYY-MM-DD_{slug}.md` を作成
4. `/Users/resily0808/Documents/Obsidian Vault/01_Daily/YYYY-MM-DD.md` の `## メモ` に wikiリンクを追記

## 制約

- 要約はキーポイント5行以内（トークン節約）
- デイリーノートは上書き禁止・追記のみ
- 既存リンクとの重複チェックを必ず行う
