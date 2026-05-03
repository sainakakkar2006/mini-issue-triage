import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from issue_triage.cli import main
from issue_triage.io import load_issues
from issue_triage.reporting import ranked_to_json
from issue_triage.triage import rank_issues


class IOReportingCLITests(unittest.TestCase):
    def test_loads_issues_from_json(self):
        with tempfile.TemporaryDirectory() as temp_name:
            path = Path(temp_name) / "issues.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": 1,
                            "title": "Crash",
                            "body": "App crash",
                            "labels": ["Bug"],
                            "created_at": "2026-04-30",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            issues = load_issues(path)

        self.assertEqual(issues[0].labels, ["bug"])

    def test_json_report_serializes_dates(self):
        ranked = rank_issues(load_issues("examples/issues.json"))
        payload = json.loads(ranked_to_json(ranked))

        self.assertIn("created_at", payload["ranked_issues"][0]["issue"])

    def test_cli_writes_report(self):
        with tempfile.TemporaryDirectory() as temp_name:
            out_path = Path(temp_name) / "report.json"
            with redirect_stdout(StringIO()):
                exit_code = main(["rank", "examples/issues.json", "--format", "json", "--out", str(out_path)])

            self.assertEqual(exit_code, 0)
            self.assertTrue(out_path.exists())


if __name__ == "__main__":
    unittest.main()
