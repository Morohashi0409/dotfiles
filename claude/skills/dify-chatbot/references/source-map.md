# Source Map

この skill は以下を基準に組んでいる。

## Primary

- Dify Key Concepts
  - Chatflow / Workflow が主要アプリ型
- Dify Answer docs
  - Answer は Chatflow 専用
  - variable order が streaming に影響
  - text / image / file の混在が可能
- Dify User Input docs
  - custom input / hidden field / file input
  - `userinput.query` は chatflow 用
- Dify Additional Features docs
  - Chatflow は opener / follow-up / TTS / file upload / citation / moderation などを持つ
- Dify Variable Aggregator docs
  - 分岐後の共通 downstream を簡素化できる

## Secondary

- official exported DSL sample
  - Chatflow export では `app.mode: advanced-chat`
- langgenius/dify issue samples
  - advanced-chat DSL の exported 例
  - Variable Aggregator / multi-branch は version 依存の確認が必要

## Derived Rules

- 新規会話型は basic Chatbot より Chatflow/advanced-chat を優先
- file-aware chat は User Input + extractor/vision まで一体で設計する
- 分岐後の重複 downstream は Variable Aggregator で減らす
