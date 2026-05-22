from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class RawLog:
    line: str


@dataclass(slots=True)
class ParsedEvent:
    timestamp: datetime
    source_ip: str
    event_type: str
    status: str
    raw: str


@dataclass(slots=True)
class ThreatAlert:
    timestamp: datetime
    alert_type: str
    source_ip: str
    severity: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AttackChain:
    timestamp: datetime
    source_ip: str
    stage: str
    technique: str
    alerts: list[ThreatAlert]


@dataclass(slots=True)
class ResponsePlan:
    timestamp: datetime
    source_ip: str
    alert_type: str
    risk_level: str
    actions: list[str]
    summary: str


@dataclass(slots=True)
class ManagedAlert:
    timestamp: datetime
    alert_type: str
    source_ip: str
    risk_level: str
    status: str
    response_actions: list[str]
