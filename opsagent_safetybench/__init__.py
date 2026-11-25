"""OpsAgent SafetyBench: evaluate synthetic IT-operations response text."""

from .evaluator import EvaluationInputError, evaluate

__all__ = ["EvaluationInputError", "evaluate"]
__version__ = "0.1.0"
