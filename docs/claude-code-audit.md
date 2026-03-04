# Claude Code 構築状況 監査レポート

**作成日:** 2026-03-03
**最終更新:** 2026-03-04
**対象:** `~/dotfiles/claude/` および `~/.claude/`

---

## 総合評価

基本構成（hooks, settings.json, CLAUDE.md, setup.sh）は機能している。
2026-03-04 の修正により、skills と commands の分離、frontmatter の統一、setup.sh の skills 対応が完了した。

---

## 修正済み問題一覧

### 1. skills と commands の混在・重複 → 解決済み

**修正内容:**
- `fixing-accessibility`, `frontend-design`, `12-principles-of-animation` の3つを
  `commands/*.md` から `skills/{name}/SKILL.md` に移動
- skills = 自動トリガー、commands = `/xxx` で明示呼び出し、という配置ルールを確立
- 各 SKILL.md に `user-invocable: true` を追加し、スラッシュコマンドでも呼べるようにした

---

### 2. skills/ が dotfiles で管理されていない → 解決済み

**修正内容:**
- `~/dotfiles/claude/skills/` に3つのスキルを配置:
  - `skills/12-principles-of-animation/SKILL.md`
  - `skills/fixing-accessibility/SKILL.md`
  - `skills/frontend-design/SKILL.md`
- `setup.sh` に skills ディレクトリ単位のリンク処理を追加
- `baseline-ui`, `find-skills` は外部インストール（`~/.agents/skills/`）のため dotfiles 管理外のまま

---

### 3. frontmatter のないコマンドが3つ存在 → 解決済み

**修正内容:**
- `commit.md`, `doc.md`, `review.md` に YAML frontmatter（description, depends-on）を追加

---

### 4. depends-on の宣言が不完全 → 解決済み

**修正内容:**
- `handover.md`, `create-command.md`, `pre-review.md`, `github-issue-organize.md` に
  `depends-on: [CLAUDE.md]` を追加
- `commit.md`, `doc.md`, `review.md` は frontmatter 追加時に同時対応

| ファイル | depends-on | 状態 |
|---------|-----------|------|
| continue.md | `CLAUDE.md` | 済（元から） |
| doc-check.md | `CLAUDE.md` | 済（元から） |
| commit.md | `CLAUDE.md` | 済（今回追加） |
| doc.md | `CLAUDE.md` | 済（今回追加） |
| review.md | `CLAUDE.md` | 済（今回追加） |
| handover.md | `CLAUDE.md` | 済（今回追加） |
| create-command.md | `CLAUDE.md` | 済（今回追加） |
| pre-review.md | `CLAUDE.md` | 済（今回追加） |
| github-issue-organize.md | `CLAUDE.md` | 済（今回追加） |

---

### 5. doc.md と review.md の内容が簡素すぎる → 解決済み

**修正内容:**
- `doc.md`: 4行 → 実施手順・構成テンプレート・執筆ルール・品質チェックを追加
- `review.md`: 4行 → レビュー手順・チェック項目（正確性/セキュリティ/パフォーマンス/可読性/規約）・出力フォーマットを追加

---

### 6. setup.sh の不完全性 → 解決済み（skills 部分）

**修正内容:**
- `setup.sh` に skills/ ディレクトリ単位のシンボリックリンク処理を追加

---

## 残存する課題

### 7. globs フィールドの不統一（低）

**現状:** 一部コマンドは `globs: ["**/*"]`、一部は限定パターン、一部は globs なし。
**影響:** 低。実運用上の問題は軽微。

---

### 8. ~/.agents/skills/ が dotfiles 管理外（低）

**現状:** `baseline-ui`, `find-skills` は `~/.agents/skills/` に独立して存在。
**影響:** 新環境での再現には手動インストールが必要。
**方針:** 外部ツールのため dotfiles 管理外として許容。必要に応じてインストール手順をドキュメント化する。

---

## 修正優先度マトリクス（更新後）

| 優先度 | 問題 | 状態 |
|-------|------|------|
| ~~**高**~~ | ~~1. skills/commands の重複解消~~ | 解決済み |
| ~~**高**~~ | ~~2. skills/ を dotfiles で管理~~ | 解決済み |
| ~~**高**~~ | ~~3. frontmatter 追加~~ | 解決済み |
| ~~**中**~~ | ~~4. depends-on 追加~~ | 解決済み |
| ~~**中**~~ | ~~5. doc.md, review.md 充実~~ | 解決済み |
| ~~**中**~~ | ~~6. setup.sh skills 対応~~ | 解決済み |
| **低** | 7. globs の方針統一 | 未対応 |
| **低** | 8. ~/.agents/skills/ の管理 | 管理外として許容 |
