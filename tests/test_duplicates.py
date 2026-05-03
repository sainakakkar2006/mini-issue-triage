import unittest
from datetime import date

from issue_triage.duplicates import duplicate_groups
from issue_triage.models import Issue


class DuplicateTests(unittest.TestCase):
    def test_groups_similar_issues(self):
        issues = [
            Issue(1, "Login crash", "Crash after password reset", ["bug"], date(2026, 4, 1)),
            Issue(2, "Password reset login crash", "Crash after reset", ["bug"], date(2026, 4, 2)),
            Issue(3, "Settings typo", "Small typo on settings page", ["low"], date(2026, 4, 3)),
        ]

        groups = duplicate_groups(issues, threshold=0.3)

        self.assertEqual(groups[1], groups[2])
        self.assertNotIn(3, groups)


if __name__ == "__main__":
    unittest.main()

