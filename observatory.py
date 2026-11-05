"""Analyze CI pipeline runs from a JSON export."""
import argparse
import collections
import datetime as dt
import json
import statistics


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def analyze(runs):
    if not isinstance(runs, list):
        raise ValueError("runs must be a list")
    outcomes = collections.Counter()
    grouped = collections.defaultdict(list)
    durations = []
    for run in runs:
        name, conclusion = run["workflow"], run["conclusion"]
        if not isinstance(name, str) or not name or conclusion not in ("success", "failure", "cancelled", "skipped"):
            raise ValueError("invalid workflow or conclusion")
        duration = (timestamp(run["completed_at"]) - timestamp(run["started_at"])).total_seconds()
        if duration < 0:
            raise ValueError("negative duration")
        outcomes[conclusion] += 1
        grouped[name].append((conclusion, duration))
        durations.append(duration)
    return {
        "total": len(runs),
        "success_rate": round(outcomes["success"] / len(runs), 4) if runs else None,
        "outcomes": dict(sorted(outcomes.items())),
        "mean_duration_seconds": round(statistics.mean(durations), 2) if durations else None,
        "workflows": {
            name: {
                "runs": len(values),
                "failures": sum(status == "failure" for status, _ in values),
                "mean_duration_seconds": round(statistics.mean(duration for _, duration in values), 2)
            }
            for name, values in sorted(grouped.items())
        }
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize exported CI runs")
    parser.add_argument("file", help="Path to JSON file")
    parser.add_argument("--output", help="Optional report file")
    args = parser.parse_args(argv)
    try:
        with open(args.file, encoding="utf-8") as source:
            data = json.load(source)
        report = analyze(data["runs"] if isinstance(data, dict) else data)
        result = json.dumps(report, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as target:
                target.write(result + "\n")
        else:
            print(result)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
