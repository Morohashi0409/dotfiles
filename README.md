# dotfiles

macOS 上で **Claude Code / Codex CLI / Cursor / WezTerm / Obsidian / zsh** をまとめて運用するための個人 dotfiles です。
`setup.sh` を 1 度実行すれば、各ツールの設定ファイル・コマンド・skill・hook が `$HOME` 配下にシンボリックリンクで展開されます。

> このリポジトリは作者個人の環境（パス・プロジェクト名・Obsidian Vault 構成）に依存しています。
> そのまま fork する場合は、後述の「[ユーザーが準備すべきもの](#ユーザーが準備すべきもの)」と「[個人設定の置換えポイント](#個人設定の置換えポイント)」を必ずチェックしてください。

---

## 目次

- [全体像](#全体像)
- [前提環境](#前提環境)
- [ディレクトリ構成](#ディレクトリ構成)
- [セットアップ手順](#セットアップ手順)
- [各ツールの設定内容](#各ツールの設定内容)
  - [Claude Code](#claude-code)
  - [Codex CLI](#codex-cli)
  - [Cursor](#cursor)
  - [WezTerm](#wezterm)
  - [Obsidian](#obsidian)
  - [zsh](#zsh)
  - [ccstatusline](#ccstatusline)
- [Claude Code マルチプロファイル運用](#claude-code-マルチプロファイル運用)
- [ユーザーが準備すべきもの](#ユーザーが準備すべきもの)
- [個人設定の置換えポイント](#個人設定の置換えポイント)
- [機密情報の扱い](#機密情報の扱い)

---

## 全体像

```
~/dotfiles ── setup.sh ──┬─► ~/.zshrc, ~/.gitconfig などの共通設定
                          ├─► ~/.claude/         (Claude Code: CLAUDE.md / commands / hooks / skills)
                          ├─► ~/.codex/          (Codex CLI hooks)
                          ├─► ~/.cursor/         (Cursor: rules / 共有 skill)
                          ├─► ~/.config/wezterm/ (WezTerm 設定)
                          ├─► ~/Library/Application Support/Cursor/User/ (Cursor settings.json)
                          └─► ~/Documents/Obsidian Vault/.obsidian/ (Obsidian 設定)
```

特徴:

- **Claude Code と Codex CLI で同じ Obsidian AI-OS スキルを共有**（実体は `claude/skills/`、Codex 側は symlink）
- **Cursor も同じ 3 スキル（`read-project-memory` / `log-feedback` / `thread-memory`）を symlink で共有**
- **マルチプロファイル対応**: 個人ライセンスと組織ライセンスを `CLAUDE_CONFIG_DIR` で切替

---

## 前提環境

| 種別 | 推奨バージョン / 備考 |
|---|---|
| OS | macOS（Darwin）。Linux でも一部は動作するが symlink 先パスを調整する必要あり |
| シェル | zsh（macOS の既定）|
| パッケージ管理 | Homebrew（`Brewfile` あり）|
| Node.js | v18+ （Claude Code / Codex CLI が依存）|
| Python | 3.11+ （Codex hooks / CloudLog skill が依存）|
| Git | 2.40+ |

必須・任意のツール:

| ツール | 用途 | 必須度 |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) | AI コーディング CLI | ★必須 |
| [Codex CLI](https://github.com/openai/codex) | ChatGPT 連携 CLI（OpenAI 公式）| 任意（codex hooks を使うなら必須）|
| [Cursor](https://cursor.com/) | AI コードエディタ | 任意 |
| [WezTerm](https://wezfurlong.org/wezterm/) | ターミナルエミュレータ | 任意 |
| [Obsidian](https://obsidian.md/) | メモ・ナレッジ管理（AI-OS 連携に使用）| ★Obsidian 連携を使うなら必須 |

---

## ディレクトリ構成

```
dotfiles/
├── README.md                  # このファイル
├── setup.sh                   # トップレベルのセットアップ（各 setup.sh を順に呼ぶ）
├── .zprofile, .gitconfig      # zsh / git のグローバル設定
├── changelog.config.js        # コミット ChangeLog 設定
├── Brewfile                   # Homebrew でインストールするツール
│
├── claude/                    # Claude Code 用
│   ├── setup.sh               #   ~/.claude/ への symlink 展開（--profile / --all 対応）
│   ├── CLAUDE.md              #   グローバル運用ガイドライン（言語・コミット規律など）
│   ├── settings.json          #   プラグイン・hook・テーマ等のグローバル設定
│   ├── commands/              #   /handover, /continue, /commit など Claude 用 slash コマンド
│   ├── hooks/                 #   Stop hook 等のシェルスクリプト
│   └── skills/                #   30+ の skill（後述）
│
├── codex/                     # Codex CLI 用
│   ├── setup.sh               #   ~/.codex/ への symlink 展開
│   └── hooks/                 #   SessionStart / UserPromptSubmit / Stop に対応する Python hook
│
├── cursor/                    # Cursor 用
│   ├── setup.sh               #   ~/.cursor/ への symlink 展開
│   └── rules/00-global.mdc    #   alwaysApply グローバルルール（日本語運用・AI-OS 参照）
│
├── config/
│   ├── cursor/settings.json   # Cursor 本体の settings.json
│   ├── wezterm/wezterm.lua    # WezTerm 設定（テーマ・フォント・launch_menu）
│   └── obsidian/              # Obsidian Vault の .obsidian/ 一式（コミュニティプラグイン・ホットキー等）
│
├── ccstatusline/settings.json # Claude Code ステータスラインの表示設定
│
├── zsh/                       # zsh から source される関数
│   ├── claude-profiles.zsh    #   claude-personal / claude-arm の起動関数
│   └── workspaces.zsh         #   dxp / wellcom / dotfiles など、cd ヘルパー + wz 起動
│
├── docs/                      # 詳細ドキュメント・設計メモ・監査ノート
├── skills-lock.json           # 外部 skill (canvas-design / polish) のバージョンロック
└── tests/                     # スキル・スクリプトのテスト
```

> **`.agents/` / `.kiro/` / `.claude/` はリポジトリに含まれません。**
> Claude Code および Kiro が `skills-lock.json` を元に自動で `~/dotfiles/.agents/skills/`
> 配下に外部 skill を取得します（再現性は lock ファイルで担保）。

---

## セットアップ手順

### 1. リポジトリを clone

```bash
git clone https://github.com/<your-fork>/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

### 2. 必要ツールをインストール

```bash
brew bundle --file Brewfile
npm install -g @anthropic-ai/claude-code
npm install -g @openai/codex   # 任意（Codex hooks を使うなら）
```

### 3. zsh から関数を読み込めるようにする

`~/.zshrc` に以下を追記（`~/.zshrc` 自体は機密性が高いので dotfiles では管理していません）:

```bash
# dotfiles の関数を読み込む
[[ -f "$HOME/dotfiles/zsh/claude-profiles.zsh" ]] && source "$HOME/dotfiles/zsh/claude-profiles.zsh"
[[ -f "$HOME/dotfiles/zsh/workspaces.zsh"      ]] && source "$HOME/dotfiles/zsh/workspaces.zsh"
```

### 4. setup.sh を実行

```bash
bash ~/dotfiles/setup.sh
```

これで以下が展開されます:

- `~/.gitconfig` / `~/.zprofile` / `~/changelog.config.js`
- `~/.config/wezterm/wezterm.lua`
- `~/Library/Application Support/Cursor/User/settings.json`
- `~/Documents/Obsidian Vault/.obsidian/`（既存があれば自動バックアップ）
- `~/.claude/` 一式（`claude/setup.sh` 経由）
- `~/.codex/` 一式（`codex/setup.sh` 経由）

> ⚠️ `~/.claude.json` は Claude Code のランタイム状態（OAuth トークン・会話履歴・MCP サーバー定義など）を含むため、**意図的に管理対象外**にしています。そのまま Claude Code が自動生成・更新します。

### 5. Cursor の rules / 共有 skill を展開

```bash
bash ~/dotfiles/cursor/setup.sh
```

Cursor を再起動すれば `~/.cursor/rules/00-global.mdc` と `~/.cursor/skills-cursor/` が反映されます。

---

## 各ツールの設定内容

### Claude Code

- **CLAUDE.md**: 全プロジェクト共通の運用ガイドライン（日本語出力・Intent Guard・コンテキスト管理・Obsidian AI-OS 連携など）
- **commands/**: `handover`, `continue`, `commit`, `review`, `pre-review`, `doc-check`, `create-command`, `github-issue-organize` ほか
- **skills/**: ドキュメント・画像・動画・SNS・Dify・CloudLog・RASHISA など 30+ の skill
- **hooks/**: Stop hook で Obsidian にセッションログを自動記録

詳細は [`claude/CLAUDE.md`](claude/CLAUDE.md) を参照。

### Codex CLI

`~/.codex/config.toml` の hooks 設定から、`codex/hooks/` 配下の Python スクリプトが呼ばれます:

| イベント | スクリプト | 役割 |
|---|---|---|
| `SessionStart` | `session_start_read_project_memory.py` | Obsidian AI-OS の Global / Rules / Feedback を読み込む |
| `UserPromptSubmit` | `user_prompt_log_feedback.py` | 訂正フレーズ検知時に Feedback.md へ追記 |
| `Stop` | `stop_thread_memory.py` | セッション末尾で feedback / rules / learnings を仕分けて追記 |

Codex 側の skill 実体は `claude/skills/{read-project-memory,log-feedback,thread-memory}/` を symlink で共有しています（Claude と完全に同一）。

### Cursor

- `cursor/rules/00-global.mdc`: `alwaysApply: true` のグローバルルール
- `~/.cursor/skills-cursor/`: Claude の 3 つの AI-OS skill を symlink で共有
- `config/cursor/settings.json`: Cursor 本体の settings（フォント・remote.SSH のプラットフォーム指定など）

### WezTerm

`config/wezterm/wezterm.lua` に以下を定義:

- カラーテーマ（Tokyo Night）
- フォント（JetBrains Mono → Hack Gen → Menlo）
- ウィンドウ透過 0.85 / macOS ブラー
- `launch_menu`: ⌘+Shift+L で開くプロジェクトランチャー（dxp / wellcom / dotfiles など）

> `launch_menu` のパスはコード内で直書きされています。自分の環境に合わせて編集してください（[個人設定の置換えポイント](#個人設定の置換えポイント)参照）。

### Obsidian

`config/obsidian/` を `~/Documents/Obsidian Vault/.obsidian/` に symlink します。
含まれる主な設定:

- `community-plugins.json`: 使用するコミュニティプラグイン一覧
- `hotkeys.json`: ホットキー（例: `Mod+Shift+V` = Remove Newlines paste）
- `plugins/`: Soundscapes / Remove Newlines 等の設定
- `app.json`, `appearance.json`, `core-plugins.json` 等

> Obsidian Vault のパスが異なる場合は `setup.sh` 内の `~/Documents/Obsidian Vault` を編集してください。

### zsh

`~/.zshrc` から source される 2 ファイル:

| ファイル | 内容 |
|---|---|
| `zsh/claude-profiles.zsh` | `claude-personal` / `claude-arm` 関数。`CLAUDE_CONFIG_DIR` を切り替えて起動 |
| `zsh/workspaces.zsh`      | `dxp` / `wellcom` / `dotfiles` 関数。`wz <name>` で WezTerm を該当ディレクトリで起動 |

ワークスペースを追加する場合は `WORKSPACES` 連想配列にエントリを追加するだけで cd 関数と `wz` 補完が自動で生えます。

### ccstatusline

`ccstatusline/settings.json`: Claude Code のステータスライン表示（モデル名・コンテキスト残量・git ブランチ・変更件数）。
`setup.sh` 実行時に `~/.config/ccstatusline/settings.json` に symlink されます。

---

## Claude Code マルチプロファイル運用

複数の Anthropic アカウントを切り替えるために `CLAUDE_CONFIG_DIR` を使い分けます。
**dotfiles の symlink は両方のプロファイルに張られるため、CLAUDE.md / skills / commands / hooks / settings.json は共通で適用されます。**

| プロファイル | 起動コマンド | `CLAUDE_CONFIG_DIR` |
|---|---|---|
| personal（個人ライセンス）| `claude` または `claude-personal` | `~/.claude/`（既定）|
| arm（組織ライセンス例）  | `claude-arm`                     | `~/.claude-config/arm/` |

### 新規プロファイル追加

```bash
# 1. dotfiles の symlink をプロファイル先に展開
bash ~/dotfiles/claude/setup.sh --profile <name>

# 2. zsh/claude-profiles.zsh に起動関数を追記
#    （personal / arm は既に定義済み）

# 3. 起動 → /login で認証
claude-<name>
```

詳細は [`claude/CLAUDE.md`](claude/CLAUDE.md) の「アカウント管理（マルチプロファイル）」セクションを参照。

---

## ユーザーが準備すべきもの

このリポジトリを別マシンや別ユーザーで動かす場合、以下を**自分で用意・置換え**する必要があります。

### 必須

1. **Anthropic アカウント** — Claude Code の `/login` で認証
2. **Homebrew** + `Brewfile` のインストール
3. **`~/.zshrc`** — 自分のマシン固有設定（dotfiles では管理しない）
4. **`~/.claude.json`** — Claude Code が自動生成する。手動コピーは不可（OAuth トークン等を含むため）

### Obsidian AI-OS 連携を使う場合

Obsidian Vault の以下のディレクトリ構造を準備:

```
~/Documents/Obsidian Vault/
└── 00_AI-OS/
    ├── Global.md                          # 全プロジェクト共通の品質基準・禁止事項
    ├── 00_Guide.md                        # 人間向け運用ガイド
    └── Projects/
        ├── _Template/                     # 新規プロジェクトのひな形
        └── <project-name>/
            ├── Rules.md                   # プロジェクト固有のルール
            └── Feedback.md                # newest-on-top の指摘ログ
```

- 起点ファイル（`Global.md`, `00_Guide.md`）は最初に手書きする
- 各プロジェクト追加時に `_Template` をコピーして `Projects/<project-name>/` を作る
- AI のセッション中に `read-project-memory` / `log-feedback` / `thread-memory` が自動で読み書きする

### Codex CLI を使う場合

```bash
# インストール
npm install -g @openai/codex

# 認証（ChatGPT または API key）
codex login

# Claude Code 内から状態確認
/codex:setup
```

### Cursor を使う場合

- Cursor をインストール → `cursor/setup.sh` を実行
- 必要に応じて `~/.cursor/mcp.json` に MCP サーバーを追加（Puppeteer など）

### WezTerm を使う場合

- WezTerm をインストール（`brew install --cask wezterm`）
- `config/wezterm/wezterm.lua` の `launch_menu` のパスを自分のプロジェクトに合わせて編集

---

## 個人設定の置換えポイント

このリポジトリには作者の個人パス・プロジェクト名が一部直書きされています。fork して使う場合は次の箇所を編集してください:

| ファイル | 直書きされている値 | 置換え方針 |
|---|---|---|
| `config/wezterm/wezterm.lua` | `cwd = '/Users/.../dxp/dxp-2/dxp'` 等 | 自分のプロジェクトディレクトリに変更 |
| `zsh/workspaces.zsh` | `WORKSPACES` 連想配列 | 自分の作業ディレクトリに変更 |
| `claude/CLAUDE.md` | `/Users/.../Documents/Obsidian Vault` | 自分の Vault パスに変更 |
| `cursor/rules/00-global.mdc` | 同上 | 同上 |
| `codex/hooks/ai_os_memory.py` | 同上 | 同上 |
| `claude/skills/cloudlog-monthly/` | CloudLog の社内 URL / Vault パス | 自社固有のためスキルごと除外することを推奨 |
| `claude/skills/rasisa-*` | RASHISA プロジェクト固有 | 不要なら skills/ から削除 |
| `claude/skills/benchmark-data-refresh/` | WellCom 社内固有 | 不要なら削除 |

> 将来的に環境変数（例: `OBSIDIAN_VAULT_ROOT`）で抽象化することを検討中。

---

## 機密情報の扱い

`.gitignore` で以下を追跡対象から外しています:

- `.zshrc` （マシン固有・API キー混入の可能性）
- `.env`, `*.pem`, `id_rsa*`, `*.key`
- **`.claude.json`** — Claude Code のランタイム状態。`oauthAccount`（emailAddress / accountUuid）、`userID`、MCP サーバー定義、プロジェクト履歴、会話統計を含むため絶対に共有しません
- **`.claude/`** — ローカルキャッシュ（`handover/` / `settings.local.json` / プロジェクト固有 skill 等）
- **`.agents/`, `.kiro/`** — Claude Code / Kiro が外部から取得する skill のローカルキャッシュ。`skills-lock.json` で版を固定しているので Claude Code 起動時に自動再取得されます
- `__pycache__/`, `*.py[cod]`
- `.DS_Store`
- `config/obsidian/workspace.json`, `workspace-mobile.json`
- `config/obsidian/plugins/obsidian-textgenerator-plugin/data.json`（API キー）

### コミット前のチェックリスト

新しい設定ファイルを dotfiles に追加するときは:

1. **API キー・トークンが含まれていないか** `grep -iE 'api[_-]?key|secret|token|password|bearer'` で確認
2. **個人パス**（例: `/Users/yourname/...`）を可能な限り `$HOME` や環境変数に置換
3. **Email アドレス / UUID**（OAuth / アカウント情報）が含まれていないか
4. 必要に応じて `.gitignore` を更新

---

## ライセンス

個人 dotfiles のため明示的なライセンスはありませんが、参考にしたい部分があれば自由にコピー・改変してください。
