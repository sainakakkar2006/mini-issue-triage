# Mini Issue Triage

This is a small command-line tool that ranks bug reports and groups issues that might be duplicates.

I made it because real software teams often have many bugs and not enough time to look at all of them first. A tool like this can help decide what should be checked first.

## What It Does

The tool reads a JSON file with issues, then gives each issue a score.

The score is based on things like:

- labels such as `critical`, `high`, `bug`, or `security`
- keywords such as `crash`, `login`, or `data loss`
- how old the issue is
- how many comments it has
- whether it looks similar to another issue

Then it prints the issues from highest priority to lowest priority.

## Quick Start

Rank the sample issues:

```bash
PYTHONPATH=src python -m issue_triage rank examples/issues.json
```

Write a JSON report:

```bash
PYTHONPATH=src python -m issue_triage rank examples/issues.json --format json --out reports/triage.json
```

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests
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

The reasons are included so the score is not a mystery.

## What I Practiced

- dictionaries and sets
- heaps for ranking
- sorting
- simple text matching
- JSON input and output
- command-line tool design
- tests for scoring and duplicate grouping

This project is small, but it connects data structures to a real developer workflow.

