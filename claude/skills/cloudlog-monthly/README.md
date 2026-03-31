# CloudLog Monthly

月次の CloudLog 入力をまとめて進めるための skill です。
必要なデータをそろえ、月次 JSON を作成し、必要なら CloudLog への自動入力までつなぎます。

## 実行イメージ

<video controls src="/private/var/folders/4w/dd_2c5r1351g9mll057964wc0000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=A3BC3CD0-DCB1-46CF-95DC-08EE9FEC7242&code=001&library=1&type=3&mode=1&loc=true&cap=true.mov/画面収録 2026-03-31 18.05.54.mov"></video>

[動画を開く](/private/var/folders/4w/dd_2c5r1351g9mll057964wc0000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=A3BC3CD0-DCB1-46CF-95DC-08EE9FEC7242&code=001&library=1&type=3&mode=1&loc=true&cap=true.mov/画面収録%202026-03-31%2018.05.54.mov)

## 何をするものか

- 対象月を `YYYY-MM` で決める
- 勤怠 PDF と予定表 PDF を決まった場所にそろえる
- 月次入力用の `YYYY-MM_cloudlog.json` を作る
- JSON を検証し、必要なら CloudLog へ自動入力する

## 必要なデータ

最低限あるとよいものは以下です。

- 対象月
- 勤怠 PDF
- Outlook カレンダー PDF
- 日ごとの作業メモ
- CloudLog の分類ルール

補足:
- PDF は月次の在席時間や予定の根拠として使います。
- 作業メモは、日ごとのカテゴリ分けや時間帯の判断に使います。
- 作業メモの形式は人によって違って問題ありません。

## 私のケース

私の運用では、作業メモとして Obsidian の Daily note を使っています。

- Daily notes: `/Users/resily0808/Documents/Obsidian Vault/01_Daily`
- CloudLog root: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog`
- 月次入力元 PDF: `monthly-sources/YYYY-MM/`
- 月次 JSON: `monthly-json/YYYY-MM_cloudlog.json`

部内共有時はここを各自のメモ運用に置き換えて使う想定です。

## データの置き場所

この skill では以下の形にそろえる想定です。

```text
CloudLog/
├── monthly-sources/
│   └── YYYY-MM/
│       ├── YYYY-MM_attendance.pdf
│       └── YYYY-MM_outlook-calendar.pdf
├── monthly-json/
│   └── YYYY-MM_cloudlog.json
├── cloudlog_automator.py
├── validate_json.py
└── クラウドログ分類と運用ガイド.md
```

## 月次の流れ

1. 対象月を決める
2. 勤怠 PDF と Outlook カレンダー PDF を集める
3. PDF を `monthly-sources/YYYY-MM/` に決まった名前で置く
4. 作業メモを見ながら `YYYY-MM_cloudlog.json` を作る
5. JSON を 5 分刻みに正規化する
6. JSON を検証する
7. 必要なら CloudLog に自動入力する

## 補助スクリプト

使える補助スクリプトは以下です。

- `scripts/prepare_monthly_sources.py`
  - PDF を所定の場所へコピーし、決まった名前にそろえる
- `scripts/check_monthly_inputs.py`
  - 必要ファイルがそろっているか確認する
- `scripts/normalize_cloudlog_json.py`
  - JSON 内の時刻を 5 分刻みにそろえる

## 代表コマンド

```bash
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/prepare_monthly_sources.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/check_monthly_inputs.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/normalize_cloudlog_json.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json --in-place
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/validate_json.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/cloudlog_automator.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json
```

## 注意点

- PDF が複数あって正しいものが分からない場合は、人が確認したほうが安全です。
- 作業メモが薄い日は、GitHub 履歴や予定表など追加の根拠が必要になることがあります。
- `attendance` と `time_blocks` は 5 分刻みにそろっている必要があります。
- 部内メンバーごとに作業メモの置き場所や形式は違ってよいですが、月次 JSON を作るための根拠は必要です。
