from code_sentinel import CodeSentinel, Incident, PR
from datetime import datetime
import pytest

def test_add_incident():
    sentinel = CodeSentinel()
    incident = Incident(1, "type1", "severity1", datetime.now())
    sentinel.add_incident(incident)
    assert len(sentinel.incidents) == 1

def test_add_pr():
    sentinel = CodeSentinel()
    pr = PR(1, "title1", ["finding1"])
    sentinel.add_pr(pr)
    assert len(sentinel.prs) == 1

def test_get_dashboard_data():
    sentinel = CodeSentinel()
    incident1 = Incident(1, "type1", "severity1", datetime.now())
    incident2 = Incident(2, "type1", "severity2", datetime.now())
    sentinel.add_incident(incident1)
    sentinel.add_incident(incident2)
    pr1 = PR(1, "title1", ["finding1"])
    pr2 = PR(2, "title2", ["finding2"])
    sentinel.add_pr(pr1)
    sentinel.add_pr(pr2)
    data = sentinel.get_dashboard_data()
    assert data["blocked_incidents"] == 2
    assert data["incident_types"] == {"type1": 2}
    assert data["incident_severity"] == {"severity1": 1, "severity2": 1}
    assert len(data["recent_prs"]) == 2

def test_get_dashboard_data_empty():
    sentinel = CodeSentinel()
    data = sentinel.get_dashboard_data()
    assert data["blocked_incidents"] == 0
    assert data["incident_types"] == {}
    assert data["incident_severity"] == {}
    assert data["recent_prs"] == []
