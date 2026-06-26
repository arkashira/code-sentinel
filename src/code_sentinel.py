import json
import os
import sys
import yaml
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Issue:
    line: int
    message: str
    severity: str  # "info", "warning", "critical"

def load_config(path: str) -> Dict[str, Any]:
    """ Load a YAML configuration file.
    The config may contain:
    - max_line_length: int
    - forbid_print: bool
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("Config must be a mapping")
    return data

def scan_code(code: str, config: Dict[str, Any]) -> List[Issue]:
    """ Very small static analysis:
    - If a line exceeds max_line_length -> warning.
    - If forbid_print is true and a line contains 'print(' -> critical.
    Returns a list of Issue objects.
    """
    issues: List[Issue] = []
    max_len = config.get("max_line_length", 120)
    forbid_print = config.get("forbid_print", False)
    for idx, line in enumerate(code.splitlines(), start=1):
        if len(line) > max_len:
            issues.append(
                Issue(
                    line=idx,
                    message=f"Line exceeds {max_len} characters",
                    severity="warning",
                )
            )
        if forbid_print and "print(" in line:
            issues.append(
                Issue(
                    line=idx,
                    message="Usage of print() is forbidden",
                    severity="critical",
                )
            )
    return issues

def format_comment(issues: List[Issue]) -> str:
    """ Produce a markdown comment summarising the issues.
    """
    if not issues:
        return "✅ No issues found by code-sentinel."
    lines = ["## code-sentinel scan results", ""]
    for issue in issues:
        emoji = {"info": "ℹ️", "warning": "⚠️", "critical": "❌"}.get(issue.severity, "")
        lines.append(
            f"- {emoji} **Line {issue.line}**: {issue.message} ({issue.severity})"
        )
    return "\n".join(lines)

def determine_status(issues: List[Issue]) -> str:
    """ Return 'success' if no critical issues, otherwise 'failure'.
    """
    has_critical = any(issue.severity == "critical" for issue in issues)
    return "failure" if has_critical else "success"

def main() -> None:
    """ Entry point used by the GitHub Action.
    Expected environment variables:
    - CONFIG_PATH: path to the YAML config file.
    - CODE_PATH: path to the source file to scan.
    The function prints the comment to stdout and exits with code 1 on failure.
    """
    config_path = os.getenv("CONFIG_PATH", "code_sentinel.yml")
    code_path = os.getenv("CODE_PATH", "")
    config = load_config(config_path)
    if not code_path or not os.path.isfile(code_path):
        print("No code file provided or file does not exist.", file=sys.stderr)
        sys.exit(2)
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()
    issues = scan_code(code, config)
    comment = format_comment(issues)
    status = determine_status(issues)
    # In a real action we would use the GitHub API; here we just output.
    print(comment)
    print(f"::set-output name=status::{status}")
    if status == "failure":
        sys.exit(1)

if __name__ == "__main__":
    main()
