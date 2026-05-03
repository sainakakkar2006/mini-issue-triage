from __future__ import annotations

import heapq
from datetime import date

from .duplicates import duplicate_groups
from .models import Issue, RankedIssue
from .scoring import score_issue


def rank_issues(issues: list[Issue], *, today: date | None = None) -> list[RankedIssue]:
    groups = duplicate_groups(issues)
    heap: list[tuple[int, date, int, RankedIssue]] = []

    for issue in issues:
        score, reasons = score_issue(issue, today=today)
        ranked = RankedIssue(
            issue=issue,
            score=score,
            reasons=reasons,
            duplicate_group=groups.get(issue.id),
        )
        heapq.heappush(heap, (-score, issue.created_at, issue.id, ranked))

    ranked_issues: list[RankedIssue] = []
    while heap:
        ranked_issues.append(heapq.heappop(heap)[3])
    return ranked_issues

