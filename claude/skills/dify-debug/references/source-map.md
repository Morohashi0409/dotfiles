# Source Map

この skill は以下を基準に組んでいる。

## Primary

- Dify Variable Inspector docs
  - node ごとの入出力確認
  - 値を編集して downstream だけ再実行できる
- Dify Run History docs
  - Result / Detail / Tracing で切り分ける
- Dify Logs docs / Workflow Logs API
  - live traffic の status, error, total_steps を追える
- Dify Handling Errors docs
  - LLM / HTTP / Code / Tool の predefined error handling

## Official issue signals

- import DSL まわりの no response / UI error / version incompatibility 報告
- chatflow import で conversation variables 欠落の報告
- Variable Aggregator の multi-branch 挙動の version-specific 報告

## Derived Rules

- import 不具合は「DSL が壊れている」のか「対象 Dify version 依存」なのかを分けて考える
- pasted DSL 修正では全面書き換えより最小差分修正を優先
- provider / plugin / secret の未解決は構造修正と分けて報告する
