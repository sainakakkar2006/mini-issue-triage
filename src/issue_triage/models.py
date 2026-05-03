from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True)
class Issue:
    id: int
    title: str
    body: str
    labels: list[str]
    created_at: date
    comments: int = 0


@dataclass(frozen=True)
class RankedIssue:
    issue: Issue
    score: int
    reasons: list[str]
    duplicate_group: int | None = None

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["issue"]["created_at"] = self.issue.created_at.isoformat()
        return payload

