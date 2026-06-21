import pytest
from src.remediation_engine import RemediationEngine, Severity, Finding, Fix

def test_get_remediation_suggestions():
    engine = RemediationEngine()
    findings = [Finding("F-1", Severity.HIGH, "Detected adversarial code")]
    suggestions = engine.get_remediation_suggestions(findings)
    assert len(suggestions) == 1
    assert suggestions[0].id == "F-1-1"

def test_validate_fix():
    engine = RemediationEngine()
    fix = Fix("F-1-1", "Remove malicious code", True)
    assert engine.validate_fix(fix) == True

def test_get_remediation_suggestions_empty_findings():
    engine = RemediationEngine()
    findings = []
    suggestions = engine.get_remediation_suggestions(findings)
    assert len(suggestions) == 0

def test_get_remediation_suggestions_multiple_findings():
    engine = RemediationEngine()
    findings = [Finding("F-1", Severity.HIGH, "Detected adversarial code"), Finding("F-2", Severity.MEDIUM, "Potential security vulnerability")]
    suggestions = engine.get_remediation_suggestions(findings)
    assert len(suggestions) == 1
    assert suggestions[0].id == "F-1-1"
