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
| `/create-command` | 新規コマンドを dotfiles に追加 |
| `/github-issue-organize` | PRコメントの整理・記録 |
| `/obsidian-log` | 会話セッションを Obsidian に記録・デイリーノートへリンク |

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
| `portable-skills` | Claude/Codex 両対応の skill 作成・更新・監査 |
| `rasisa-x-posting` | RASHISA の X 投稿作成・添削（x-impact-checker + nano-banana） |
| `rasisa-note-writing` | RASHISA の note 記事作成（タイプ解説・統計・活用法） |
| `rasisa-youtube-shorts` | RASHISA の YouTube Shorts / TikTok 動画作成 |
| `read-project-memory` | 着手前に Obsidian AI-OS の Global.md / Rules.md / Feedback.md を読み込む |
| `log-feedback` | 会話中の訂正を即座に Projects/<project>/Feedback.md（5タグ付き）の最上部に記録 |
| `thread-memory` | 会話末尾に feedback/rules/learnings を仕分けて Feedback.md / Rules.md / Global.md へ追記 |
| `obsidian-log` | 会話要約を Obsidian 05_Claude-Log/ に記録し、デイリーノートへリンク |
| `wezterm-config` | WezTerm 設定と zsh ワークスペース (`dxp`/`wellcom`/`dotfiles` 等) の追加・改修リファレンス |

※ `baseline-ui`, `find-skills`, `x-impact-checker`, `remotion-best-practices` は外部インストール（`~/.agents/skills/`）のため dotfiles 管理外。

**新規スキルを追加したら** `bash ~/dotfiles/claude/setup.sh` を実行し、`~/.claude/skills/` へシンボリックリンクを張り直すこと。

---

## アカウント管理（マルチプロファイル）

複数の Anthropic アカウント（個人ライセンス・ARM 社内ライセンス等）を `CLAUDE_CONFIG_DIR` でディレクトリ分離する運用。認証情報・履歴・todos などはプロファイル毎に独立し、CLAUDE.md / skills / commands / hooks / settings.json は dotfiles の symlink で共通化される。

### プロファイル

| プロファイル | 起動コマンド | CLAUDE_CONFIG_DIR |
|---|---|---|
| personal（個人ライセンス） | `claude` または `claude-personal` | `~/.claude/`（既定） |
| arm（社内ライセンス） | `claude-arm` | `~/.claude-config/arm/` |

引数はすべて `claude` 本体にそのまま forward される:

```bash
claude-arm --dangerously-skip-permissions
claude-arm --model claude-sonnet-4-6
claude-arm /status
```

### 起動中のアカウント確認

```bash
/status        # 起動中の Claude Code 内で実行 → 認証アカウントが表示される
```

### 新規プロファイル追加手順

```bash
# 1. dotfiles の symlink をプロファイル先に展開
bash ~/dotfiles/claude/setup.sh --profile <name>

# 2. 関数を追加（personal 用 / arm 用は既に dotfiles/zsh/claude-profiles.zsh に定義済み）
#    新規プロファイルが必要なら同ファイルに claude-<name>() を追記

# 3. ログイン
claude-<name>     # 起動 → /login で当該アカウント認証
```

### 注意

- `settings.local.json` はマシン固有のため symlink 化していない。プロファイル別に必要なら手動作成する。
- MCP の認証キャッシュ（Figma / Gmail / Drive 等）はプロファイル別。ARM 側で初回利用時は再認証が必要。
- 既存 symlink を一括更新する場合は `bash ~/dotfiles/claude/setup.sh --all`。

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

---

## Obsidian AI-OS 自動参照（認識齟齬と反復指摘の防止）

Obsidian Vault `00_AI-OS/` は「作業前に読む情報」と「作業後に追記する情報」を管理している領域。
以下 4 スキルを段階的に自動起動させ、同じ指摘の再発を防ぐ。

| タイミング | スキル | 役割 |
|---|---|---|
| **着手直前** | `read-project-memory` | `Global.md` / `Projects/<project>/Rules.md` / `Feedback.md` を読み、遵守3点・禁止3点を提示 |
| **会話中（訂正時）** | `log-feedback` | ユーザーの「違う」「〜しないで」等を検知し、`Projects/<project>/Feedback.md` の最上部に5タグ付きで追記 |
| **会話末尾（明示 or 持続作業後）** | `thread-memory` | feedback / rules / learnings を仕分けて `Feedback.md` / `Rules.md` / `Global.md` へ追記 |
| **会話末尾（毎回）** | `obsidian-log` | 会話要約を `05_Claude-Log/` に記録しデイリーノートへリンク |

### 動作規範

- `read-project-memory` は実作業（実装・設計・デバッグ・編集・調査）の**最初のアクション前**に 1 回だけ起動。挨拶・雑談・単発 Q&A では起動しない。
- `log-feedback` は検知精度を優先し、誤検知したら黙って本題を続ける（ユーザーに確認しない）。
- `thread-memory` は `log-feedback` が既に書いた指摘を重複チェックで skip するため、両方走らせて良い。
- ユーザーが「読まなくていい」「スキップ」と明言した場合は `read-project-memory` を起動しない。

### Vault の絶対パス

- Root: `/Users/resily0808/Documents/Obsidian Vault`
- AI-OS: `00_AI-OS/`
  - `Global.md`（全プロジェクト共通）
  - `Projects/<project>/Rules.md` `Feedback.md`（プロジェクト固有）
  - `00_Guide.md`（人間向け運用ガイド）

---

## Obsidian セッション記録（毎回必須）

**実質的な作業（コード変更・設計・調査など）を行ったセッションの末尾で必ず `/obsidian-log` を実行すること。**

- Stop hook が自動で最小エントリを `05_Claude-Log/` に作成する
- `/obsidian-log` を実行することでLLM要約（キーポイント・変更ファイル）に上書き更新される
- ユーザーが「記録して」「ログ残して」と言った場合も `/obsidian-log` を実行する
- 挨拶や雑談のみのセッションはスキップしてよい

---

## Cursor との共通運用（Obsidian AI-OS 3 スキルを共有）

Cursor Agent も同じ Obsidian AI-OS 連携を動かすため、`~/dotfiles/cursor/` を新設して symlink で共有する。

### 配置

| 種別 | dotfiles | symlink 先 |
|---|---|---|
| 共通ルール（alwaysApply） | `cursor/rules/00-global.mdc` | `~/.cursor/rules/00-global.mdc` |
| 共有スキル（3 種） | `claude/skills/{read-project-memory,log-feedback,thread-memory}/` | `~/.cursor/skills-cursor/<name>/` |

- SKILL.md は Claude と完全に同じ実体を symlink で共有（統一）
- `obsidian-log` は Cursor 側では使わないため symlink しない

### セットアップ

```bash
bash ~/dotfiles/cursor/setup.sh
```

- `~/.cursor/rules/` と `~/.cursor/skills-cursor/` に symlink を展開
- 既存ファイルは `*.bak.YYYYMMDD_HHMMSS` にバックアップしてから上書き
- Cursor を再起動して反映

### 新規共有スキルを追加する手順

1. `~/dotfiles/claude/skills/<name>/SKILL.md` を作成（Claude と共通）
2. `~/dotfiles/cursor/setup.sh` の `OBSIDIAN_SKILLS` 配列に `<name>` を追加
3. `bash ~/dotfiles/cursor/setup.sh` で symlink を張り直し
