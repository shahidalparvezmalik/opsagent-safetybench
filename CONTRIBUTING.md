# Contributing

Contributions should keep the project synthetic, deterministic, and reviewable.

- Do not add live-system connectors, automated remediation, or production credentials.
- Do not include real incident data, personal information, or internal infrastructure details.
- Add a paired safe/unsafe fixture when changing a rubric or evaluator behavior.
- Keep phrase checks narrow; document known false-positive and false-negative risks.
- Run `python3 -m unittest discover -s tests -v` and both bundled CLI controls.
- Describe scenario changes and their rationale in the pull request.

A passing test suite checks the code paths covered by tests. It does not independently validate scenario quality or safety claims.
