---
name: requirement-brief-md
description: Creates markdown requirement briefs that bundle file paths, Cursor/Claude skills, MCP tools, and verification steps so Claude Code or other agents can execute work from a single attached MD. Use when the user asks to document specs for handoff, to "要件をmdにまとめる", or to prepare instructions with explicit paths and tooling.
---

# 要件ブリーフ MD の作成

**格納:** `~/dotfiles/claude/skills/requirement-brief-md/`（プロジェクトの `.cursor/skills` ではなく dotfiles 側を正とする。Cursor で使う場合は symlink かエージェントが dotfiles のスキルを読む設定にする。）

## いつ使うか

- 機能・不具合・データパイプラインなどを **別セッション／Claude Code にそのまま渡して実装させたい**
- 依頼文に **ファイルパス・スキル・MCP・検証手順** を埋め込んだ **1 本の MD** が欲しい

## 出力の置き場（対象リポジトリ内）

| 種別 | パス例 |
|------|--------|
| 分析レポート系 | `docs/analysis-report/requirements/<topic>.md` |
| バックエンド単体 | `backend/docs/requirements/<topic>.md` |
| フロント単体 | `docs/frontend/requirements/<topic>.md` |

既存の並びに合わせる（例: `q12_job_chart_issues.md` のような命名）。

## MD に必ず含めるブロック

1. **目的** — 1～3 行
2. **参照ファイル（リポジトリ相対パス）** — 実装・調査の起点。`backend/src/...` のように **コピー可能なパス** で列挙
3. **使用するスキル** — pptx / xlsx 等、作業種別に応じて明示（プロジェクトの `CLAUDE.md` で言及されるスキルも）
4. **MCP** — 使う場合のみ（サーバー名・用途。不要なら「なし」）
5. **仕様・制約** — 数値ハードコード禁止など **対象リポの `CLAUDE.md` / `AGENTS.md`** と矛盾しないこと
6. **実装チェックリスト** — 箇条書き
7. **検証** — コマンド・SQL・生成物の確認手順

## スキル / MCP の書き方

- **スキル**: 名前と「何のためか」1 行（例: `pptx` — グラフ・凡例の OOXML 調整）
- **MCP**: `user-excel` / `user-powerpoint-mcp` 等、**そのワークスペースで有効な識別子**で記載。スキーマ確認が必要なら「呼び出し前に descriptor を読む」と書く

## テンプレート（コピー用）

```markdown
# <タイトル>

## 目的
（何を達成するか）

## 参照ファイル
| 役割 | パス |
|------|------|
| 実装主 | `backend/...` |
| 設定/データ | `backend/FY25/...` |

## 使用スキル
- （例）pptx — スライド上のチャート修正
- （例）xlsx — ベンチマーク Excel の列確認

## MCP
- なし / （あればサーバー名と用途）

## 仕様・制約
- CLAUDE.md のルール（ハードコーディング禁止等）に従う

## 実装チェックリスト
- [ ] …
- [ ] …

## 検証
\`\`\`bash
# 例
cd backend/FY25/survey_report && python3 ...
\`\`\`
```

## エージェント向けメモ

- パスは **ワークスペースルートからの相対** がそのまま CLI に使える形がよい
- 既存要件 MD と **重複する課題** があればリンクで参照し、新 MD では差分だけ書く
- 長い背景は **別 MD に分け**、本ブリーフは実行可能な範囲に絞る（500 行未満目安）
