import json
from dataclasses import dataclass
from typing import List

@dataclass
class Diagnostic:
    line: int
    risk: str
    remediation: str

class CodeSentinel:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.diagnostics = []

    def scan(self) -> List[Diagnostic]:
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if 'suspicious' in line:
                        self.diagnostics.append(Diagnostic(i + 1, 'High', 'Refactor the code'))
                return self.diagnostics
        except FileNotFoundError:
            return []

    def register_diagnostic_provider(self):
        # Register the diagnostic provider
        pass

    def disable_extension(self):
        # Disable the extension
        pass

    def enable_extension(self):
        # Enable the extension
        pass
