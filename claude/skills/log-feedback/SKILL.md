---
name: log-feedback
description: Use the moment the user expresses a correction, frustration, or "don't do that" during a conversation — immediately writes the feedback to the appropriate Obsidian `Projects/<project>/Feedback.md` (top of file) so the same mistake doesn't repeat later in the same thread or in future sessions. Trigger on phrases like 「違う」「そうじゃなくて」「〜しないで」「〜するな」「また同じ」「何度言えば」「ダメ」「NG」, explicit 「記録して」, or any tone shift indicating dissatisfaction with the previous assistant response. This is the mid-session complement to `thread-memory`.
---

# log-feedback

## Overview

ユーザー訂正の瞬間を逃さず即座に Obsidian へ 1 ブロック書き込む。`thread-memory` が会話末尾の一括処理なのに対し、本スキルは**発話直後の単発コミット**。

書き込み先: `00_AI-OS/Projects/<project>/Feedback.md` の最上部（newest-on-top）。

## Codex Hooks Integration (Recommended)

Codex で自動起動する場合は `UserPromptSubmit` を使う。  
このイベントでは `matcher` が効かないため、**スクリプト内判定で必ず絞る**。

```toml
[features]
codex_hooks = true

[[hooks.UserPromptSubmit]]

[[hooks.UserPromptSubmit.hooks]]
type = "command"
command = "python3 /Users/resily0808/dotfiles/codex/hooks/user_prompt_log_feedback.py"
timeout = 30
statusMessage = "Capturing correction feedback"
```

Hook script requirements:
- 全ユーザー入力で走る前提なので、訂正・否定・禁止要求パターンに一致しない場合は no-op。
- 第三者への言及（例: 「チームに違うと言われた」）は no-op。
- 対象時のみ `Projects/<project>/Feedback.md` 最上部へ 1 エントリ追記。
- 同日・同一原文の重複記録は skip（再投稿・再送信対策）。

## Trigger Patterns

- 明示否定: 「違う」「そうじゃなくて」「それは違う」「逆」
- 禁止要求: 「〜しないで」「〜するな」「やめて」「勝手に〜するな」
- 反復苛立ち: 「また同じ」「何度も言ってるけど」「前も言った」「何回言えば」
- 短評価: 「ダメ」「NG」「微妙」「違和感」
- 明示依頼: 「これ記録して」「忘れないで」「次回のために残して」
- 品質不満: 「雑」「適当」「考えてない」

**誤検知回避**: ユーザーが**第三者への言及**（例: "チームに『違う』って言われた"）で上記語を使った場合は起動しない。直前の assistant 応答への評価である場合のみ起動。

## カテゴリタグ判定（5タグ体系）

書き込むエントリの先頭タグを以下の基準で選ぶ：

| タグ | 内容 | 例 |
|---|---|---|
| `[コード]` | 実装・ロジック・API・データ加工・命名 | optional chaining不可、正規化処理不要、変数名 |
| `[UI]` | 見た目・レイアウト・配置・色・グラフ・文言 | 縦軸文字逆転、軸ラベル欠落、白背景 |
| `[テスト]` | 動作確認・検証・副作用チェック・ローカル起動 | 全メトリクス比較、ローカル起動確認、回帰テスト |
| `[チケット]` | Issue/PR起票・PR本文・Git操作・ブランチ | resolve #XXXX、masterに反映、部分コミット |
| `[コミュ]` | 説明・報告・確認タイミング・出典明示・語調 | 確認してと言ったとき、Excelセル番地、質問だけ |

**判定困難な場合**: `[コード]` をデフォルトにし、エントリ末尾に `[要分類]` を併記。

## Steps

1. **プロジェクト特定**
   - `cwd` のリポジトリ名／worktree 名から推定。
   - `00_AI-OS/Projects/<project>/Feedback.md` が無ければ `_Template/Feedback.md` をひな形にして新規作成。
   - 推定不能なら 1 行だけ確認。

2. **カテゴリタグ判定**（上表から1つ選ぶ）

3. **ファイル先頭に append**
   - `Feedback.md` の `---` 区切り直後（最上部）に新エントリを挿入:
     ```
     ### YYYY-MM-DD [カテゴリ]
     - 指摘(原文): <ユーザー発話をそのまま>
     - 再発防止: <次回から取るべき具体的行動を 1 文>
     - 関連ファイル: <会話中に出ていれば>
     ```
   - **原文保持**: 語尾・感情表現を整形しない。

4. **反復検知 → 昇格促進**
   - 同ファイルを読み、同趣旨の指摘が過去 30 日で 3 件以上あれば、応答末尾に
     `🔝 昇格候補: 「XXX」が3回以上発生。Rules.md への移動を検討してください。`
   - 自動移動はしない（ユーザー判断）。

5. **報告（最小）**
   - 本体応答の末尾に 1 行: `📝 記録: <絶対パス> [カテゴリ]`

## Guardrails

- **本題を止めない**: 訂正後の続きを期待されている。記録は素早く済ませる。
- **確認を増やさない**: 記録内容の確認ダイアログは出さない。
- **破壊編集禁止**: 既存エントリの書き換え不可。最上部に append のみ。
- **空書き禁止**: 原文が曖昧（「うーん」だけ等）なら書かずに本題を続行。
- **担当外**: rules / learnings の仕分けは書かない（`thread-memory` の担当）。

## Relation to thread-memory

- `log-feedback` が既に書いた指摘は、`thread-memory` 実行時に重複チェックされ skip される。
- 両方走らせても二重記録されない。

## Common Mistakes

| やりがち | 正しい挙動 |
|---|---|
| 記録した旨を長々と説明する | 末尾 1 行の絶対パス表示のみ |
| 第三者への言及で誤発火 | 直前の自分の応答への評価かを判定 |
| ファイルの末尾に append する | 最上部（`---` 直後）に append（newest-on-top） |
| 旧パス（`02_Common-Feedback.md`等）に書く | `Projects/<project>/Feedback.md` に書く |
| カテゴリタグを付けずに書く | 必ず `[コード]` `[UI]` `[テスト]` `[チケット]` `[コミュ]` のいずれかを付ける |
| 意訳してから「指摘(原文)」欄に書く | 原文は一字一句そのまま |
