from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Incident:
    id: int
    type: str
    severity: str
    timestamp: datetime

@dataclass
class PR:
    id: int
    title: str
    findings: List[str]

class CodeSentinel:
    def __init__(self):
        self.incidents = []
        self.prs = []

    def add_incident(self, incident: Incident):
        self.incidents.append(incident)

    def add_pr(self, pr: PR):
        self.prs.append(pr)

    def get_dashboard_data(self):
        blocked_incidents = len(self.incidents)
        incident_types = {}
        incident_severity = {}
        for incident in self.incidents:
            if incident.type not in incident_types:
                incident_types[incident.type] = 1
            else:
                incident_types[incident.type] += 1
            if incident.severity not in incident_severity:
                incident_severity[incident.severity] = 1
            else:
                incident_severity[incident.severity] += 1
        recent_prs = self.prs[-5:]  # show last 5 PRs
        return {
            "blocked_incidents": blocked_incidents,
            "incident_types": incident_types,
            "incident_severity": incident_severity,
            "recent_prs": recent_prs,
        }
