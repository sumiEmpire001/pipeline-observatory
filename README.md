# Pipeline Observatory

An offline Python CLI for summarizing exported CI pipeline runs. Reports overall success rate, outcome counts, mean duration, and per-workflow failures and average durations. Uses only the Python standard library.

## Usage

```bash
python observatory.py examples/runs.json
python observatory.py examples/runs.json --output report.json
```

Input is a JSON array or an object with a `runs` array. Each run must have `workflow`, `conclusion` (`success`, `failure`, `cancelled`, or `skipped`), `started_at`, and `completed_at` in ISO 8601 format with timezone information. Example input is in `examples/runs.json`.

## Tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs tests on Python 3.10, 3.12 and 3.13. This tool analyzes offline exports; it does not connect to GitHub or fetch private build logs.
