from __future__ import annotations

import json
from pathlib import Path

from .models import RankedIssue


def ranked_to_json(ranked: list[RankedIssue]) -> str:
    payload = {
        "total_issues": len(ranked),
        "ranked_issues": [issue.to_dict() for issue in ranked],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def ranked_to_text(ranked: list[RankedIssue]) -> str:
    if not ranked:
        return "No issues to triage."

    lines = [f"{len(ranked)} issue(s) ranked", ""]
    for position, item in enumerate(ranked, start=1):
        group = f" duplicate-group={item.duplicate_group}" if item.duplicate_group else ""
        lines.append(f"{position}. #{item.issue.id} score={item.score}{group}")
        lines.append(f"   {item.issue.title}")
        lines.append(f"   reasons: {', '.join(item.reasons)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def write_report(content: str, out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")

