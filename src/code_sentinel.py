from dataclasses import dataclass
from typing import List

@dataclass
class Finding:
    explanation: str
    suggestion: str
    kb_link: str

class CodeSentinel:
    def __init__(self, findings=None):
        self.findings = findings if findings else []

    def get_findings(self, *args, **kwargs) -> List[Finding]:
        if args or kwargs:
            raise TypeError("get_findings() takes no arguments")
        return self.findings
