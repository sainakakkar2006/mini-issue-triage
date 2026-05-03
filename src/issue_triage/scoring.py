from __future__ import annotations

from datetime import date

from .models import Issue
from .text import tokenize


LABEL_SCORES = {
    "critical": 80,
    "high": 55,
    "medium": 30,
    "low": 10,
    "security": 70,
    "bug": 20,
    "regression": 35,
}

KEYWORD_SCORES = {
    "data loss": 70,
    "security": 60,
    "crash": 45,
    "payment": 40,
    "login": 25,
    "timeout": 20,
    "slow": 15,
}


def score_issue(issue: Issue, *, today: date | None = None) -> tuple[int, list[str]]:
    today = today or date.today()
    score = 0
    reasons: list[str] = []

    for label in issue.labels:
        if label in LABEL_SCORES:
            points = LABEL_SCORES[label]
            score += points
            reasons.append(f"label:{label} +{points}")

    combined_text = f"{issue.title} {issue.body}".lower()
    for keyword, points in KEYWORD_SCORES.items():
        if keyword in combined_text:
            score += points
            reasons.append(f"keyword:{keyword} +{points}")

    age_days = max((today - issue.created_at).days, 0)
    age_points = min(age_days // 2, 20)
    if age_points:
        score += age_points
        reasons.append(f"age:{age_days}d +{age_points}")

    comment_points = min(issue.comments * 2, 20)
    if comment_points:
        score += comment_points
        reasons.append(f"comments:{issue.comments} +{comment_points}")

    if not reasons:
        reasons.append("baseline +0")

    return score, reasons


def issue_terms(issue: Issue) -> set[str]:
    return tokenize(f"{issue.title} {issue.body} {' '.join(issue.labels)}")

