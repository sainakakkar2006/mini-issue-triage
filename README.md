# Mini Issue Triage

A small command-line tool that ranks bug reports and groups likely duplicates. It is built as a practical second-year software-development project using dictionaries, heaps, sets, sorting, and text processing.

## Why This Project Exists

Small teams often have many bug reports but limited time. This tool helps answer:

- Which issues should we look at first?
- Which bugs might be duplicates?
- Why did an issue receive its priority score?

## Quick Start

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

## Input Format

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

## What The Score Considers

- severity labels like `critical`, `high`, `medium`, and `low`
- keywords like `crash`, `security`, `data loss`, and `login`
- issue age
- number of comments
- whether the issue has bug-related labels

## What This Shows

This repo demonstrates practical software-development thinking: prioritization, text processing, basic ranking algorithms, JSON input/output, CLI design, and tests.

