import json
import os
import tempfile
import pytest
from code_sentinel import (
    load_config,
    scan_code,
    format_comment,
    determine_status,
    Issue,
)

def test_load_config_happy(tmp_path):
    cfg_path = tmp_path / "cfg.yml"
    cfg_path.write_text("max_line_length: 80\nforbid_print: true\n")
    cfg = load_config(str(cfg_path))
    assert cfg["max_line_length"] == 80
    assert cfg["forbid_print"] is True

def test_load_config_missing():
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent.yml")

def test_scan_code_happy():
    code = "a = 1\nprint('hi')\n" + "x = 2\n"
    cfg = {"max_line_length": 10, "forbid_print": True}
    issues = scan_code(code, cfg)
    # line 2 contains print -> critical, line 1 length ok, line 3 ok
    assert any(i.severity == "critical" and i.line == 2 for i in issues)
    assert len(issues) == 2  # corrected to 2

def test_scan_code_edge_cases():
    # Empty code should yield no issues regardless of config
    issues = scan_code("", {"max_line_length": 5, "forbid_print": True})
    assert issues == []

def test_format_comment_no_issues():
    comment = format_comment([])
    assert "No issues found" in comment
    assert comment.startswith("✅")

def test_format_comment_with_issues():
    issues = [
        Issue(line=1, message="Too long", severity="warning"),
        Issue(line=2, message="Print forbidden", severity="critical"),
    ]
    comment = format_comment(issues)
    assert "code-sentinel scan results" in comment
    assert "ℹ️" not in comment  # info emoji not used
    assert "⚠️" in comment  # warning emoji used
    assert "❌" in comment  # critical emoji used
