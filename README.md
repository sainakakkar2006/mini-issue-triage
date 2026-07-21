# mini-issue-triage

**Name:** Saina Kakkar

## Design and Implementation

This is a small command-line tool that ranks bug reports and groups issues
that might be duplicates. I made it because real software teams often have
many bugs and not enough time to look at all of them first. A tool like this
can help decide what should be checked first.

The tool reads a JSON file with issues, then gives each issue a score, then
prints the issues from highest priority to lowest priority. I used a heap
for the ranking and simple text matching for the duplicate grouping.

```
issues.json ──► score each issue ──► heap ──► ranked list with reasons
                (labels, keywords,           (duplicates grouped)
                 age, comments)
```

## The Scoring Table

The exact weights live in `scoring.py`. Labels:

| Label | Points |
|---|---|
| `critical` | 80 |
| `security` | 70 |
| `high` | 55 |
| `regression` | 35 |
| `medium` | 30 |
| `bug` | 20 |
| `low` | 10 |

Keywords found in the title or body:

| Keyword | Points |
|---|---|
| `data loss` | 70 |
| `security` | 60 |
| `crash` | 45 |
| `payment` | 40 |
| `login` | 25 |
| `timeout` | 20 |
| `slow` | 15 |

On top of that, older issues and issues with more comments earn extra
points. The weights are my judgment calls, not science. `security` scoring
above `high` was on purpose: a security bug that waits in a backlog is a
bigger risk than a UI bug, even a loud one.

## Run

Rank the sample issues:

```bash
PYTHONPATH=src python -m issue_triage rank examples/issues.json
```

Write a JSON report:

```bash
PYTHONPATH=src python -m issue_triage rank examples/issues.json --format json --out reports/triage.json
```

## CLI Reference

| Argument | Default | What it does |
|---|---|---|
| `issues` | (required) | Path to the issues JSON file |
| `--format` | `text` | `text` or `json` |
| `--today` | real today | Override today's date (`YYYY-MM-DD`) |
| `--out` | none | Write the report to a file |

The `--today` flag looks strange until you think about the age scoring. An
issue's age depends on what day it is, so without this flag the same input
could produce different scores tomorrow. Tests pin `--today` so the output
is fully deterministic.

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

The `reasons` line is there so the score is not a mystery. You
can check the math against the tables above: 70 + 80 + 20 accounts for 170
of the 249 points, and the rest comes from keywords, age, and comments.

## Project Layout

```
src/issue_triage/
  cli.py         the rank subcommand
  models.py      the Issue dataclass
  io.py          reading the issues JSON
  scoring.py     LABEL_SCORES, KEYWORD_SCORES, age and comment bonuses
  duplicates.py  similarity grouping for possible duplicates
  triage.py      puts scoring + duplicates together, heap ranking
  text.py        text normalization helpers
  reporting.py   text / json formatters
tests/           scoring, duplicates, triage, and CLI tests
```

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

## License

MIT. See the [LICENSE](LICENSE) file.
