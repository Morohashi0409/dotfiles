module.exports = {
  disableEmoji: false,
  format: "【{emoji}: {type}】 {subject}",
  list: [
    "fix",
    "feat",
    "refactor",
    "test",
    "style",
    "chore",
    "docs",
    "perf",
    "ci",
    "wip",
  ],
  maxMessageLength: 64,
  minMessageLength: 3,
  questions: ["type", "subject"],
  scopes: [],
  types: {
    chore: {
      description: "ドキュメントの生成やビルドプロセス、ライブラリなどの変更",
      emoji: "🤖",
      value: "chore",
    },
    ci: {
      description: "CI用の設定やスクリプトに関する変更",
      emoji: "⚙️",
      value: "ci",
    },
    docs: {
      description: "ドキュメントのみの変更",
      emoji: "✏️",
      value: "docs",
    },
    feat: {
      description: "新機能の追加や機能強化",
      emoji: "🎸",
      value: "feat",
    },
    fix: {
      description: "不具合の修正やバグフィックス",
      emoji: "🐛",
      value: "fix",
    },
    perf: {
      description: "パフォーマンス改善のためのコード変更",
      emoji: "⚡️",
      value: "perf",
    },
    refactor: {
      description: "機能追加やバグ修正を伴わないコード改善",
      emoji: "💡",
      value: "refactor",
    },
    style: {
      description: "コードの処理に影響しない変更（スペースや書式設定）",
      emoji: "💄",
      value: "style",
    },
    test: {
      description: "テストコードの追加、修正、更新",
      emoji: "💍",
      value: "test",
    },
    wip: {
      description: "作業中の状態を表す変更",
      emoji: "🚧",
      value: "wip",
    },
  },
};
