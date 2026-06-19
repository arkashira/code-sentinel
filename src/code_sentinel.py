import ast
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

@dataclass
class DetectionResult:
    """Holds the result of a code scan."""
    is_adversarial: bool
    score: float
    reasons: List[str] = field(default_factory=list)

class CodeSentinel:
    """ Adversarial Code Detection Engine.
    Uses static analysis (AST) and heuristics to identify potentially malicious code.
    """
    def __init__(self, threshold: float = 50.0, entropy_limit: float = 3.5):
        self.threshold = threshold
        self.entropy_limit = entropy_limit

    def _calculate_shannon_entropy(self, data: str) -> float:
        """Calculates the Shannon entropy of a string."""
        if not data:
            return 0.0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += -p_x * math.log(p_x, 2)
        return entropy

    def _check_string_entropy(self, string_val: str) -> bool:
        """Returns True if string entropy exceeds the limit (potential obfuscation)."""
        return self._calculate_shannon_entropy(string_val) > self.entropy_limit

    def _analyze_node(self, node: ast.AST) -> Tuple[float, List[str]]:
        """ Recursively analyzes an AST node to generate a risk score.
        Returns (score, list_of_reasons).
        """
        score = 0.0
        reasons = []
        # Check for dangerous function calls
        if isinstance(node, ast.Call):
            func_name = ""
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            # High-risk calls
            if func_name in ("eval", "exec", "compile"):
                score += 100
                reasons.append(f"Dangerous function call: {func_name}")
            elif func_name == "__import__":
                score += 50
                reasons.append("Dynamic import detected: __import__")
            elif func_name in ("system", "popen"):
                # Check if it's os.system or subprocess.popen
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id in ("os", "subprocess"):
                        score += 100
                        reasons.append(f"Shell execution call: {node.func.value.id}.{func_name}")
        # Check for high entropy strings (potential payloads/obfuscation)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if self._check_string_entropy(node.value):
                score += 25
                reasons.append("High entropy string detected (potential obfuscation)")
        # Recurse into children
        for child in ast.iter_child_nodes(node):
            child_score, child_reasons = self._analyze_node(child)
            score += child_score
            reasons.extend(child_reasons)
        return score, reasons

    def scan(self, code: str) -> DetectionResult:
        """ Scans a snippet of Python code. Returns a DetectionResult object.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            # If code is invalid Python, we treat it as benign or error depending on policy.
            # Here we treat it as benign to avoid FPs on broken snippets,
            # but in a real system, this might be flagged.
            return DetectionResult(is_adversarial=False, score=0.0, reasons=["Syntax Error"])
        score, reasons = self._analyze_node(tree)
        is_adversarial = score >= self.threshold
        # Deduplicate reasons
        unique_reasons = list(dict.fromkeys(reasons))
        return DetectionResult(
            is_adversarial=is_adversarial,
            score=score,
            reasons=unique_reasons
        )

    def evaluate(self, dataset: List[Tuple[str, bool]]) -> Dict[str, float]:
        """ Evaluates the detector against a dataset of (code, is_adversarial_label).
        Returns metrics: accuracy, false_positive_rate.
        """
        if not dataset:
            return {"accuracy": 0.0, "false_positive_rate": 0.0}
        correct_predictions = 0
        false_positives = 0
        total_benign = 0
        for code, actual_is_adversarial in dataset:
            result = self.scan(code)
            predicted_is_adversarial = result.is_adversarial
            if predicted_is_adversarial == actual_is_adversarial:
                correct_predictions += 1
            if not actual_is_adversarial:
                total_benign += 1
                if predicted_is_adversarial:
                    false_positives += 1
        accuracy = correct_predictions / len(dataset)
        fpr = 0.0
        if total_benign > 0:
            fpr = false_positives / total_benign
        return {
            "accuracy": accuracy,
            "false_positive_rate": fpr
        }
