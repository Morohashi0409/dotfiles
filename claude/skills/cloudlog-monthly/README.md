# CloudLog Monthly

月次の CloudLog 入力を end-to-end で進めるための skill です。
この skill は「月次 JSON を作るだけ」ではなく、「CloudLog にその月を登録して、保存結果まで確認する」前提で使います。

## 重要な前提

この skill は意図的に `skill` ディレクトリ単体では完結しません。

ただし、`/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/` 配下の資料は、
部内全員が読める共有ドキュメントではなく、現時点ではこのローカル環境で保持している運用資料です。
そのため、部内共有向け README としては「そのパスを読めばよい」とは扱わず、
skill 内の `README.md` / `SKILL.md` / `docs/` を共有向けの説明面にします。

- skill 内に置くもの
  - 実行フロー
  - 停止条件
  - 補助スクリプト
  - 読み込むべき資料の順序
- 外部の CloudLog 運用資料に置くもの
  - 案件別カテゴリ一覧
  - 自動入力の厳密な JSON 契約
  - 別スレッドへ渡す実行テンプレート
  - 実運用上の分類基準

この分離を曖昧にしないために、README は人間向けの全体像、`SKILL.md` はエージェント向けの入口、`docs/` は skill の詳細資料として使います。

## 誰が何を読むか

- 月次入力を依頼する人
  - この README
  - `docs/user-preparation.md`
  - `docs/conversation-guide.md`
- skill を実行するエージェント
  - `SKILL.md`
  - `docs/source-of-truth.md`
  - `docs/category-management.md`
  - `references/`
- skill を保守する人
  - `docs/document-map.md`
  - `docs/source-of-truth.md`
  - この環境で参照できる場合のみ、外部の CloudLog 運用資料

## ドキュメント構成

- `README.md`
  - 人間向けの概要、準備物、責務の切り分け
- `SKILL.md`
  - エージェント向けの実行入口
  - 最初に読む資料と作業順
- `docs/document-map.md`
  - README、SKILL、docs、references、外部資料の役割分担
- `docs/source-of-truth.md`
  - 何を skill 内で持ち、何を外部正本に置くか
- `docs/user-preparation.md`
  - 実行依頼者、環境保持者、運用保守者ごとの準備事項
- `docs/conversation-guide.md`
  - 資料添付ベースでの会話例
  - Chrome 起動や自動入力をチャットで依頼する例
- `docs/category-management.md`
  - `WellCom`、`one-platform`、`アドモニ` など案件別カテゴリの管理方針
- `references/`
  - パス規約、月次実行フロー、自動入力契約の要約

## ローカル運用者向け外部正本

この skill が参照する主な外部正本は次です。
ただし、以下はこのローカル環境の運用資料であり、部内メンバーがそのまま参照できる前提ではありません。
共有向けの説明は skill 内 docs に残し、実行時の厳密な正本としてのみ使います。

- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/INDEX.md`
  - CloudLog 側ドキュメントの索引
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/クラウドログ分類と運用ガイド.md`
  - 案件別カテゴリと分類基準の正本
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md`
  - JSON 契約と automator の UI 契約の正本
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/README_cloudlog_automator.md`
  - automator 単体の詳細 README
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/QUICKSTART.md`
  - 環境立ち上げの quickstart
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/別スレッド用_月次入力テンプレート.md`
  - 別スレッドへそのまま渡す実行テンプレートの正本
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-sources/`
  - 月次入力に使う canonical PDF
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/`
  - 月次 JSON の出力先

## 部内共有向けに見る資料

部内メンバーに共有する前提で見るべき資料は次です。

- `README.md`
- `docs/document-map.md`
- `docs/source-of-truth.md`
- `docs/user-preparation.md`
- `docs/conversation-guide.md`
- `docs/category-management.md`
- `references/path-conventions.md`
- `references/monthly-workflow.md`
- `references/automatic-entry-contract.md`

## この skill がやること

この skill は、対象月の CloudLog 登録を次の順で進めます。

1. 対象月 `YYYY-MM` を確定する
2. 添付ファイルを最優先に、なければ `~/Downloads` から勤怠 PDF と予定 PDF を探す
3. それらを `monthly-sources/YYYY-MM/` に canonical 名で配置する
4. Daily ノート、勤怠 PDF、予定 PDF、GitHub や repo の履歴を使って `monthly-json/YYYY-MM_cloudlog.json` を作る
5. CloudLog の制約に合わせて、勤怠時刻と `time_blocks` を 5 分刻みに正規化する
6. `validate_json.py` で保存可能な形か検証する
7. 自動入力が必要なら `check_cloudlog_automator_ready.py` で事前確認する
8. `cloudlog_automator.py` を実行して、保存できた日と失敗した日を確認する
9. 一部の日だけ失敗した場合は、直せる範囲は修正して再実行する

## 依頼者の準備物

最低限、次を把握して依頼できる状態が必要です。

- 対象月
  - 例: `2026-03`
- Daily ノート
  - 各営業日について、何をやったかが最低限わかる状態
- その月の勤怠 PDF 1 つ
  - 添付するか `~/Downloads` に置く
- その月の Outlook / Teams 予定 PDF 1 つ
  - 添付するか `~/Downloads` に置く
- カテゴリやマイパターンの変更情報
  - 先月と CloudLog のカテゴリ構成が変わっていれば伝える
- 自動入力までやる場合は、CloudLog にログイン済みの Chrome debug セッション
  - CloudLog の勤務表ページを開いた状態まで含む

詳細は `docs/user-preparation.md` を参照してください。

## この skill が前提にしないこと

依頼者は次をやる必要はありません。

- PDF のリネーム
- `monthly-sources` への移動
- JSON の 5 分刻み調整
- JSON の整合性チェック
- 自動入力前の細かい前処理
- 案件カテゴリ文字列の skill 内同期

## 更新先のルール

何を変えたいかによって更新先を分けます。

- 実行手順や停止条件を変える
  - `SKILL.md` または `references/`
- ユーザー向けの説明を変える
  - `README.md`
- skill と外部正本の責務分担を変える
  - `docs/source-of-truth.md`
- `WellCom`、`one-platform`、`アドモニ` などの案件分類を変える
  - 外部の `クラウドログ分類と運用ガイド.md`
- 別スレッドに渡す依頼テンプレートを変える
  - 外部の `別スレッド用_月次入力テンプレート.md`

ローカル専用資料へのリンクを README に足す場合は、
「部内全員が読める補足資料」と誤解されないよう、必ずローカル運用者向けであることを明記します。

## 関連資料

- `docs/document-map.md`
- `docs/source-of-truth.md`
- `docs/user-preparation.md`
- `docs/category-management.md`
- `references/path-conventions.md`
- `references/monthly-workflow.md`
- `references/automatic-entry-contract.md`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/INDEX.md`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/README_cloudlog_automator.md`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/クラウドログ分類と運用ガイド.md`
