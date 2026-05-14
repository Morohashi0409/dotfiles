# メモリ運用の現状整理

## 目的
- 同じ指摘の再発を防ぐ。
- セッションの学びを次回作業に引き継ぐ。
- Claude 側と Codex 側で同じルールを使う。

## 現在の利用の流れ
1. 作業開始前に過去メモリを読む。
2. 実装や調査を進める。
3. 作業中に否定や訂正が出たら即時で記録する。
4. セッション終了時に内容をまとめて永続メモリへ追記する。

## 構成
- 実体は Claude 側の skill に置く。
- Codex 側はシンボリックリンクで Claude 側を参照する。
- 主要 skill は次の 3 つ。
  - read-project-memory: 作業前の読み込み
  - log-feedback: 作業中の即時記録
  - thread-memory: セッション終端の集約記録

## Obsidian 構成
- 保管先ルート
  - `/Users/resily0808/Documents/Obsidian Vault/00_AI-OS`
- 主要エリア
  - `Global.md`
  - `Projects/<プロジェクト名>/Rules.md`
  - `Projects/<プロジェクト名>/Feedback.md`
  - `Projects/_Template/`
- グローバル側の主なファイル
  - `Global.md`: 全プロジェクト共通の期待品質・禁止事項・確定ルール・ユーザー特性
- プロジェクト側の主なファイル
  - `Rules.md`: プロジェクト固有ルール
  - `Feedback.md`: newest-on-top の指摘記録（5タグ）

## 使い分け
- read-project-memory
  - 実装、修正、調査、デバッグ、起票の前に使う。
  - `Global.md` + `Rules.md` + `Feedback.md(直近5件)` を読み、遵守3点/禁止3点を提示する。
- log-feedback
  - 「違う」「そうじゃない」「しないで」などの訂正が出た瞬間に使う。
  - 指摘の原文を `Feedback.md` 最上部へ1件追記する（同日同文は重複skip）。
- thread-memory
  - セッション末尾トリガー時に使う（`/handover` など）。
  - フィードバックの重複を避けつつ、必要分を `Feedback.md` に追記する。

## Codex Hooks 反映（2026-05-12）
- `SessionStart` -> `session_start_read_project_memory.py`
- `UserPromptSubmit` -> `user_prompt_log_feedback.py`
- `Stop` -> `stop_thread_memory.py`
- 実装場所: `~/dotfiles/codex/hooks/`
- 設定場所: `~/.codex/config.toml`

## 良い点
- 作業前、作業中、作業後で責務が分かれている。
- 指摘の取りこぼしを減らせる。
- Codex 側の更新漏れを構造で防げる。

## 課題
- 発火の境界が人の判断に依存しやすい。
- 軽い依頼で読み込みを省略すると、過去ルールを見落としやすい。
- プロジェクト特定が曖昧な時に記録先がぶれる可能性がある。
- 類似指摘の統合は手作業寄りで、昇格判断が遅れることがある。

## 改善の方向
1. 発火条件を短いチェックリストで固定する。
2. 記録後の出力形式を統一して見落としを減らす。
3. プロジェクト不明時の扱いを固定文で運用する。
4. 月次で重複指摘を確認して昇格候補を整理する。

## 運用の要点
- 原文保持を最優先にする。
- 既存履歴は書き換えず追記する。
- 1つの指摘は 1エントリで残す。
- 迷ったらまず global に寄せ、次回で project 側へ昇格する。
