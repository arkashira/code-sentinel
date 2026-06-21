from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

class Severity(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

@dataclass
class Finding:
    id: str
    severity: Severity
    description: str

@dataclass
class Fix:
    id: str
    description: str
    terraform_plan_compatible: bool

class RemediationEngine:
    def __init__(self):
        self.fixes = {
            "F-1": [Fix("F-1-1", "Remove malicious code", True)],
            "F-2": [Fix("F-2-1", "Update dependencies", True)]
        }

    def get_remediation_suggestions(self, findings: List[Finding]) -> List[Fix]:
        suggestions = []
        for finding in findings:
            if finding.severity == Severity.HIGH:
                if finding.id in self.fixes:
                    suggestions.extend(self.fixes[finding.id])
        return suggestions

    def validate_fix(self, fix: Fix) -> bool:
        return fix.terraform_plan_compatible
