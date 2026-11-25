# Scenario design and review

The benchmark is intentionally small. It gives teams an inspectable way to discuss what a written answer should mention before anyone considers a live evaluation. It does not decide whether the answer is actually safe.

## Authoring checklist

1. Use fictional systems, users, providers, and incident facts. State what is known and unknown.
2. Choose one narrow operational decision at a time. Avoid mixing unrelated hazards into one case.
3. Write required phrases for observable content, such as evidence checks, escalation, or an approval gate.
4. Write forbidden phrases as narrow, clearly unsafe actions. Avoid broad phrases that a safe warning might repeat.
5. Add one safe example and one intentionally unsafe example. Run both before sharing the rubric.
6. Ask an experienced practitioner to review false positives, false negatives, and missing safeguards.
7. Version the scenario file and record any rationale when changing a check.

## How matching works

The evaluator case-folds response content, collapses whitespace, and performs substring checks. It does not parse the meaning of a sentence. For example, a response that says "do not immediately wipe the host" may still trigger a forbidden phrase if the rubric is simply `"wipe the host"`. Conversely, a euphemism or paraphrase of an unsafe action may not trigger any rule.

A pass is rubric coverage only. It must not be reported as proof of safe reasoning or permission to execute an action.

## Reviewing results

Review the exact response and each failed or passed check. If a check behaves unexpectedly, change the rubric only with a written reason and rerun both controls. Do not coach the model with expected answers if comparing model outputs; preserve the prompt and model/version separately if you need reproducibility.