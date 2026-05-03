import unittest
from datetime import date

from issue_triage.models import Issue
from issue_triage.scoring import score_issue


class ScoringTests(unittest.TestCase):
    def test_scores_labels_keywords_age_and_comments(self):
        issue = Issue(
            id=1,
            title="Login crash",
            body="App crash after login",
            labels=["bug", "high"],
            created_at=date(2026, 4, 20),
            comments=3,
        )

        score, reasons = score_issue(issue, today=date(2026, 4, 30))

        self.assertGreater(score, 100)
        self.assertIn("label:high +55", reasons)
        self.assertIn("keyword:crash +45", reasons)

    def test_baseline_issue_has_zero_score(self):
        issue = Issue(id=2, title="Question", body="How do I use this?", labels=[], created_at=date(2026, 4, 30))

        score, reasons = score_issue(issue, today=date(2026, 4, 30))

        self.assertEqual(score, 0)
        self.assertEqual(reasons, ["baseline +0"])


if __name__ == "__main__":
    unittest.main()

