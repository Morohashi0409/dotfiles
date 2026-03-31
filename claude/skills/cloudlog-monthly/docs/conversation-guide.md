# Conversation Guide

This guide shows how to talk to `cloudlog-monthly` in chat.

The main idea is simple:

- attach the month’s PDFs if you have them
- tell the agent the target month
- say whether you want JSON only or full CloudLog entry
- answer only when the agent hits a real ambiguity

## Recommended Style

Prefer short, direct requests.

Good:

- "2026-03 の CloudLog 月次入力を完了して。資料を添付します。"
- "この添付資料で 2026-03 の JSON を作って。自動入力はまだ不要。"
- "2026-03 を CloudLog まで入れて。必要なら Chrome も起動して。"

Not necessary:

- long explanation of folder moves
- manual PDF rename instructions
- detailed 5-minute rounding instructions

The skill handles those.

## Attachment-First Request

The cleanest request is to attach the attendance PDF and calendar PDF and then say:

```text
2026-03 の CloudLog 月次入力を完了して。
添付した資料を使ってください。
自動入力までお願いします。
カテゴリ変更はありません。
```

## If You Only Want JSON

```text
2026-03 の CloudLog 月次 JSON だけ作ってください。
資料は添付します。
CloudLog への自動入力はまだ不要です。
```

## If Files Are Not Attached

If the PDFs are already in `Downloads`, a short request is enough:

```text
2026-03 の CloudLog 月次入力を進めてください。
PDF は Downloads にある想定です。
自動入力までお願いします。
```

The skill should look at attachments first, then canonical monthly files, then `~/Downloads`.

## Chat-Style Chrome Preparation

Chrome preparation can also be requested in chat.

Example:

```text
2026-03 の CloudLog を最後まで入れてください。
必要なら Chrome debug も起動してください。
ログインが必要になったらそのタイミングで言ってください。
```

Or more explicitly:

```text
自動入力までやってください。
CloudLog 用の Chrome を開くところから進めてください。
ログイン操作が必要なら待機してください。
```

## Practical Conversation Flow

In practice, the conversation often looks like this:

1. User attaches PDFs and gives the month
2. Agent checks readiness and source files
3. Agent asks only if:
   - the PDFs are missing
   - multiple PDFs look plausible
   - category evidence is too weak
   - category structure changed
   - Chrome / CloudLog is not ready for safe automatic entry
4. User answers the blocker
5. Agent continues through JSON, validation, readiness check, and automator run

## Minimal Request Templates

### Full Monthly Run

```text
2026-03 の CloudLog 月次入力を完了して。
添付資料を使ってください。
自動入力までお願いします。
```

### Full Run With Chrome Start

```text
2026-03 の CloudLog 月次入力を完了して。
添付資料を使ってください。
Chrome の起動が必要ならそこから進めてください。
自動入力までお願いします。
```

### JSON Refresh Only

```text
2026-03 の monthly-json を更新してください。
添付資料を使ってください。
CloudLog の自動入力はまだ不要です。
```

### Existing JSON + Auto Entry Only

```text
2026-03 の既存 JSON を使って CloudLog へ入力してください。
必要なら Chrome debug を起動してください。
保存できた日と失敗日まで確認してください。
```

## What To Mention If Relevant

Mention these only when they matter:

- "カテゴリ変更あり"
- "マイパターン変わりました"
- "今月末はまだ未確定です"
- "JSON は既存のものを使ってください"
- "自動入力はせず JSON までで止めてください"

## What You Usually Do Not Need To Explain

You usually do not need to explain:

- canonical file naming
- `monthly-sources` placement
- JSON normalization
- validator order
- readiness check order

Those are execution details owned by the skill.
