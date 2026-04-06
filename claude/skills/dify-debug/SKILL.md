---
name: dify-debug
description: Debug and verify Dify workflow or chatflow DSL. Use when the user reports import errors, missing outputs, broken variables, node failures, version-specific behavior, or wants a pasted Dify YAML/DSL audited and minimally fixed.
---

# Dify Debug

Dify の Workflow / Chatflow / DSL import を診断し、最小差分で修正するためのスキル。

## この skill の対象

- import 後に動かない DSL
- 実行時エラー
- node output 欠落
- variable が想定通り流れない
- version 差分での挙動変化
- pasted DSL の構造監査

詳細ソースは [references/source-map.md](references/source-map.md) を参照。

## デバッグの基本姿勢

- いきなり全面書き換えしない
- まず構造不整合か runtime 不整合かを切り分ける
- 最小の再現条件を作る
- 修正は 1 箇所ずつ
- 直った根拠を run history / variable inspector / logs で確認する

## 標準フロー

1. 症状を明文化する
   - import 失敗
   - 実行はされるが返答が空
   - 特定ノードだけ失敗
   - 分岐後の値が混線
2. DSL 監査
   - top-level
   - node / edge 整合
   - mode と Answer / Output の整合
   - dependencies / env vars / conversation vars
3. 実行デバッグ
   - Variable Inspector
   - Last run
   - Run History
   - Logs / Logs API
4. 最小修正
5. 再実行
6. version / environment 依存リスクを明示

## DSL 構造監査チェックリスト

- `app`
- `kind`
- `version`
- `dependencies`
- `workflow.environment_variables`
- `workflow.conversation_variables`
- `workflow.features`
- `workflow.graph.nodes`
- `workflow.graph.edges`
- 全 edge の `source` / `target` が実在するか
- branch handle が実在するか
- `workflow` なのに `Answer` になっていないか
- `advanced-chat` なのに `Output` 前提になっていないか
- `Code` が declared output を返しているか

## 実行デバッグで使う観点

### Variable Inspector

- 各 node の入出力を確認する
- downstream だけ再実行したいときは値を書き換えて試す
- `Last run` の記録は変わらない点に注意する

### Run History

- Result
- Detail
- Tracing

失敗箇所が「どこで止まったか」を tracing で切る。

### Logs

- 公開後の live traffic の問題を追う
- debug session ではなく実利用ログを見る
- API 連携時は workflow logs / run details API で status, error, total_steps を拾う

## よくある原因

### 構造系

- `Output` に出力変数がない
- edge が古い node id を指している
- `dependencies` を消して plugin が解決できない
- `conversation_variables` や feature 設定が import 後に欠けている

### 実行系

- `Code` node の戻り値不足
- `Knowledge Retrieval` の結果が空
- branch のどこかで null / empty を返している
- model provider / secret / tool が環境差で解決できない

### version 依存

- import 後の表示不良や no response
- version incompatible な DSL import
- Variable Aggregator 周りの version-specific bug
- chatflow の conversation variable import 不備報告

## エラー処理を見るとき

- LLM / HTTP / Code / Tool は predefined error handling を持つ
- `None`
- `Default Value`
- `Fail Branch`

Loop / Iteration では error mode の差も確認する。

## pasted DSL を直すときのルール

- まず壊れている最小箇所を説明する
- 全面生成し直すのは最後
- 既存 id と変数名を極力維持
- 修正 diff を箇条書きで示す
- 「構造修正」と「環境依存の未解決」を分けて返す

## この skill で返すもの

1. 原因候補の優先順位
2. 監査結果
3. 最小修正 DSL
4. 再テスト手順
5. 依然として残る version / environment リスク
