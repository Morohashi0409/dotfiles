# dotfiles 統合管理 実装計画

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** macOS ローカル環境の設定ファイルを `~/dotfiles` に集約し、シンボリックリンク + Git で管理する

**Architecture:** 既存の `~/dotfiles/claude/` はそのまま活かし、追加の設定ファイル（.zshrc, .gitconfig, .claude.json, Cursor, Obsidian）を `~/dotfiles` に移動。ルートに `setup.sh` を新設し全体のリンクを構築、Claude 固有は既存 `claude/setup.sh` に委任する。

**Tech Stack:** bash, ln, git, brew

---

## 現在の環境状態（事前確認済み）

- `~/dotfiles/` は存在するが Git 未初期化、`.gitignore` なし
- `~/dotfiles/claude/` に CLAUDE.md, settings.json, commands/, hooks/, setup.sh が既存
- `~/.zshrc` — 実ファイル
- `~/.gitconfig` — 実ファイル
- `~/.claude.json` — 実ファイル
- `~/.wezterm.lua` — 存在しない（スキップ）
- `~/Library/Application Support/Cursor/User/settings.json` — 実ファイル
- `~/Documents/Obsidian Vault/.obsidian/` — 実ディレクトリ
- `brew` — 利用可能

---

### Task 1: .gitignore の作成

**Files:**
- Create: `~/dotfiles/.gitignore`

**Step 1: .gitignore を作成**

```bash
cat > ~/dotfiles/.gitignore << 'EOF'
# Secrets
.env
*.pem
id_rsa*
*.key

# OS
.DS_Store
DS_Store

# Obsidian cache
config/obsidian/workspace.json
config/obsidian/workspace-mobile.json
EOF
```

**Step 2: 内容を確認**

Run: `cat ~/dotfiles/.gitignore`
Expected: 上記の内容が表示される

---

### Task 2: .zshrc を移動

**Files:**
- Move: `~/.zshrc` → `~/dotfiles/.zshrc`
- Create symlink: `~/.zshrc` → `~/dotfiles/.zshrc`

**Step 1: 現在の .zshrc が実ファイルであることを確認**

Run: `ls -la ~/.zshrc`
Expected: シンボリックリンクでない通常ファイル

**Step 2: .zshrc を dotfiles に移動**

```bash
mv ~/.zshrc ~/dotfiles/.zshrc
```

**Step 3: シンボリックリンクを作成**

```bash
ln -snf ~/dotfiles/.zshrc ~/.zshrc
```

**Step 4: リンクが正しいことを確認**

Run: `ls -la ~/.zshrc`
Expected: `~/.zshrc -> /Users/resily0808/dotfiles/.zshrc`

Run: `head -5 ~/.zshrc`
Expected: zshrc の内容が正しく読める

---

### Task 3: .gitconfig を移動

**Files:**
- Move: `~/.gitconfig` → `~/dotfiles/.gitconfig`
- Create symlink: `~/.gitconfig` → `~/dotfiles/.gitconfig`

**Step 1: .gitconfig を dotfiles に移動**

```bash
mv ~/.gitconfig ~/dotfiles/.gitconfig
```

**Step 2: シンボリックリンクを作成**

```bash
ln -snf ~/dotfiles/.gitconfig ~/.gitconfig
```

**Step 3: リンクが正しいことを確認**

Run: `ls -la ~/.gitconfig`
Expected: `~/.gitconfig -> /Users/resily0808/dotfiles/.gitconfig`

Run: `git config --global user.name`
Expected: Git 設定が正しく読める（エラーにならない）

---

### Task 4: .claude.json を移動

**Files:**
- Move: `~/.claude.json` → `~/dotfiles/.claude.json`
- Create symlink: `~/.claude.json` → `~/dotfiles/.claude.json`

**Step 1: .claude.json を dotfiles に移動**

```bash
mv ~/.claude.json ~/dotfiles/.claude.json
```

**Step 2: シンボリックリンクを作成**

```bash
ln -snf ~/dotfiles/.claude.json ~/.claude.json
```

**Step 3: リンクが正しいことを確認**

Run: `ls -la ~/.claude.json`
Expected: `~/.claude.json -> /Users/resily0808/dotfiles/.claude.json`

---

### Task 5: Cursor settings.json を移動

**Files:**
- Create dir: `~/dotfiles/config/cursor/`
- Move: `~/Library/Application Support/Cursor/User/settings.json` → `~/dotfiles/config/cursor/settings.json`
- Create symlink: 元のパス → `~/dotfiles/config/cursor/settings.json`

**Step 1: ディレクトリを作成し settings.json を移動**

```bash
mkdir -p ~/dotfiles/config/cursor
mv ~/Library/Application\ Support/Cursor/User/settings.json ~/dotfiles/config/cursor/settings.json
```

**Step 2: シンボリックリンクを作成**

```bash
ln -snf ~/dotfiles/config/cursor/settings.json ~/Library/Application\ Support/Cursor/User/settings.json
```

**Step 3: リンクが正しいことを確認**

Run: `ls -la ~/Library/Application\ Support/Cursor/User/settings.json`
Expected: シンボリックリンクが `~/dotfiles/config/cursor/settings.json` を指している

---

### Task 6: Obsidian .obsidian を移動

**Files:**
- Move: `~/Documents/Obsidian Vault/.obsidian` → `~/dotfiles/config/obsidian`
- Create symlink: 元のパス → `~/dotfiles/config/obsidian`

**注意:** Obsidian が起動中の場合は事前に終了すること。ディレクトリごとの移動なので、Obsidian がファイルをロックしていると失敗する可能性がある。

**Step 1: Obsidian が起動中でないことを確認**

Run: `pgrep -x Obsidian || echo "not running"`
Expected: `not running`（起動中なら終了を依頼）

**Step 2: .obsidian ディレクトリを dotfiles に移動**

```bash
mkdir -p ~/dotfiles/config
mv ~/Documents/Obsidian\ Vault/.obsidian ~/dotfiles/config/obsidian
```

**Step 3: シンボリックリンクを作成**

```bash
ln -snf ~/dotfiles/config/obsidian ~/Documents/Obsidian\ Vault/.obsidian
```

**Step 4: リンクが正しいことを確認**

Run: `ls -la ~/Documents/Obsidian\ Vault/.obsidian`
Expected: `.obsidian -> /Users/resily0808/dotfiles/config/obsidian`

Run: `ls ~/Documents/Obsidian\ Vault/.obsidian/app.json`
Expected: ファイルが読める（エラーにならない）

---

### Task 7: setup.sh の作成

**Files:**
- Create: `~/dotfiles/setup.sh`

**Step 1: setup.sh を作成**

```bash
#!/usr/bin/env bash
# setup.sh
# ~/dotfiles 内の設定ファイルを元のパスにシンボリックリンクとして配置する
#
# 使い方:
#   bash ~/dotfiles/setup.sh
#
# 安全対策:
#   - 既存の実ファイルはタイムスタンプ付きバックアップを作成してからリンク
#   - rm は使わず mv でバックアップ
#   - 親ディレクトリが無い場合は mkdir -p で作成

set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "$0")" && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}✓${NC} $*"; }
log_warn() { echo -e "${YELLOW}!${NC} $*"; }
log_skip() { echo -e "  - スキップ: $*"; }

backup_and_link() {
  local src="$1"
  local dst="$2"

  mkdir -p "$(dirname "$dst")"

  if [[ -L "$dst" ]]; then
    rm "$dst"
  elif [[ -e "$dst" || -d "$dst" ]]; then
    local backup="${dst}.bak_$(date +%Y%m%d_%H%M%S)"
    mv "$dst" "$backup"
    log_warn "バックアップ作成: $backup"
  fi

  ln -snf "$src" "$dst"
  log_ok "リンク: $dst → $src"
}

echo "=== dotfiles セットアップ ==="
echo "ソース: $DOTFILES_DIR"
echo ""

# 1. ホームディレクトリ直下のドットファイル
for file in .zshrc .gitconfig .claude.json .wezterm.lua; do
  src="$DOTFILES_DIR/$file"
  dst="$HOME/$file"
  if [[ -e "$src" ]]; then
    backup_and_link "$src" "$dst"
  else
    log_skip "$file（dotfiles 内に存在しない）"
  fi
done

# 2. Cursor settings.json
CURSOR_SRC="$DOTFILES_DIR/config/cursor/settings.json"
CURSOR_DST="$HOME/Library/Application Support/Cursor/User/settings.json"
if [[ -e "$CURSOR_SRC" ]]; then
  backup_and_link "$CURSOR_SRC" "$CURSOR_DST"
else
  log_skip "Cursor settings.json（dotfiles 内に存在しない）"
fi

# 3. Obsidian .obsidian ディレクトリ
OBSIDIAN_SRC="$DOTFILES_DIR/config/obsidian"
OBSIDIAN_DST="$HOME/Documents/Obsidian Vault/.obsidian"
if [[ -d "$OBSIDIAN_SRC" ]]; then
  backup_and_link "$OBSIDIAN_SRC" "$OBSIDIAN_DST"
else
  log_skip "Obsidian 設定（dotfiles 内に存在しない）"
fi

# 4. Claude 設定（既存の claude/setup.sh に委任）
CLAUDE_SETUP="$DOTFILES_DIR/claude/setup.sh"
if [[ -x "$CLAUDE_SETUP" ]]; then
  echo ""
  bash "$CLAUDE_SETUP"
else
  log_skip "claude/setup.sh（存在しないか実行権限なし）"
fi

echo ""
echo "=== セットアップ完了 ==="
```

**Step 2: 実行権限を付与**

```bash
chmod +x ~/dotfiles/setup.sh
```

**Step 3: 内容と権限を確認**

Run: `ls -la ~/dotfiles/setup.sh`
Expected: `-rwxr-xr-x` のパーミッション

Run: `head -10 ~/dotfiles/setup.sh`
Expected: shebang とコメントが表示される

---

### Task 8: Brewfile の生成

**Files:**
- Create: `~/dotfiles/Brewfile`

**Step 1: brew bundle dump を実行**

```bash
cd ~/dotfiles && brew bundle dump --force
```

**Step 2: Brewfile が生成されたことを確認**

Run: `wc -l ~/dotfiles/Brewfile`
Expected: 行数が表示される（0 でない）

Run: `head -10 ~/dotfiles/Brewfile`
Expected: tap, brew, cask などのエントリが表示される

---

### Task 9: Git 初期化とコミット

**Files:**
- Init: `~/dotfiles/.git`

**Step 1: git init**

```bash
cd ~/dotfiles && git init
```

**Step 2: .gitignore が機能していることを確認**

Run: `cd ~/dotfiles && git status`
Expected: `.DS_Store` や `workspace.json` がリストに現れない

**Step 3: 全ファイルをステージング**

```bash
cd ~/dotfiles && git add -A
```

**Step 4: ステージング内容を確認**

Run: `cd ~/dotfiles && git status`
Expected: 全管理対象ファイルが staged。機密ファイルや `.DS_Store` が含まれていないこと

**Step 5: コミット**

```bash
cd ~/dotfiles && git commit -m "Initial commit: Set up dotfiles structure"
```

**Step 6: コミット結果を確認**

Run: `cd ~/dotfiles && git log --oneline -1`
Expected: `Initial commit: Set up dotfiles structure`

---

## 完了後の確認チェックリスト

- [ ] `~/.zshrc` がシンボリックリンクで `~/dotfiles/.zshrc` を指している
- [ ] `~/.gitconfig` がシンボリックリンクで `~/dotfiles/.gitconfig` を指している
- [ ] `~/.claude.json` がシンボリックリンクで `~/dotfiles/.claude.json` を指している
- [ ] Cursor の `settings.json` がシンボリックリンクで dotfiles を指している
- [ ] `~/Documents/Obsidian Vault/.obsidian` がシンボリックリンクで dotfiles を指している
- [ ] `~/dotfiles/.gitignore` が存在し、機密ファイルを除外している
- [ ] `~/dotfiles/setup.sh` が実行可能で、新しい環境でリンクを再構築できる
- [ ] `~/dotfiles/Brewfile` が存在する
- [ ] `git log` で初回コミットが確認できる
- [ ] シェルを新しいタブで開いて `.zshrc` が正しく読み込まれる
