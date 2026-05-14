#!/usr/bin/env python3
"""
filter_pending_dates.py

既入力済みの日付を除外して、未入力分だけの JSON を出力する。

使い方:
  # 未入力分を stdout に出力
  python3 filter_pending_dates.py 2026-04

  # 直接ファイルに書き出す
  python3 filter_pending_dates.py 2026-04 --out /path/to/pending.json

  # 完了記録を手動で更新（automator 実行後に行う）
  python3 filter_pending_dates.py 2026-04 --mark-done 2026-04-01 2026-04-02 ...

完了記録ファイル:
  monthly-json/YYYY-MM_done.json
  形式: {"done": ["YYYY-MM-DD", ...]}

  automator が成功した日は自動で追記される（--mark-done オプション）。
  手動で編集しても構わない。
"""

import sys
import json
import argparse
from pathlib import Path

CLOUDLOG_ROOT = Path("/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog")
JSON_DIR = CLOUDLOG_ROOT / "monthly-json"


def done_path(month: str) -> Path:
    return JSON_DIR / f"{month}_done.json"


def load_done(month: str) -> set:
    p = done_path(month)
    if not p.exists():
        return set()
    data = json.loads(p.read_text(encoding="utf-8"))
    return set(data.get("done", []))


def save_done(month: str, dates: set) -> None:
    p = done_path(month)
    existing = load_done(month)
    merged = sorted(existing | dates)
    p.write_text(json.dumps({"done": merged}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[done] 完了記録を更新しました: {p}", file=sys.stderr)


def load_monthly(month: str) -> list:
    p = JSON_DIR / f"{month}_cloudlog.json"
    if not p.exists():
        print(f"[error] monthly JSON が見つかりません: {p}", file=sys.stderr)
        sys.exit(1)
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="未入力日のみ抽出する")
    parser.add_argument("month", help="対象月 YYYY-MM")
    parser.add_argument("--out", help="出力先ファイルパス（省略時は stdout）")
    parser.add_argument(
        "--mark-done",
        nargs="+",
        metavar="DATE",
        help="入力完了した日付を完了記録に追記する (YYYY-MM-DD ...)",
    )
    parser.add_argument(
        "--show-done",
        action="store_true",
        help="完了済み日付一覧を表示して終了",
    )
    args = parser.parse_args()

    month = args.month

    if args.mark_done:
        save_done(month, set(args.mark_done))
        return

    done = load_done(month)

    if args.show_done:
        if done:
            print("完了済み日付:")
            for d in sorted(done):
                print(f"  {d}")
        else:
            print("完了済み日付なし")
        return

    entries = load_monthly(month)
    pending = [e for e in entries if e["date"] not in done]

    skipped = [e["date"] for e in entries if e["date"] in done]
    if skipped:
        print(f"[skip] スキップ ({len(skipped)}日): {', '.join(skipped)}", file=sys.stderr)
    print(f"[info] 未入力 ({len(pending)}日): {', '.join(e['date'] for e in pending)}", file=sys.stderr)

    if not pending:
        print("[done] 全日入力済みです。", file=sys.stderr)
        sys.exit(0)

    out_json = json.dumps(pending, ensure_ascii=False, indent=2)

    if args.out:
        Path(args.out).write_text(out_json, encoding="utf-8")
        print(f"[info] 出力: {args.out}", file=sys.stderr)
    else:
        print(out_json)


if __name__ == "__main__":
    main()
