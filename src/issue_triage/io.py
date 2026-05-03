from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .models import Issue


def load_issues(path: str | Path) -> list[Issue]:
    raw_items = json.loads(Path(path).read_text(encoding="utf-8"))
    return [_parse_issue(item) for item in raw_items]


def _parse_issue(item: dict) -> Issue:
    return Issue(
        id=int(item["id"]),
        title=str(item.get("title", "")).strip(),
        body=str(item.get("body", "")).strip(),
        labels=[str(label).strip().lower() for label in item.get("labels", [])],
        created_at=date.fromisoformat(str(item["created_at"])),
        comments=int(item.get("comments", 0)),
    )

