# Claude Code 通知システム

## 概要

Claude Code の通知イベント（Notification / Stop）時に、ローカル REST API 経由で Logitech MX Master 4 の haptic フィードバックをトリガーするシステム。

---

## アーキテクチャ

### イベントフロー

```
Claude Code イベント発火
  ↓
settings.json の hooks 定義を参照
  ↓
┌─────────────────────────────────┐
│ 1. haptic-trigger.sh 実行       │ ← 詳細な振動制御
│    （イベント種別に応じた振動）  │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│ 2. notification.sh 実行         │ ← 統一的な衝撃フィードバック
│    （固定エンドポイント呼び出し） │
└─────────────────────────────────┘
```

---

## コンポーネント詳細

### 1. haptic-trigger.sh
**場所**: `~/.claude/hooks/haptic-trigger.sh`

#### 入力
- Claude Code からの JSON（hook_event_name, notification_type を含む）

#### 処理
1. `hook_event_name` を抽出
2. イベント種別に応じて waveform を選択
3. REST API 経由で haptic フィードバックをトリガー

#### waveform マッピング

**Notification イベント**:
| notification_type | waveform | 用途 |
|------------------|----------|------|
| `permission_prompt` | `knock` | 権限要求の注意喚起 |
| `idle_prompt` | `ringing` | ユーザー入力待ち |
| `elicitation_dialog` | `jingle` | 質問・ダイアログ |
| `auth_success` | `happy_alert` | 認証成功 |
| その他 | `wave` | デフォルト振動 |

**Stop イベント**:
- `waveform = "completed"` （完了感を演出）

#### API エンドポイント
```
POST https://local.jmw.nz:41443/haptic/{waveform}
```

#### 特徴
- **入力依存**: JSON から動的に振動パターンを決定
- **意味のある振動**: ユーザーに状況を伝える
- タイムアウト: 2秒（接続）/ 5秒（全体）
- 非ブロッキング: エラー時も黙示的に続行

---

### 2. notification.sh
**場所**: `~/.claude/hooks/notification.sh`

#### 入力
なし（イベント情報は参照しない）

#### 処理
- REST API に固定エンドポイント呼び出しのみ

#### API エンドポイント
```
POST https://local.jmw.nz:41443/haptic/sharp_collision
```

#### 特徴
- **固定エンドポイント**: すべてのイベントで `sharp_collision`
- **統一的フィードバック**: 確実な完了通知
- バックグラウンド実行: `&` で即座に戻る
- タイムアウト: 1秒（接続）/ 1秒（全体）
- 非ブロッキング: エラー時も黙示的に続行

---

## 設定方法

### `claude/settings.json`

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/resily0808/.claude/hooks/haptic-trigger.sh"
          }
        ]
      },
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/notification.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/resily0808/.claude/hooks/haptic-trigger.sh"
          }
        ]
      },
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/notification.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 動作例

### シナリオ 1: 権限要求時

```
ユーザーが Bash コマンド実行を試みる
  ↓
[Notification イベント] notification_type = "permission_prompt"
  ↓
haptic-trigger.sh:
  - waveform = "knock" ← 注意を引く振動
  - POST /haptic/knock
  ↓
notification.sh:
  - POST /haptic/sharp_collision ← 確実な完了通知
```

**体感**: 注意深い振動（knock）+ 衝撃フィードバック

---

### シナリオ 2: 処理完了時

```
Claude Code が応答を完成させる
  ↓
[Stop イベント]
  ↓
haptic-trigger.sh:
  - waveform = "completed" ← 完了感
  - POST /haptic/completed
  ↓
notification.sh:
  - POST /haptic/sharp_collision ← 確実な完了通知
```

**体感**: 充足感ある振動（completed）+ 衝撃フィードバック

---

## 依存関係

- **HapticWebPlugin**: Logitech MX Master 4 の haptic フィードバックを制御する外部ツール
- **REST API エンドポイント**: `https://local.jmw.nz:41443`

---

## トラブルシューティング

### 通知が来ない場合

1. HapticWebPlugin が起動しているか確認
2. ローカル REST API `https://local.jmw.nz:41443` が応答しているか確認
3. ファイアウォール設定を確認

### 通知が遅い場合

- `notification.sh` でバックグラウンド実行 + タイムアウト設定済み
- タイムアウト値を調整する場合は `--max-time` と `--connect-timeout` パラメータを変更

---

## 履歴

**2026-03-05**:
- osascript から REST API へ移行完了
- haptic-trigger.sh の重複エントリを削除
- notification.sh に早期終了（バックグラウンド + タイムアウト）を追加
