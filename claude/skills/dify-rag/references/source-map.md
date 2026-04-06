# Source Map

この skill は以下を基準に組んでいる。

## Primary

- Dify Knowledge Retrieval docs
  - `result` が retrieval 出力
  - metadata filtering
  - Top K / Score Threshold / rerank
  - LLM の Context へ接続するのが基本
- Dify LLM docs
  - Prompt / Context / multimodal の基本
- Dify Template / Code / Variable Aggregator docs
  - 整形、JSON 変換、分岐マージの基本構成

## Secondary

- note: Contextual Retrieval を Dify に落とし込む
  - chunk に文脈を補う ingest 前処理として整理
  - Code + Iteration + LLM の構成が中心
- note: HyDE の理論から Dify 実装・検証
  - `質問 -> 仮説回答 -> 検索 -> 最終回答` の構成
- note: GraphRAG を Dify に落とし込む
  - Dify 単体ではまず entity / relation 抽出ワークフローとして扱う
  - `LLM -> Code(JSON parse) -> Template` の流れ

## Derived Rules

- HyDE は query-side 改善
- Contextual Retrieval は ingest-side 改善
- GraphRAG は Dify 単体で完結する native graph retrieval ではなく、まず抽出系パイプラインとして設計する
- 既存 DSL 編集では retrieval node と downstream context wiring を必ずセットで確認する
