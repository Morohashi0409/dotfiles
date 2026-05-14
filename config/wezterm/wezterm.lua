local wezterm = require 'wezterm'
local config = wezterm.config_builder()
local act = wezterm.action

-- ■■■ 1. 見た目の設定（Cursorライク & モダンに） ■■■

-- カラーテーマ
-- Cursorのデフォルトに近い、落ち着いたダークテーマ（Tokyo Nightなど）がおすすめ
config.color_scheme = 'Tokyo Night'

-- フォント設定
-- ※ 'JetBrains Mono' は別途インストール推奨ですが、なければ自動でFallbackされます
config.font = wezterm.font_with_fallback {
  'JetBrains Mono',
  'Hack Gen',  -- 日本語フォントがあればここに指定
  'Menlo',
}
config.font_size = 14.0

-- ウィンドウの透明度（0.0〜1.0）
-- 少し透かすと「イキってる」感が出てカッコいい上に、裏の資料が見えて便利
config.window_background_opacity = 0.85
config.macos_window_background_blur = 10

-- タイトルバーを消す（Cursorのターミナルのようにスッキリさせる）
config.window_decorations = "RESIZE"

-- タブバーのデザイン
config.use_fancy_tab_bar = false -- シンプルなタブバーにする
config.tab_bar_at_bottom = true  -- タブを下に配置（好みで false にして上でもOK）
config.hide_tab_bar_if_only_one_tab = false -- タブが1つでも表示する

-- ■■■ 2. Claude Code / AI開発向け設定 ■■■

-- スクロールバック行数
-- Claude Codeの長い差分表示やログが消えないように多めに確保
config.scrollback_lines = 10000

-- ■■■ 3. プロジェクトランチャー（Cmd+Shift+L で表示） ■■■
-- ワークスペースを追加する場合は下の launch_menu に項目を増やすだけでOK。
-- zsh 側の WORKSPACES (~/dotfiles/zsh/workspaces.zsh) と揃えておくと CLI / GUI が一致します。

local HOME = os.getenv('HOME')
local SHELL = os.getenv('SHELL') or '/bin/zsh'

config.launch_menu = {
  {
    label = 'dxp',
    args = { SHELL, '-l' },
    cwd = '/Users/resily0808/dxp/dxp-2/dxp',
  },
  {
    label = 'wellcom',
    args = { SHELL, '-l' },
    cwd = HOME .. '/WrllCom_front2025/WellCom_front',
  },
  {
    label = 'dotfiles',
    args = { SHELL, '-l' },
    cwd = HOME .. '/dotfiles',
  },
}

-- ■■■ 4. キーバインド（Mac / Cursorユーザーが迷わないように） ■■■

-- MacのOptionキーをMetaキーとして扱う（Option+矢印で単語移動などができるように）
config.send_composed_key_when_left_alt_is_pressed = false
config.send_composed_key_when_right_alt_is_pressed = false

config.keys = {
  -- 【コピー & ペースト】（Cmd+C / Cmd+V）
  { key = 'c', mods = 'SUPER', action = act.CopyTo 'Clipboard' },
  { key = 'v', mods = 'SUPER', action = act.PasteFrom 'Clipboard' },

  -- 【ペイン操作】（画面分割）
  -- CursorやVS Codeのterminalに近い感覚で
  { key = 'd', mods = 'SUPER', action = act.SplitHorizontal { domain = 'CurrentPaneDomain' } }, -- 左右分割
  { key = 'D', mods = 'SUPER', action = act.SplitVertical { domain = 'CurrentPaneDomain' } },   -- 上下分割
  { key = 'w', mods = 'SUPER', action = act.CloseCurrentPane { confirm = false } },             -- ペインを閉じる

  -- 【ペイン移動】（Cmd + 矢印）
  { key = 'LeftArrow',  mods = 'SUPER', action = act.ActivatePaneDirection 'Left' },
  { key = 'RightArrow', mods = 'SUPER', action = act.ActivatePaneDirection 'Right' },
  { key = 'UpArrow',    mods = 'SUPER', action = act.ActivatePaneDirection 'Up' },
  { key = 'DownArrow',  mods = 'SUPER', action = act.ActivatePaneDirection 'Down' },

  -- 【フォントサイズ変更】（Cmd + +/-）
  { key = '+', mods = 'SUPER', action = act.IncreaseFontSize },
  { key = '-', mods = 'SUPER', action = act.DecreaseFontSize },
  { key = '0', mods = 'SUPER', action = act.ResetFontSize },

  -- 【コマンドパレット】（Cmd + Shift + P）
  -- WezTermの機能を検索して実行できる（VS Codeと同じキー）
  { key = 'p', mods = 'SUPER|SHIFT', action = act.ActivateCommandPalette },

  -- 【検索モード】（Cmd + F）
  { key = 'f', mods = 'SUPER', action = act.Search 'CurrentSelectionOrEmptyString' },

  -- 【プロジェクトランチャー】（Cmd + Shift + L）
  -- launch_menu に登録したワークスペースを fuzzy 検索 → 選択でそのディレクトリに新規タブ
  {
    key = 'l',
    mods = 'SUPER|SHIFT',
    action = act.ShowLauncherArgs { flags = 'FUZZY|LAUNCH_MENU_ITEMS' },
  },
}

-- ■■■ 5. その他 ■■■

-- 日本語入力（IME）のチラつき防止など
config.use_ime = true

return config
