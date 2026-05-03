from __future__ import annotations

from .models import Issue
from .scoring import issue_terms
from .text import jaccard_similarity


def duplicate_groups(issues: list[Issue], *, threshold: float = 0.35) -> dict[int, int]:
    """Assign duplicate group numbers to likely duplicate issues."""

    terms_by_id = {issue.id: issue_terms(issue) for issue in issues}
    group_by_issue: dict[int, int] = {}
    next_group = 1

    for index, issue in enumerate(issues):
        for other in issues[index + 1 :]:
            similarity = jaccard_similarity(terms_by_id[issue.id], terms_by_id[other.id])
            if similarity < threshold:
                continue

            group = group_by_issue.get(issue.id) or group_by_issue.get(other.id)
            if group is None:
                group = next_group
                next_group += 1
            group_by_issue[issue.id] = group
            group_by_issue[other.id] = group

    return group_by_issue
