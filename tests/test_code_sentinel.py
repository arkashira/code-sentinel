import pytest
from src.code_sentinel import CodeSentinel, Finding

def test_get_findings():
    sentinel = CodeSentinel()
    findings = sentinel.get_findings()
    assert len(findings) == 0

def test_get_findings_empty():
    sentinel = CodeSentinel()
    findings = sentinel.get_findings()
    assert len(findings) == 0

def test_get_findings_invalid_input():
    sentinel = CodeSentinel()
    with pytest.raises(TypeError):
        sentinel.get_findings("invalid_input")

def test_get_findings_with_findings():
    findings = [
        Finding(explanation="Dependency Confusion Attack detected", suggestion="Remove unused dependencies", kb_link="KB-204: Dependency Confusion Fix"),
        Finding(explanation="SQL Injection Attack detected", suggestion="Use parameterized queries", kb_link="KB-205: SQL Injection Fix")
    ]
    sentinel = CodeSentinel(findings)
    retrieved_findings = sentinel.get_findings()
    assert len(retrieved_findings) == 2
    assert retrieved_findings[0].explanation == "Dependency Confusion Attack detected"
    assert retrieved_findings[1].suggestion == "Use parameterized queries"
