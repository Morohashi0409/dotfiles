# Source Map

この skill は以下を基準に組んでいる。

## Primary

- Dify Key Concepts
  - Workflow と Chatflow は主要アプリ型
  - `User Input` と `Trigger` は排他的
  - Workflow は単発処理向け
- Dify Output node docs
  - Output は旧 End
  - Workflow 専用
  - output variable がないと返り値が返らない
- Dify Code node docs
  - declared output に対応する dict を返す必要がある
- Dify official exported DSL sample
  - `app / dependencies / kind / version / workflow / graph.nodes / graph.edges` の基本形
- langgenius/dify issue examples
  - `app.mode: workflow` の exported DSL 実例
  - import 周りは version 差異で不具合が起こりうる

## Secondary

- MYUUU: Dify の DSL（YAML）とは？
  - GUI と YAML のハイブリッド運用
  - import 後に tool / model / secret を点検する実務観点

## Derived Rules

- 既存 DSL 編集では unknown field を削らない
- node id を維持し、edge だけ壊さない
- import/export をまたぐ変更では plugin・provider・secret を別枠で確認する
