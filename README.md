# Mini Issue Triage

**Name:** Saina Kakkar

## Design and Implementation

This is a small command-line tool that ranks bug reports and groups issues
that might be duplicates. I made it because real software teams often have
many bugs and not enough time to look at all of them first. A tool like this
can help decide what should be checked first.

The tool reads a JSON file with issues, then gives each issue a score based
on:

- labels such as `critical`, `high`, `bug`, or `security`
- keywords such as `crash`, `login`, or `data loss`
- how old the issue is
- how many comments it has
- whether it looks similar to another issue

Then it prints the issues from highest priority to lowest priority. I used a
heap for the ranking and simple text matching for the duplicate grouping.

## Run

Rank the sample issues:

```bash
PYTHONPATH=src python -m issue_triage rank examples/issues.json
```

Write a JSON report:

```bash
PYTHONPATH=src python -m issue_triage rank examples/issues.json --format json --out reports/triage.json
```

## Input Example

```json
[
  {
    "id": 101,
    "title": "Login crashes after password reset",
    "body": "Users see a crash after resetting their password.",
    "labels": ["bug", "crash", "high"],
    "created_at": "2026-04-28",
    "comments": 4
  }
]
```

## Output Example

```text
4 issue(s) ranked

1. #104 score=249
   Security issue in export endpoint
   reasons: label:security +70, label:critical +80, label:bug +20
```

Notice the `reasons` line. I included it so the score is not a mystery. In
the example above you can read exactly why #104 came first: the security
label alone is worth 70 points, which is a choice I made on purpose, because
a security bug that waits in the backlog is a bigger risk than a UI bug.

## Verify

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

The tests cover the scoring and the duplicate grouping.

## Notes

Could've had the tool print just a sorted list, but a score without an
explanation is hard to trust, so every ranking shows exactly which labels
and keywords contributed and by how much. This project is small, but it
connects data structures (dictionaries, sets, heaps, sorting) to a real
developer workflow.
