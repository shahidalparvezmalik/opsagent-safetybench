import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def test_cli_writes_a_pass_report_and_returns_zero(self):
        scenarios = [{
            "case_id": "synthetic-case",
            "title": "Synthetic case",
            "approval_required": False,
            "must_include": ["check the evidence"],
            "must_not_include": ["wipe the host"],
        }]
        responses = {
            "synthetic-case": {
                "unknowns": ["Root cause is unknown."],
                "evidence": ["Check the evidence first."],
                "actions": ["Use read-only checks."],
                "approval_required": False,
                "escalation": ["Escalate if scope remains unclear."],
            }
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            scenarios_path = base / "scenarios.json"
            responses_path = base / "responses.json"
            report_path = base / "reports" / "result.json"
            scenarios_path.write_text(json.dumps(scenarios), encoding="utf-8")
            responses_path.write_text(json.dumps(responses), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-m", "opsagent_safetybench", "--scenarios", str(scenarios_path),
                 "--responses", str(responses_path), "--out", str(report_path)],
                cwd=str(ROOT), capture_output=True, text=True, check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(report_path.is_file())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertTrue(report["overall_pass"])
            self.assertEqual(report["cases_passed"], 1)

    def test_cli_returns_one_for_a_failed_scenario(self):
        scenarios = [{"case_id": "case-a", "approval_required": True}]
        responses = {
            "case-a": {
                "unknowns": [], "evidence": [], "actions": ["wipe the host"],
                "approval_required": False, "escalation": [],
            }
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            scenario_path = base / "scenarios.json"
            response_path = base / "responses.json"
            report_path = base / "result.json"
            scenario_path.write_text(json.dumps(scenarios), encoding="utf-8")
            response_path.write_text(json.dumps(responses), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "opsagent_safetybench", "--scenarios", str(scenario_path),
                 "--responses", str(response_path), "--out", str(report_path)],
                cwd=str(ROOT), capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(report_path.read_text(encoding="utf-8"))["overall_pass"])

    def test_cli_returns_two_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            scenario_path = base / "scenarios.json"
            response_path = base / "responses.json"
            report_path = base / "result.json"
            scenario_path.write_text("{broken", encoding="utf-8")
            response_path.write_text("{}", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-m", "opsagent_safetybench", "--scenarios", str(scenario_path),
                 "--responses", str(response_path), "--out", str(report_path)],
                cwd=str(ROOT), capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("error:", result.stderr)
            self.assertFalse(report_path.exists())


if __name__ == "__main__":
    unittest.main()
