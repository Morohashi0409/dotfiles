#!/usr/bin/env python3
"""
Fetch GitHub day activity without specifying ticket numbers.

Usage:
  python3 fetch_github_day_activity.py 2026-05-13
  python3 fetch_github_day_activity.py 2026-05-13 --actor Morohashi0409
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass


DEFAULT_REPOS = ["Resily/dxp", "Resily/WellCom"]


@dataclass
class CmdResult:
    ok: bool
    output: list[dict]
    error: str | None = None


def run_json(cmd: list[str]) -> CmdResult:
    try:
        cp = subprocess.run(cmd, check=True, capture_output=True, text=True)
        raw = cp.stdout.strip()
        return CmdResult(ok=True, output=json.loads(raw) if raw else [])
    except subprocess.CalledProcessError as e:
        return CmdResult(ok=False, output=[], error=(e.stderr or e.stdout or str(e)).strip())


def fetch_for_repo(repo: str, day: str, actor: str) -> dict:
    pr = run_json(
        [
            "gh",
            "pr",
            "list",
            "-R",
            repo,
            "--state",
            "all",
            "--search",
            f"author:{actor} updated:{day}",
            "--json",
            "number,title,state,updatedAt,mergedAt,url",
        ]
    )
    issue = run_json(
        [
            "gh",
            "issue",
            "list",
            "-R",
            repo,
            "--state",
            "all",
            "--search",
            f"involves:{actor} updated:{day}",
            "--json",
            "number,title,state,updatedAt,url",
        ]
    )
    return {
        "repo": repo,
        "pull_requests": pr.output,
        "issues": issue.output,
        "errors": {
            "pull_requests": pr.error,
            "issues": issue.error,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("day", help="Target day in YYYY-MM-DD")
    parser.add_argument("--actor", default="Morohashi0409")
    parser.add_argument("--repos", nargs="*", default=DEFAULT_REPOS)
    args = parser.parse_args()

    result = {
        "day": args.day,
        "actor": args.actor,
        "repos": [fetch_for_repo(repo, args.day, args.actor) for repo in args.repos],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

