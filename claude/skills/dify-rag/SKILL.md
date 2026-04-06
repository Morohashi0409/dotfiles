---
name: dify-rag
description: Build or edit Dify RAG workflows and DSL. Use when the user asks for knowledge retrieval pipelines, HyDE, contextual retrieval, GraphRAG-inspired flows, retrieval tuning, or pastes existing Dify YAML/DSL to modify a RAG app.
---

# Dify Rag

Dify 上で RAG を構築・改善・DSL 編集するためのスキル。

## この skill の対象

- 通常の RAG
- `Knowledge Retrieval` ノードの調整
- HyDE
- Contextual Retrieval
- GraphRAG 風の抽出・関係整理パイプライン
- 既存 DSL の retrieval 部分だけの安全な差分編集

詳細ソースは [references/source-map.md](references/source-map.md) を参照。

## まず決めること

1. 単発問い合わせか、会話型 QA か
2. 既にナレッジベースがあるか
3. 課題は「検索前処理」か「検索時クエリ」か「回答生成」か
4. 既存 DSL を編集するのか、新規構築するのか
5. 真の GraphRAG が必要か、GraphRAG 風の関係抽出で十分か

## 推奨判断

### 通常 RAG

向いている場合:

- チャンク品質が既に高い
- 質問文と本文の文体ギャップが小さい
- まずはシンプルに組みたい

基本構成:

`User Input -> Knowledge Retrieval -> LLM -> Answer/Output`

### HyDE

向いている場合:

- 質問文が短く曖昧
- 回答文の語彙と原文書の語彙が近い
- クエリ側を改善したい

基本構成:

`User Input -> LLM(仮説回答) -> Knowledge Retrieval -> LLM(最終回答) -> Answer/Output`

### Contextual Retrieval

向いている場合:

- 文書登録時にチャンク化で文脈が落ちている
- 検索前に document 側を強くしたい
- 前処理コストを許容できる

注意:

- これは主に ingest 側の改善であり、単純な runtime 分岐だけでは完結しない
- Dify だけで閉じない場合は、前処理 workflow と knowledge 登録運用を分けて説明する

### GraphRAG 風フロー

向いている場合:

- 人物・組織・概念・関係の連鎖が重要
- 文章の近さより関係性の復元が重要

注意:

- Dify の標準ノードだけでは「完全な graph retrieval 基盤」にはならない
- まずは `LLM -> Code(JSON parse) -> Template` で entity / relation 抽出を組み、外部グラフ基盤が必要なら別途明示する

## 既存 DSL を編集するルール

- 既存の `app.mode` は維持する
- `Knowledge Retrieval` ノードの knowledge base バインドや metadata filter を勝手に消さない
- `dependencies` の provider / plugin は維持する
- 既存 node id は極力維持する
- `Output` と `Answer` の使い分けは mode に従う
- retrieval 結果の変数受け渡しを変える場合、後続 LLM / Template / Answer まで連鎖確認する

## 実装パターン

### 通常 RAG

1. `User Input`
2. `Knowledge Retrieval`
3. `LLM`
   - Context に retrieval の `result` を接続
4. `Answer` または `Output`

### HyDE

1. `User Input`
2. `LLM`
   - 質問から仮説回答を生成
3. `Knowledge Retrieval`
   - 仮説回答ベースで検索
4. `LLM`
   - 検索結果と元質問から最終回答
5. `Answer` または `Output`

### Contextual Retrieval 前処理

1. 文書入力
2. `Code` で chunk 化
3. `Iteration`
4. `LLM` で各 chunk に文脈付与
5. `Template` または `Code` で整形
6. knowledge 登録フローへ受け渡し

### GraphRAG 風抽出

1. 文書入力
2. `LLM` で entity / relation を JSON 生成
3. `Code` で JSON parse と欠損補完
4. `Template` で可読化
5. `Output`

Code node では、エラー時も宣言した全 output を返す。

## Retrieval tuning checklist

- `Top K`
- `Score Threshold`
- rerank model の有無
- weighted score の重み
- metadata filtering の条件
- LLM context に `result` を正しく渡しているか
- citations を見せたいなら Chatflow + Answer の構成が適切か

## この skill で返すべきもの

1. 採用パターンの理由
2. ノード構成図
3. 完成 DSL
4. knowledge 側で必要な準備
   - chunking 方針
   - metadata
   - provider / rerank model
5. 検証用クエリ
6. 失敗しやすいケース

## よくある誤り

- `Knowledge Retrieval` の `result` を Context に渡していない
- HyDE なのに検索クエリを元質問のままにしている
- Contextual Retrieval を runtime だけで済ませようとする
- GraphRAG と単なる entity extraction を混同する
- Code node の parse 失敗時に output 欠落で downstream が壊れる
- score threshold を上げ過ぎて retrieval が空になる
