---
name: thread-memory
description: Use when the current conversation needs to be filed into the Obsidian AI memory system `00_AI-OS/` so that feedback, working rules, and session learnings are routed to the correct project or global files. Trigger on 「整理して記録して」「次回に活かしたい」「同じ指摘を繰り返したくない」「AIメモリに書いて」, on explicit user corrections during a thread, and at end-of-thread checkpointing before `/handover` or `/obsidian-log`.
---

# thread-memory

## Overview

1スレッドの成果を Obsidian `00_AI-OS/` 配下の永続メモリへ仕分けて追記する。反復指摘の再発防止とプロジェクト横断の学びの蓄積が目的。

**`obsidian-log` との差**: `obsidian-log` は会話要約を `05_Claude-Log/` に1ファイル書くスキル。本スキルは feedback / rules / learnings を**ファイル別に仕分け追記**することに特化。両方走らせてよい。

## Paths

- Vault: `/Users/resily0808/Documents/Obsidian Vault`
- Global: `00_AI-OS/Global.md`
- Project: `00_AI-OS/Projects/<project>/Rules.md` + `Feedback.md`
- Template: `00_AI-OS/Projects/_Template/`

## Codex Hooks Integration (Recommended)

Codex で自動起動する場合は `Stop` を使う。  
ただし `Stop` は全ターンで走るため、**厳格なガード条件付き**で運用する。

```toml
[features]
codex_hooks = true

[[hooks.Stop]]

[[hooks.Stop.hooks]]
type = "command"
command = "python3 /Users/resily0808/dotfiles/codex/hooks/stop_thread_memory.py"
timeout = 45
statusMessage = "Routing thread memory"
```

Hook script requirements:
- `Stop` では `matcher` が効かないため、スクリプト側で明示トリガーを判定する。  
  例: 「整理して記録して」「次回に活かしたい」「AIメモリに書いて」「/handover」「/obsidian-log」
- トリガー未一致なら no-op（常時保存しない）。
- バケット抽出結果が 0 件なら no-op（空書き禁止）。
- `session_id + turn_id` などで冪等化し、同一ターンの二重書き込みを防ぐ。
- 破壊編集禁止・原文保持・追記専用のガードレールを必ず適用する。

## Routing

| バケット | 抽出対象 | 追記先 |
|---|---|---|
| feedback | 指摘・違和感の表明・「〜しないで」 | `Projects/<project>/Feedback.md`（最上部に append、5タグ付与） |
| project_rules | 反復が確定したプロジェクト固有ルール | `Projects/<project>/Rules.md` |
| global_rules | 全プロジェクト適用のルール（ユーザー固有の癖） | `Global.md` |
| session_learnings | 何が効いた/失敗した/発見 | `Projects/<project>/Feedback.md` の最上部に `[学び]` タグで記録 |

> **昇格は3回以上の再発で検討**。3回未満の指摘は Feedback.md 止まり。

## カテゴリタグ判定（5タグ体系）

feedback バケットのエントリには必ず1タグ付与:

| タグ | 内容 |
|---|---|
| `[コード]` | 実装・ロジック・API・データ加工・命名 |
| `[UI]` | 見た目・レイアウト・配置・色・グラフ・文言 |
| `[テスト]` | 動作確認・検証・副作用チェック・ローカル起動 |
| `[チケット]` | Issue/PR起票・PR本文・Git操作・ブランチ |
| `[コミュ]` | 説明・報告・確認タイミング・出典明示・語調 |

**判定困難**: `[コード]` をデフォルトにし、エントリ末尾に `[要分類]` を併記。

## Steps

1. **プロジェクト特定**
   - 明示指定があればそれを採用。
   - 無ければ `cwd` のリポジトリ名、対象ファイルパス、直近のコミットスコープから推定。
   - 不可なら `unknown` とし、`Global.md` のみ追記。
   - プロジェクトディレクトリが無ければ `_Template/` をひな形にして初期化（Read→Write で各ファイルを作成）。

2. **バケット仕分け**
   - 指摘の wording は原文保持。要約は「再発防止」欄へ。
   - 1指摘=1エントリ。

3. **追記**（append-only）
   - **feedback 書き込み前に重複チェック**: 対象 `Feedback.md` を読み、同日かつ同一原文のエントリが既にあれば skip（`log-feedback` が先行記録している可能性）。
   - `Feedback.md` の `---` 区切り直後（最上部）にエントリ追加:
     ```
     ### YYYY-MM-DD [カテゴリ]
     - 指摘(原文): <原文>
     - 再発防止: <1文>
     - 関連ファイル: <任意>
     ```
   - `Rules.md` は該当セクション（優先ルール/実装ルール/レビュー観点）に追記。
   - `Global.md` への追記はユーザー固有の判断軸が3回以上現れたケースに限る（過剰昇格を避ける）。
   - `session_learnings` は `Feedback.md` 最上部に `[学び]` タグで記録。

4. **昇格促進**
   - 同趣旨の feedback が3回以上蓄積している場合、応答末尾に1行:
     `🔝 昇格候補: 「XXX」が3回以上発生。Rules.md への移動を検討してください。`

5. **報告**
   - `Project resolved: <name|unknown>`
   - `Files updated:` 絶対パスの一覧
   - `Added entries: feedback=N, rules=N, learnings=N`
   - 残った曖昧さ（あれば1行）

## Guardrails

- **破壊編集禁止**: 既存エントリの書き換え・削除は不可。見出し構造は保持。
- **原文尊重**: 指摘の語尾・表現を勝手に整形しない。
- **空書き禁止**: 該当バケットが 0 件ならそのファイルは触らない。
- **担当外**: `05_Claude-Log/` への会話要約は書かない（`obsidian-log` の担当）。`.claude/handover/` も書かない（`/handover` の担当）。
- **個人情報**: ユーザー固有の好み/判断軸は `Global.md` のユーザー特性セクションへ。プロジェクト固有要件は `Rules.md` へ。混ぜない。

## Common Mistakes

| やりがち | 正しい挙動 |
|---|---|
| 旧パス（`02_Common-Feedback.md`等）に書く | 新構成 `Projects/<project>/Feedback.md` に書く |
| `Feedback.md` の末尾に append する | 最上部（`---` 直後）に append（newest-on-top） |
| カテゴリタグを付け忘れる | 必ず5タグのいずれかを付ける |
| 1回目の指摘で Rules.md に書く | 3回以上の再発確認まで Feedback.md 止まり |
| 学びを `90_Task-Diary.md` に書く | 廃止済み。Feedback.md に `[学び]` タグで記録 |
| 既存ヘッダや他日付エントリを書き換える | 最上部に append のみ |
