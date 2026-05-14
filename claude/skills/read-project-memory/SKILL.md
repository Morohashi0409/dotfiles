---
name: read-project-memory
description: Use before the first concrete action of any non-trivial session in a project that has an Obsidian `00_AI-OS/Projects/<project>/` entry — loads global rules, project rules, and recent feedback into context so the same mistakes don't repeat. Trigger when the user asks to implement/design/debug/edit/investigate, when a task spans multiple steps, or when the session starts in a known project directory. SKIP for greetings, one-line Q&A, or when the user says 「読み込み不要」「スキップして」.
---

# read-project-memory

## Overview

実作業に入る前に Obsidian `00_AI-OS/` 内の「作業前に読むべき情報」を機械的にロードし、遵守事項と地雷を会話冒頭に短く提示する。反復指摘の再発防止が唯一の目的。

## Paths

- Vault: `/Users/resily0808/Documents/Obsidian Vault`
- Global: `00_AI-OS/Global.md`
- Project: `00_AI-OS/Projects/<project>/Rules.md` + `Feedback.md`

## Codex Hooks Integration (Recommended)

Codex で自動起動する場合は `SessionStart` を使う。

```toml
[features]
codex_hooks = true

[[hooks.SessionStart]]
matcher = "startup|resume|clear"

[[hooks.SessionStart.hooks]]
type = "command"
command = "python3 /Users/resily0808/dotfiles/codex/hooks/session_start_read_project_memory.py"
timeout = 30
statusMessage = "Loading AI-OS project memory"
```

Hook script requirements:
- `SessionStart` の `source` が `startup|resume|clear` の時だけ処理。
- `Global.md` と `Projects/<project>/Rules.md` + `Feedback.md`（直近5件）を読み、要約を 15 行以内で返す。
- ユーザーが「読み込み不要」「スキップ」と明示している文脈では no-op。
- 出力は短い追加コンテキストのみ。冗長ログを返さない。

## Steps

1. **プロジェクト特定**
   - 明示指定があれば採用。無ければ `cwd` のリポジトリ名／worktree 名から推定。
   - `Projects/<name>/` が存在しなければ `unknown` とし、Global.md のみ読む。

2. **読み込み対象**（合計3ファイル）
   - `00_AI-OS/Global.md`（全プロジェクト共通：期待品質・絶対やらない・確定ルール・ユーザー特性）
   - `00_AI-OS/Projects/<project>/Rules.md`（プロジェクト概要・固有ルール）
   - `00_AI-OS/Projects/<project>/Feedback.md`（直近5件のみ。最上部から）

3. **要約出力**（会話冒頭に1ブロックだけ、冗長禁止）
   ```
   【AI-OS 事前読み込み: <project|unknown>】
   ■ 今回守る 3 点:
   - …
   - …
   - …
   ■ やらない 3 点:
   - …
   - …
   - …
   ■ 要確認:
   - …
   ```

4. **以降の実装判断に反映**
   - 読み込んだルールに違反しそうな実装/提案は、提示前に自己検閲。

## When NOT to Trigger

- 挨拶・雑談のみ
- 1 往復で終わる事実照会（"今何時？" "このファイル何行？"）
- ユーザーが明示的に「読まなくていい」「スキップ」と言った時
- AI-OS に該当プロジェクトが存在せず Global.md も不要な場合（純粋な情報検索など）

## Output Contract

**最大 15 行、日本語、箇条書き。**事前読み込みブロック以外の前置きは書かない。読み込み後すぐに本来のタスクに着手する。

- `Feedback.md` が 200 行を超える場合、要約末尾に次を追記する:
  「⚠ Feedback.md が XX 行に達しています。古いエントリの Rules.md 昇格・削除を検討してください。」

## Common Mistakes

| やりがち | 正しい挙動 |
|---|---|
| 全ファイルを全文出力する | 遵守事項の要点だけ 3×2 箇条で出す |
| 読み込みをスキップして着手する | 「3 点遵守・3 点禁止」が言えるまで着手しない |
| Feedback.md を全件読む | 直近5件（最上部から5ブロック）のみ |
| 旧パス（`02_Projects/`・`02_Feedback/`）を読もうとする | 新構成 `Projects/<project>/Rules.md` + `Feedback.md` を読む |
| 読み込みブロックを会話末尾に出す | 必ず**作業着手の直前**に 1 回だけ出す |
