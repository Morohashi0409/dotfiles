# Claude Agent グローバル運用ガイドライン

このファイルは `~/dotfiles/claude/CLAUDE.md` として管理され、シンボリックリンクで `~/.claude/CLAUDE.md` に配置される。
すべてのプロジェクトで共通して適用されるグローバルなガイドラインを定義する。

---

## コミュニケーション方針

- 技術的に誤った意見には根拠を示して反論すること
- 指示が曖昧な場合は推測せず、明確化を求めること
- 設計・レビューは分割せず、完全な形で一度に提出すること
- 出力は日本語で行うこと

---

## 実装規律

- 初回実装時にバリデーション（範囲制約・境界値・型チェック）を組み込む
- コミット前に linter・型チェック・フォーマット・テストを実行する
- 3ステップ以上のタスクは実行前に計画フェーズを設け、承認を得てから着手する（Intent Guard）

---

## Git・Agent 管理

- `git worktree` 使用時は作業ディレクトリの確認が必須
- マルチエージェント調整では明示的なスコープと完了条件を設定し、作業の重複を防ぐ
- スキル呼び出し時は該当スキルのみ実行し、暗黙的なピボットは禁止

---

## コンテキスト管理（トークン節約）

### 計画的リセットの原則

トークン消費が **150k** を超えたら handover を実行してコンテキストをリセットする。

```
手順:
1. /handover を実行して現在の状態をファイルに書き出す
2. /clear でコンテキストをリセット
3. 新セッションで /continue を実行して作業を再開
```

### handover ファイルの保存先

```
.claude/handover/{context}/
  ├── project-state.json   # タスク・ファイルパス・ブロッカー・コミットSHAを含む状態
  └── summary.md           # 人間が読める進捗サマリー
```

- `project-state.json` は `/handover` スキルが自動生成する。直接編集しない。
- `summary.md` は次セッションの `/continue` が参照する。

---

## ドキュメント自動チェック（doc-check）

コードを変更したタイミングで `/doc-check` を呼び出し、関連ドキュメントの更新漏れを検出する。

### depends-on の宣言

スキルや命令ファイルの frontmatter に `depends-on` を宣言すると、doc-check がそのファイルとの整合性をチェックする。

```yaml
---
description: 何をするスキルか
depends-on:
  - CLAUDE.md
  - docs/architecture.md
---
```

---

## コマンド一覧（~/dotfiles/claude/commands/）

ユーザーが `/xxx` で明示的に呼び出すコマンド。

| コマンド | 用途 |
|----------|------|
| `/handover` | 現在の進捗・文脈をファイルに書き出す |
| `/continue` | handover ファイルから作業を再開する |
| `/doc-check` | ドキュメントの差分チェック・更新 |
| `/commit` | コミット＆プッシュ（絵文字 Prefix 付き） |
| `/review` | コードレビュー |
| `/pre-review` | コミット前の自動チェック |
| `/doc` | 技術ドキュメント作成・整備 |
| `/create-command` | 新規コマンドを dotfiles に追加 |
| `/github-issue-organize` | PRコメントの整理・記録 |

## スキル一覧（~/dotfiles/claude/skills/）

Claude Code が自動トリガーする、または `/skill名` でも呼べるスキル。

| スキル | 用途 |
|--------|------|
| `frontend-design` | 高品質フロントエンドUI生成 |
| `fixing-accessibility` | アクセシビリティ修正 |
| `12-principles-of-animation` | アニメーション品質の監査 |
| `pptx` | スライド・プレゼン（.pptx の作成・編集・読み取り） |
| `pdf` | PDF の読み取り・結合・分割・フォーム入力など |
| `xlsx` | スプレッドシート（.xlsx/.csv の読み書き・編集） |
| `webapp-testing` | Playwright によるローカル Web アプリのテスト |
| `nano-banana` | 画像生成・編集（Gemini CLI の nanobanana 拡張経由） |

※ `baseline-ui`, `find-skills` は外部インストール（`~/.agents/skills/`）のため dotfiles 管理外。

**新規スキルを追加したら** `bash ~/dotfiles/claude/setup.sh` を実行し、`~/.claude/skills/` へシンボリックリンクを張り直すこと。

---

## MCP（Puppeteer）

Puppeteer MCP でブラウザ自動操作・スクリーンショット等を利用できる。

- **Claude Code**: `.claude.json` の `mcpServers.puppeteer` に `npx -y @modelcontextprotocol/server-puppeteer` で登録済み。ユーザー全体で有効にする場合は `claude mcp add puppeteer -s user -- npx -y @modelcontextprotocol/server-puppeteer` を実行してもよい。
- **Cursor**: このリポジトリの `.cursor/mcp.json` に Puppeteer を定義済み。この dotfiles を開いているワークスペースでは Cursor 再起動後に利用可能。全プロジェクトで使う場合は `~/.cursor/mcp.json` に同じ設定を追加する。

---

## セッション開始時のチェックリスト

1. `cat .claude/handover/*/summary.md` で前回の引き継ぎを確認（あれば）
2. `git log --oneline -5` で最新コミットを確認
3. タスクの depends-on に記載されたドキュメントを読む
