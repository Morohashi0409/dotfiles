---
name: wezterm-config
description: Use when adding or editing WezTerm settings managed in this dotfiles repo — launcher menu items, key bindings, color/font/window options, or zsh workspace shortcuts (dxp / wellcom / dotfiles / 新規プロジェクト). Triggers include 「ワークスペース追加」「新しいプロジェクト先を作って」「WezTerm のキーバインド変えて」「ランチャーに〜を追加」「wz で〜に飛べるように」「ターミナルのフォント変えて」, or any direct edit to ~/dotfiles/zsh/workspaces.zsh or ~/dotfiles/config/wezterm/wezterm.lua.
---

# wezterm-config

このリポジトリで管理している WezTerm 設定と、それと連動した zsh ワークスペース機能を安全に拡張・改修するためのリファレンス。

## Overview

WezTerm 設定はホーム直下ではなく `~/dotfiles/config/wezterm/wezterm.lua` を実体とし、`~/.config/wezterm/wezterm.lua` から symlink で参照されている。`setup.sh` の `backup_and_link` がリンクを張る役割を持ち、symlink を介して dotfiles の変更が即座に反映される。

zsh 側のショートカット (`dxp` / `wellcom` / `dotfiles` / `wz <name>`) は `~/dotfiles/zsh/workspaces.zsh` の `WORKSPACES` 連想配列で一元定義されており、cd 関数は動的生成、`wz` の tab 補完も自動で連動する。**ワークスペースを増やすときは zsh 側の `WORKSPACES` と WezTerm 側の `launch_menu` を必ずペアで更新する**。これが唯一の不変条件。

## When to Use

- 新しいプロジェクトディレクトリへの cd ショートカット / `wz` での起動を追加・変更したい
- WezTerm のキーバインド・カラースキーム・フォント・透明度・タブバー設定を変えたい
- ランチャーメニュー (`Cmd+Shift+L`) の項目を追加・削除したい
- 既存ワークスペースのパスが変わった、名前を変えたい
- WezTerm 設定が反映されない / symlink がおかしいと感じた
- `wz` コマンドや `dxp` / `wellcom` / `dotfiles` が見つからない・動かない

**Do NOT use when:**
- 他のターミナル (iTerm2, Terminal.app, Alacritty) の設定変更 → 別タスク
- 一時的な環境変数や PATH 追加 → `~/dotfiles/.zshrc` を直接編集（このスキルの範囲外）
- Claude Code のプロファイル切替 (`claude-arm` 等) → `~/dotfiles/zsh/claude-profiles.zsh` 側、別スキル

## ファイル構成（不変）

| 役割 | 実体 | symlink / 参照元 |
|------|------|------------------|
| WezTerm 本体設定 | `~/dotfiles/config/wezterm/wezterm.lua` | `~/.config/wezterm/wezterm.lua` |
| zsh ワークスペース定義 | `~/dotfiles/zsh/workspaces.zsh` | `~/dotfiles/.zshrc` から source |
| zsh 本体 | `~/dotfiles/.zshrc` | `~/.zshrc` |
| symlink 反映スクリプト | `~/dotfiles/setup.sh` | — |

`~/.wezterm.lua` は使わない（過去の残骸があれば削除可）。実体は必ず `~/.config/wezterm/wezterm.lua` 経由。

## Quick Reference

### ワークスペース追加（最頻ケース）

2 ファイルをペアで編集 → setup.sh 不要（symlink 済みのため即反映）。

**Step 1.** `~/dotfiles/zsh/workspaces.zsh` の `WORKSPACES` に1行追加:
```zsh
typeset -gA WORKSPACES=(
  dxp      "/Users/resily0808/dxp/dxp-2/dxp"
  wellcom  "$HOME/WrllCom_front2025/WellCom_front"
  dotfiles "$HOME/dotfiles"
  myproj   "$HOME/path/to/myproj"          # ← 追加
)
```
キー名はそのまま cd 関数名 / `wz` のサブコマンドになる。zsh 予約語 (`cd`, `ls`, `cd` 等) と衝突する名前は避ける。

**Step 2.** `~/dotfiles/config/wezterm/wezterm.lua` の `launch_menu` に同じ項目を追加:
```lua
config.launch_menu = {
  { label = 'dxp',      args = { SHELL, '-l' }, cwd = '/Users/resily0808/dxp/dxp-2/dxp' },
  { label = 'wellcom',  args = { SHELL, '-l' }, cwd = HOME .. '/WrllCom_front2025/WellCom_front' },
  { label = 'dotfiles', args = { SHELL, '-l' }, cwd = HOME .. '/dotfiles' },
  { label = 'myproj',   args = { SHELL, '-l' }, cwd = HOME .. '/path/to/myproj' },  -- ← 追加
}
```
`label` は zsh の `WORKSPACES` キーと一致させると CLI / GUI 体験が揃う。

**Step 3.** 反映:
- 開いている zsh セッションでは `exec zsh` で再読み込み
- WezTerm は GUI 操作不要（ファイル保存時に自動再読み込み）。反映しない場合は WezTerm の `Cmd+Shift+R` (Reload Configuration)

### ワークスペース削除 / リネーム

- `WORKSPACES` から該当行を削除（または key を rename）
- `launch_menu` から該当 entry を削除（または `label` を rename）
- 削除した名前で開いている関数は `unfunction <name>` で同セッション中も即消せる

### キーバインド追加

`wezterm.lua` の `config.keys = { ... }` 配列に追記:
```lua
{ key = 't', mods = 'SUPER|SHIFT', action = act.SpawnTab 'CurrentPaneDomain' },
```
- `mods`: `SUPER`(Cmd), `SHIFT`, `ALT`(Option), `CTRL`, `|` で複数
- `action`: `wezterm.action.XXX` の一覧は `wezterm show-keys` か WezTerm 公式 keyassignment ドキュメント参照
- 既存 macOS ショートカット (Cmd+C/V/W/F 等) と衝突しないか確認

### 見た目の変更

`wezterm.lua` 冒頭セクション「1. 見た目の設定」のキーを書き換える:
| キー | 役割 | 値の例 |
|------|------|--------|
| `config.color_scheme` | カラーテーマ | `'Tokyo Night'`, `'Catppuccin Mocha'`, `'Dracula'` ほか組み込み多数 |
| `config.font` | フォント | `wezterm.font_with_fallback { 'JetBrains Mono', 'Hack Gen' }` |
| `config.font_size` | サイズ | `14.0` |
| `config.window_background_opacity` | 透明度 | `0.0`〜`1.0` |
| `config.macos_window_background_blur` | 背景ぼかし | `0`〜`100` |
| `config.window_decorations` | タイトルバー | `"RESIZE"` (なし) / `"TITLE \| RESIZE"` (あり) |

## 反映方法

| 変更箇所 | 反映タイミング | 手動操作 |
|----------|----------------|----------|
| `workspaces.zsh` | 次回 zsh 起動 | 既存セッションは `exec zsh` |
| `wezterm.lua` | 保存時に自動 | 効かない時のみ WezTerm で `Cmd+Shift+R` |
| symlink が壊れた | — | `bash ~/dotfiles/setup.sh` |

新規マシンや symlink が消えた場合のみ `bash ~/dotfiles/setup.sh` を実行する。日常編集では setup.sh 不要。

## 検証

変更後にこれを走らせれば、cd / wz / symlink すべて確認できる:
```bash
zsh -i -c '
  source ~/dotfiles/zsh/workspaces.zsh
  for k in "${(@k)WORKSPACES}"; do
    if [[ -d "${WORKSPACES[$k]}" ]]; then printf "✓ %s -> %s\n" "$k" "${WORKSPACES[$k]}"
    else printf "✗ %s -> %s (missing)\n" "$k" "${WORKSPACES[$k]}"; fi
  done
'
ls -la ~/.config/wezterm/wezterm.lua   # symlink 先が dotfiles を指していること
```

## Common Mistakes

| 症状 | 原因 | 対処 |
|------|------|------|
| `wz dxp` でディレクトリ違いに飛ぶ | `WORKSPACES` のパスが古い | `workspaces.zsh` を修正 |
| ランチャーに新規項目が出ない | `launch_menu` への追加忘れ | `wezterm.lua` を更新 → 自動再読み込み |
| `dxp` コマンドが「command not found」 | 既存セッションが旧 .zshrc キャッシュ | `exec zsh` で再起動 |
| 名前変更したのに古い関数が残る | 同一セッション内の遺残 | `unfunction <oldname>` または `exec zsh` |
| `~/.wezterm.lua` を編集しても効かない | 実体は `~/.config/wezterm/wezterm.lua` | `~/dotfiles/config/wezterm/wezterm.lua` を編集 |
| `setup.sh` 実行後にバックアップが量産される | 実体ファイルが symlink になっていない | 1度だけ起きる挙動。`.bak_*` は手動削除可 |
| WezTerm が設定エラーで起動しない | `wezterm.lua` の構文ミス | ターミナルで `wezterm --config-file ~/dotfiles/config/wezterm/wezterm.lua start --always-new-process echo ok` でエラー詳細を確認 |

## Red Flags（編集中に出たら一旦止まる）

- ワークスペース追加で `workspaces.zsh` だけ / `wezterm.lua` だけ触っている → 必ずペア更新
- `~/.config/wezterm/wezterm.lua` を直接編集している → 実体ではない、symlink 先を編集する
- `setup.sh` を編集して個別ワークスペースを足そうとしている → setup.sh は symlink 配線のみ、ワークスペース定義は `workspaces.zsh`
- `wz` を alias で再定義しようとしている → 関数版（補完対応）が `workspaces.zsh` にあるので alias は使わない
