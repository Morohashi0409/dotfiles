---
description: 現在の作業コンテキストをファイルに書き出し、次セッションへ引き継ぐ
globs: ["**/*"]
depends-on:
  - CLAUDE.md
---

# /handover

`/handover` が実行されたとき、**セッション引き継ぎアシスタント**として現在の作業状態をファイルに書き出す。
トークン消費が 150k を超えた際、または長期タスクの区切りで実行する。

## 制約

- `project-state.json` は自動生成する。ユーザーに編集を促さない
- 保存先は `.claude/handover/{context}/` 固定（コンテキスト名はタスクの識別子）
- 既存の handover ファイルがある場合は上書きする
- 書き出し完了後、必ず `/clear` の実行を案内する

## 実施手順

1. **コンテキスト名を決定する**
   - 現在のタスクを表す短い識別子（英数字・ハイフン）を決める
   - 例: `auth-refactor`, `api-endpoint`, `doc-update`
   - 曖昧な場合のみユーザーに確認する

2. **git の状態を確認する**
   ```bash
   git log --oneline -5
   git status --short
   git diff --stat HEAD
   ```

3. **project-state.json を生成する**
   ```
   保存先: .claude/handover/{context}/project-state.json
   ```
   以下の形式で生成する：
   ```json
   {
     "context": "{コンテキスト名}",
     "timestamp": "{ISO8601形式の現在日時}",
     "lastCommit": {
       "sha": "{直近コミットのSHA}",
       "message": "{コミットメッセージ}"
     },
     "currentTask": {
       "description": "{現在取り組んでいるタスクの説明}",
       "status": "in_progress | blocked | completed",
       "blockers": ["{ブロッカーがあれば記載}"]
     },
     "files": {
       "modified": ["{変更中のファイルパス}"],
       "created": ["{新規作成したファイルパス}"],
       "deleted": ["{削除したファイルパス}"]
     },
     "nextActions": [
       "{次にやるべきアクション1}",
       "{次にやるべきアクション2}"
     ],
     "tokenUsage": "{現在の概算トークン消費量（例: 145k）}"
   }
   ```

4. **summary.md を生成する**
   ```
   保存先: .claude/handover/{context}/summary.md
   ```
   以下の形式で生成する：
   ```markdown
   # Handover Summary: {コンテキスト名}

   **日時:** {現在日時}
   **最終コミット:** {SHA} - {メッセージ}

   ## 現在のタスク
   {タスクの説明を2〜3文で}

   ## 完了済み
   - {完了したこと1}
   - {完了したこと2}

   ## 次にやること
   1. {次のアクション1}
   2. {次のアクション2}

   ## ブロッカー・注意事項
   - {あれば記載、なければ「なし」}

   ## 重要なファイルパス
   - {関連ファイル1}
   - {関連ファイル2}
   ```

5. **完了報告と次の指示**
   ```
   handover を完了しました。
   保存先: .claude/handover/{context}/
     - project-state.json
     - summary.md

   次のステップ:
   1. /clear を実行してコンテキストをリセット
   2. 新しいセッションで /continue を実行して作業を再開
   ```
