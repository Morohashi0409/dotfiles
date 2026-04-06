---
name: dify-chatbot
description: Build or edit Dify chatflow DSL for conversational bots. Use when the user asks for Dify chatbots, advanced-chat YAML/DSL, multi-turn branching, Answer node design, file-aware chatflows, or pastes an existing chatbot DSL to modify.
---

# Dify Chatbot

会話型の Dify Chatflow を新規構築するか、既存の advanced-chat DSL を安全に編集するためのスキル。

## この skill の対象

- Chatflow / `advanced-chat`
- multi-turn な会話設計
- `Answer` ノード中心の応答設計
- `Question Classifier` / `If-Else` / `Variable Aggregator` を使う会話分岐
- ファイル入力付き chatbot
- 既存 DSL の差分編集

詳細ソースは [references/source-map.md](references/source-map.md) を参照。

## 前提

- Dify docs 上では Chatflow と表現される
- exported DSL では official sample 上 `app.mode: advanced-chat`
- Chatflow は `Answer` ノードを使う
- Workflow 用の `Output` とは役割が違う

## まず確認すること

1. 何ターンの会話を想定しているか
2. 会話履歴をどう使うか
3. ファイル入力が必要か
4. 分岐は intent 判定か、単純条件か
5. 既存 DSL 編集か、新規作成か

## 新規 Chatflow を組む手順

1. 入口を決める
   - 基本は `User Input`
   - hidden field や custom field が必要なら最初に定義
2. 会話の主経路を決める
   - 単純応答: `User Input -> LLM -> Answer`
   - intent 分岐: `User Input -> Question Classifier -> 各分岐`
   - 条件分岐: `User Input -> If-Else -> 各分岐`
3. 共通後段を整理する
   - 分岐後に共通処理へ戻すなら `Variable Aggregator`
4. `Answer` を設計する
   - streaming 順を意識して変数の並びを決める
5. `features` を調整する
   - opener
   - follow-up
   - file upload
   - citation
   - moderation

## 既存 DSL を編集するルール

- `app.mode: advanced-chat` を維持する
- `workflow.conversation_variables` を安易に消さない
- `workflow.features` を落とさない
- `Answer` ノードの本文と変数順を勝手に崩さない
- `Question Classifier` / `If-Else` の branch 変更時は downstream の merge まで確認する
- 既存 node id は極力維持する

## ファイル入力パターン

### ドキュメント

`User Input(files) -> Doc Extractor -> LLM -> Answer`

### 画像

`User Input(files) -> Vision enabled LLM -> Answer`

### mixed files

`User Input(files) -> List Operator で分離 -> 各処理 -> Answer`

Workflow apps では file upload feature が非推奨寄りだが、Chatflow では file upload/citation 等の機能を素直に使える。

## 分岐パターン

### Intent routing

`User Input -> Question Classifier -> 各 intent の処理 -> Variable Aggregator -> Answer`

### 条件分岐

`User Input -> If-Else -> 各処理 -> Answer`

### マルチ Answer

途中経過を先に返したい場合は複数の `Answer` を置いてよい。

## Answer ノードの設計ルール

- `Answer` は Chatflow 専用
- 変数の並びが streaming 挙動を左右する
- 先に解決する変数を前に置く
- markdown と変数を混在できる
- text / image / file を同じ返答で流せる

## この skill を使ったときの返却物

1. 会話の主経路
2. 分岐戦略
3. 完成 DSL
4. feature 設定の要点
5. サンプル会話シナリオ
6. import 後に再確認すべき項目

## よくある誤り

- Chatflow なのに `Output` を使おうとする
- `Answer` の変数順を無視して streaming が遅くなる
- required field を hidden にしようとする
- file upload を有効化したのに `Doc Extractor` や vision LLM をつながない
- 分岐後に同じ LLM を複製し続けて複雑化する
