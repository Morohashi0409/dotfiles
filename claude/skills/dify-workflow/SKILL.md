---
name: dify-workflow
description: Build or edit Dify Workflow DSL for single-turn apps. Use when the user asks for Dify workflow YAML/DSL creation, import/export-safe edits, Start/LLM/Code/Template/Output design, or pastes an existing workflow DSL to modify.
---

# Dify Workflow

基本の Dify Workflow を新規構築するか、既存の DSL を壊さず編集するためのスキル。

## この skill の対象

- `app.mode: workflow` の単発実行アプリ
- Start から Output までの基本ノード設計
- `User Input` と `Trigger` のどちらで始めるべきかの判断
- 既存 DSL の最小差分編集
- import/export を前提にした移植しやすい YAML 整備

詳細ソースは [references/source-map.md](references/source-map.md) を参照。

## 最初に確認すること

1. これは単発タスクか、会話を継続するチャットか
2. 実行起点は `User Input` か `Trigger` か
3. 最終的に返したい出力は何か
4. 既存 DSL の編集か、新規作成か
5. 外部ツール・HTTP・Knowledge・secret 環境変数が必要か

会話型なら `dify-chatbot` を優先する。

## 2つの作業モード

### 1. 新規 DSL を作る

以下の順で組み立てる。

1. 入力
   - 単純なテキストなら `User Input`
   - 定期実行やイベント起動なら `Trigger`
2. 主処理
   - 生成なら `LLM`
   - 条件分岐なら `If-Else`
   - 計算・JSON 変換・整形なら `Code` / `Template`
3. 出力
   - Workflow では `Output` を使う
   - API 返却が必要なら `Output` の出力変数を必ず定義する

### 2. 貼られた DSL を編集する

必ず以下の順で扱う。

1. まず YAML をそのまま読み、既存の `app / dependencies / workflow` の形を把握する
2. 変更対象のノードだけを特定する
3. 既存の node id をできる限り維持する
4. node id を変えた場合は `graph.edges[*].source / target / sourceHandle / targetHandle` を必ず追従させる
5. 触っていない unknown field は削除しない
6. 変更後は「壊していない部分」と「意図的に変えた部分」を分けて説明する

## DSL 編集の不変条件

- `kind: app` は維持する
- `app.mode` は Workflow なら `workflow` を維持する
- `version` は既存値を基本維持する
- `dependencies` は勝手に削除しない
- `workflow.environment_variables` と `workflow.conversation_variables` は名前・id・selector を安易に変えない
- `workflow.features` は import 後の UI 挙動に効くので丸ごと落とさない
- `graph.nodes` と `graph.edges` は整合している必要がある
- `Output` を使うなら output variable を最低 1 つ返す
- `Answer` は Chatflow 用なので Workflow では使わない

## 設計パターン

### 最小構成

`User Input -> LLM -> Output`

単純な要約、整形、分類、変換に向く。

### 条件分岐

`User Input -> If-Else -> 各処理 -> Output`

分岐後の後段が共通なら、変数名を揃えるか `Variable Aggregator` を検討する。

### 計算・整形入り

`User Input -> Code -> Template -> Output`

Code node は declared output と一致する dict を返す前提で書く。

### 定期実行

`Trigger -> 各処理 -> Output`

`User Input` と `Trigger` は同じ canvas で併用しない。

## 出力時のフォーマット

この skill を使ったら、原則として以下を返す。

1. ノード構成の要約
2. 変更方針
3. 完成 DSL
4. import 後に再設定が必要なもの
   - モデルプロバイダ
   - plugin / tool
   - secret 環境変数
5. テスト観点

## 典型的な落とし穴

- `Output` に返却変数がなく、API から何も返らない
- `Code` の戻り値キーが output variable 名と一致していない
- node id を変えたのに edge を更新していない
- `User Input` と `Trigger` を混在させようとする
- import 先に plugin / provider が存在せず壊れる
- Dify のバージョン差で import 後に挙動が変わる

## 実務ルール

- フルリライトより最小差分を優先
- 既存 DSL がある場合、まず patch 方針を示してから反映
- 仕様が曖昧でも、既存ノード命名・変数命名・構造は極力継承
- 環境依存の tool や model は「推定」ではなく「要再設定」と明示
