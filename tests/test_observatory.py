import json
import tempfile
import unittest
from pathlib import Path
from observatory import analyze, main


def sample(outcome="success", name="CI", finish="2026-11-05T10:02:00Z"):
    return {"workflow": name, "conclusion": outcome, "started_at": "2026-11-05T10:00:00Z", "completed_at": finish}


class ObservatoryTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(analyze([])["total"], 0)
    def test_success_rate(self):
        self.assertEqual(analyze([sample(), sample("failure")])["success_rate"], 0.5)
    def test_duration(self):
        self.assertEqual(analyze([sample()])["mean_duration_seconds"], 120)
    def test_grouping(self):
        self.assertEqual(analyze([sample(), sample("failure", "Deploy")])["workflows"]["Deploy"]["failures"], 1)
    def test_invalid_conclusion(self):
        with self.assertRaises(ValueError):
            analyze([sample("unknown")])
    def test_negative_duration(self):
        with self.assertRaises(ValueError):
            analyze([sample(finish="2026-11-05T09:00:00Z")])
    def test_json_export(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "runs.json"
            target = Path(directory) / "report.json"
            source.write_text(json.dumps({"runs": [sample()]}), encoding="utf-8")
            main([str(source), "--output", str(target)])
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))["total"], 1)


if __name__ == "__main__":
    unittest.main()
