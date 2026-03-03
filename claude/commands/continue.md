---
description: handover ファイルを読み込み、前回セッションの作業を再開する
globs: ["**/*"]
depends-on:
  - CLAUDE.md
---

# /continue

`/continue` が実行されたとき、**セッション再開アシスタント**として handover ファイルを読み込み、
最小のコンテキスト消費で前回の作業を再開できる状態を整える。

## 制約

- handover ファイルがない場合は「引き継ぎファイルが見つかりません」と伝え、現状確認を促す
- project-state.json を直接編集しない
- コンテキストを節約するため、必要なファイルのみ読み込む

## 実施手順

1. **handover ファイルの検索**
   ```bash
   ls -lt .claude/handover/*/summary.md 2>/dev/null | head -5
   ```
   - 複数ある場合は最新のものを優先する
   - コンテキスト名が指定されている場合（例: `/continue auth-refactor`）はそれを使う

2. **summary.md を読み込む**
   - `.claude/handover/{context}/summary.md` を読み込む
   - 内容をユーザーに提示し、再開するタスクを確認する

3. **project-state.json を読み込む**
   - `.claude/handover/{context}/project-state.json` を読み込む
   - `nextActions` と `files.modified` を把握する

4. **git の状態を確認する**
   ```bash
   git log --oneline -5
   git status --short
   ```
   - handover 時の lastCommit.sha と現在の HEAD が一致するか確認する
   - 差分がある場合は「前回セッション以降に X 件のコミットがあります」と伝える

5. **最小限のファイル読み込み**
   - `files.modified` に記載されたファイルのうち、直近タスクに必要なものだけ読み込む
   - 一度に読み込むファイルは最大 5 件まで（コンテキスト節約）

6. **再開報告**
   ```
   前回のセッション（{コンテキスト名}）から再開します。

   現在のタスク: {currentTask.description}
   次のアクション:
   1. {nextActions[0]}
   2. {nextActions[1]}

   準備完了です。作業を開始してください。
   ```

## コンテキスト名を指定した再開

```
/continue {コンテキスト名}
```

例:
```
/continue auth-refactor
/continue api-endpoint
```
