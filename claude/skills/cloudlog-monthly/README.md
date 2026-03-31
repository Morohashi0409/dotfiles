# CloudLog Monthly

月次の CloudLog 入力を end-to-end で進めるための skill です。
この skill は「月次 JSON を作るだけ」ではなく、「CloudLog にその月を登録して、保存結果まで確認する」前提で使います。

## 実行イメージ

<video controls src="/private/var/folders/4w/dd_2c5r1351g9mll057964wc0000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=A3BC3CD0-DCB1-46CF-95DC-08EE9FEC7242&code=001&library=1&type=3&mode=1&loc=true&cap=true.mov/画面収録 2026-03-31 18.05.54.mov"></video>

[動画を開く](/private/var/folders/4w/dd_2c5r1351g9mll057964wc0000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=A3BC3CD0-DCB1-46CF-95DC-08EE9FEC7242&code=001&library=1&type=3&mode=1&loc=true&cap=true.mov/画面収録%202026-03-31%2018.05.54.mov)

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

## ユーザーが用意するもの

- 対象月
  例: `2026-03`
- Daily ノート
  各営業日について、何をやったかが最低限わかる状態
- その月の勤怠 PDF 1 つ
  添付するか `~/Downloads` に置く
- その月の Outlook / Teams 予定 PDF 1 つ
  添付するか `~/Downloads` に置く
- カテゴリやマイパターンの変更情報
  先月と CloudLog のカテゴリ構成が変わっていれば伝える
- 自動入力までやる場合は、CloudLog にログイン済みの Chrome debug セッション
  CloudLog の勤務表ページを開いた状態まで含む

## 標準のファイル配置

この skill では、月次データを次の形にそろえます。

```text
CloudLog/
├── monthly-sources/
│   └── YYYY-MM/
│       ├── YYYY-MM_attendance.pdf
│       └── YYYY-MM_outlook-calendar.pdf
├── monthly-json/
│   └── YYYY-MM_cloudlog.json
├── check_cloudlog_automator_ready.py
├── cloudlog_automator.py
├── validate_json.py
└── クラウドログ分類と運用ガイド.md
```

主なファイルの役割は以下です。

- `validate_json.py`
  - 作成した月次 JSON が CloudLog に保存できる形か確認する
- `check_cloudlog_automator_ready.py`
  - 自動入力を始めてよい状態か事前確認する
- `cloudlog_automator.py`
  - 月次 JSON を使って CloudLog へ自動入力し、保存処理まで進める
- `クラウドログ分類と運用ガイド.md`
  - 日ごとの作業内容をどのカテゴリに入れるか判断するための基準
- `monthly-sources/YYYY-MM/`
  - その月の勤怠 PDF と予定 PDF を置く場所
- `monthly-json/YYYY-MM_cloudlog.json`
  - その月の CloudLog 入力データ本体

## 自動入力の前提条件

`cloudlog_automator.py` を使う前に、次の状態が必要です。

- Chrome が remote debugging 付きで起動している
  - 例: `--remote-debugging-port=9222`
- CloudLog にログイン済み
- CloudLog の勤務表ページを開いている
- `monthly-json/YYYY-MM_cloudlog.json` がある
- `validate_json.py` が通っている
- `check_cloudlog_automator_ready.py` が通っている

Chrome の起動例:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/ChromeDebug"
```

## 推奨実行順

自動入力までやる場合は、次の順で進めます。

```bash
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/prepare_monthly_sources.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/check_monthly_inputs.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/normalize_cloudlog_json.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json --in-place
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/validate_json.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/check_cloudlog_automator_ready.py 2026-03
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/cloudlog_automator.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json
```

この順を崩さず、validator と readiness check を通してから automator を流します。

## JSON の最小イメージ

`monthly-json/YYYY-MM_cloudlog.json` は、CloudLog に登録する日別データそのものです。

```json
[
  {
    "date": "2026-03-02",
    "attendance": {
      "clock_in": "10:05",
      "clock_out": "19:00"
    },
    "cloudlog_entries": [
      {
        "category": "全社共通業務 > 商品や業務に紐づかない会議 > （アドモニ、本部会議）> 入力不要",
        "minutes": 25,
        "time_blocks": ["10:05-10:30"]
      },
      {
        "category": "マイパターン登録済みの業務",
        "minutes": 30,
        "time_blocks": ["10:30-11:00"]
      }
    ],
    "needs_confirmation": false
  }
]
```

見方のポイント:

- 1 要素が 1 日分
- `attendance` は勤怠時刻
- `cloudlog_entries` は工数カテゴリの一覧
- `time_blocks` の 1 件が CloudLog 上の 1 行になる
- `minutes` は画面入力値ではなく、検証用の期待値
- `needs_confirmation: true` の日は自動入力をスキップする
- 全休など勤怠を入れない日は `attendance: null` にできる

## `validate_json.py` が保証すること

`validate_json.py` は、JSON が CloudLog 入力用として最低限成立しているかを確認します。

主に見ているのは以下です。

- `date` が `YYYY-MM-DD` 形式か
- `attendance` が正しい形か
- `clock_in` / `clock_out` が 5 分刻みか
- `time_blocks` が `HH:MM-HH:MM` 形式か
- `time_blocks` の開始・終了が 5 分刻みか
- `minutes` が数値で 5 分単位か

注意点:

- warning だけなら終了コード `0` で通る
- `time_blocks` 合計と `minutes` のズレなどは warning 扱いになることがある
- warning が残っていると automator で保存失敗することがある

つまり、validator は必須ですが、通っただけで完全に安全とは限りません。

## `cloudlog_automator.py` がやること

`cloudlog_automator.py` は、CloudLog の勤務表画面に対して次の操作をします。

1. Chrome debug session に接続する
2. CloudLog のタブを見つける
3. 対象日を含む週に移動する
4. その日の `編集` ボタンを押す
5. `attendance` があれば勤務開始・終了を入力する
6. `time_blocks` を 1 ブロックずつ工数行として追加する
7. カテゴリを選ぶ
8. サマリーを確認して `保存` を押す
9. 保存できた日と失敗した日をログで出す

カテゴリ選択は次の順です。

- まずマイパターンで検索
- 見つからなければ `>` 区切りの階層パスとして通常タブで選択

## automator が実際に触る UI

- CloudLog の勤務表ページ
- 日別の `編集` ボタン
- 勤務開始・終了入力欄
- 工数行
- カテゴリ picker
- `保存` ボタン

## 補足ドキュメント

詳細を確認したい場合は、次も参照できます。

- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md`
  - JSON 契約と自動入力の前提を詳しく説明したファイル
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/README_cloudlog_automator.md`
  - `cloudlog_automator.py` 単体の詳しい README
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/別スレッド用_月次入力テンプレート.md`
  - 他スレッドへそのまま渡す実行テンプレート

## ユーザーがやらなくていいこと

- PDF のリネーム
- `monthly-sources` への移動
- JSON の 5 分刻み調整
- JSON の整合性チェック
- 自動入力前の細かい前処理

## この skill が止まって質問する条件

- PDF が見つからない
- `~/Downloads` に候補 PDF が複数あって判別できない
- Daily と GitHub を見ても、その日のカテゴリ配分が決め切れない
- CloudLog 側のカテゴリやマイパターンが変わっていて、既存 JSON と一致しない
- 月末最終日がまだ未確定
- CloudLog の画面変更で automator が安全に続行できない

## 完了の定義

`YYYY-MM_cloudlog.json` ができた、だけでは完了ではありません。

自動入力まで依頼された場合は、次の状態までを完了扱いにします。

- JSON が validate 済み
- automator 実行済み
- 保存できた日が確認済み
- 失敗日や保留日があれば理由つきで整理済み

## 補助スクリプト

使える補助スクリプトは以下です。

- `scripts/prepare_monthly_sources.py`
  - PDF を所定の場所へコピーし、決まった名前にそろえる
- `scripts/check_monthly_inputs.py`
  - 必要ファイルがそろっているか確認する
- `scripts/normalize_cloudlog_json.py`
  - JSON 内の時刻を 5 分刻みにそろえる
- `check_cloudlog_automator_ready.py`
  - 自動入力を始めてよい状態か事前確認する

## 注意点

- 作業メモの形式は人によって違って問題ありませんが、各営業日の作業内容が最低限わかる必要があります。
- PDF は添付が最優先です。添付がなければ `~/Downloads` を見にいきます。
- `attendance` と `time_blocks` は 5 分刻みにそろっていないと CloudLog に保存できません。
- 自動入力を使う場合は、CloudLog にログイン済みで、勤務表ページを開いた Chrome debug セッションが必要です。
- automator の終了コードは、全日成功で `0`、準備不足または一部日付失敗で `1` です。

## よくある失敗

- ブラウザ接続に失敗する
  - Chrome が `--remote-debugging-port=9222` 付きで起動しているか確認する
- CloudLog タブが見つからない
  - 勤務表ページを開いてログイン済みか確認する
- カテゴリが見つからない
  - マイパターン未登録、または CloudLog 側のカテゴリ構成変更を疑う
- 保存されたように見えて再読込すると消える
  - `validate_json.py` を再実行し、5 分刻みと warning の有無を見直す
- 編集ボタンが見つからない
  - 対象週が合っていないか、CloudLog の UI が変わっている可能性がある
