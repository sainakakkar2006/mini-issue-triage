from __future__ import annotations

import argparse
from datetime import date

from .io import load_issues
from .reporting import ranked_to_json, ranked_to_text, write_report
from .triage import rank_issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="issue-triage",
        description="Rank bug reports and group likely duplicate issues.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    rank = subcommands.add_parser("rank", help="rank issues from a JSON file")
    rank.add_argument("issues", help="path to issues JSON")
    rank.add_argument("--format", choices=["text", "json"], default="text")
    rank.add_argument("--today", help="override today's date, YYYY-MM-DD")
    rank.add_argument("--out", help="optional report path")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    today = date.fromisoformat(args.today) if args.today else None
    ranked = rank_issues(load_issues(args.issues), today=today)
    report = ranked_to_json(ranked) if args.format == "json" else ranked_to_text(ranked)

    if args.out:
        write_report(report, args.out)
    print(report)
    return 0

