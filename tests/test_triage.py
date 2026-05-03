import unittest
from datetime import date

from issue_triage.models import Issue
from issue_triage.triage import rank_issues


class TriageTests(unittest.TestCase):
    def test_ranks_highest_score_first(self):
        issues = [
            Issue(1, "Small typo", "Typo in docs", ["low"], date(2026, 4, 29)),
            Issue(2, "Security data loss", "Security bug causes data loss", ["critical", "security"], date(2026, 4, 29)),
        ]

        ranked = rank_issues(issues, today=date(2026, 4, 30))

        self.assertEqual(ranked[0].issue.id, 2)
        self.assertGreater(ranked[0].score, ranked[1].score)


if __name__ == "__main__":
    unittest.main()

