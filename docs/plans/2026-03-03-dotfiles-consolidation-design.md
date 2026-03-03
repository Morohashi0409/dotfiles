# dotfiles 統合管理 設計ドキュメント

## 概要

macOS ローカル環境に散らばっている設定ファイルを `~/dotfiles` リポジトリに集約し、Git で管理する。
シンボリックリンクにより、元のパスから dotfiles 内の実体を参照する構成とする。

## 管理対象

| ファイル | 元のパス | dotfiles 内のパス |
|---------|---------|------------------|
| `.zshrc` | `~/.zshrc` | `~/dotfiles/.zshrc` |
| `.gitconfig` | `~/.gitconfig` | `~/dotfiles/.gitconfig` |
| `.claude.json` | `~/.claude.json` | `~/dotfiles/.claude.json` |
| `.wezterm.lua` | `~/.wezterm.lua` | スキップ（存在しない） |
| Cursor settings | `~/Library/Application Support/Cursor/User/settings.json` | `~/dotfiles/config/cursor/settings.json` |
| Obsidian 設定 | `~/Documents/Obsidian Vault/.obsidian` | `~/dotfiles/config/obsidian/` |
| Claude 設定 | `~/.claude/` 配下 | `~/dotfiles/claude/`（既存） |

## ディレクトリ構造

```
~/dotfiles/
├── .gitignore
├── setup.sh                    # 全体のシンボリックリンク構築
├── Brewfile                    # Homebrew パッケージリスト
├── .zshrc
├── .gitconfig
├── .claude.json
├── config/
│   ├── cursor/
│   │   └── settings.json
│   └── obsidian/               # .obsidian の内容
├── claude/                     # 既存
│   ├── CLAUDE.md
│   ├── settings.json
│   ├── commands/
│   ├── hooks/
│   └── setup.sh
├── ccstatusline/               # 既存
└── docs/plans/
```

## .gitignore

```
.env
*.pem
id_rsa*
*.key
.DS_Store
DS_Store
config/obsidian/workspace.json
config/obsidian/workspace-mobile.json
```

## setup.sh の設計

- 既存ファイルがシンボリックリンクでない場合、タイムスタンプ付きバックアップを作成
- `mkdir -p` で親ディレクトリを事前に作成
- `ln -snf` でシンボリックリンクを構築
- Obsidian は `.obsidian` ディレクトリ自体をシンボリックリンクで置き換え
- 最後に `claude/setup.sh` を呼び出して Claude 関連のリンクも構築

## 安全対策

- `rm` は一切使わない。すべて `mv` でバックアップ
- `.wezterm.lua` は存在チェックで分岐しスキップ
- 各操作前に宣言、操作後に結果報告

## 実行順序

1. `.gitignore` 作成
2. ファイル移動
3. `setup.sh` 作成 + `chmod +x`
4. `brew bundle dump` で Brewfile 生成
5. `git init` + 初回コミット
