"""Command-line entry point for OpsAgent SafetyBench."""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .evaluator import EvaluationInputError, evaluate


def _read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="opsagent-safetybench",
        description="Evaluate supplied text responses against synthetic IT-operations scenarios.",
    )
    parser.add_argument("--scenarios", required=True, type=Path, help="JSON array of scenario objects")
    parser.add_argument("--responses", required=True, type=Path, help="JSON object keyed by case_id")
    parser.add_argument("--out", required=True, type=Path, help="Path for the JSON evaluation report")
    args = parser.parse_args(argv)

    try:
        report = evaluate(_read_json(args.scenarios), _read_json(args.responses))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, EvaluationInputError) as exc:
        print("error: {}".format(exc), file=sys.stderr)
        return 2

    print("{}/{} cases passed; overall_pass={}".format(
        report["cases_passed"], report["cases_total"], report["overall_pass"]
    ))
    print("Report: {}".format(args.out))
    return 0 if report["overall_pass"] else 1