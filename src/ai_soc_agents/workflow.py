from __future__ import annotations

from dataclasses import asdict

from .agents import AlertManager, AgentLogger, AttackChainAgent, LogParserAgent, ResponseAgent, ThreatDetectionAgent
from .bus import MessageBus
from .models import RawLog


SAMPLE_LOGS = [
    "2025-05-25 10:15:24 Failed login from 192.168.1.10",
    "2025-05-25 10:15:24 Failed login from 192.168.1.10",
    "2025-05-25 10:15:24 Failed login from 192.168.1.10",
    "2025-05-25 10:15:25 Failed login from 192.168.1.10",
    "2025-05-25 10:15:25 Failed login from 192.168.1.10",
    "2025-05-25 10:15:25 Failed login from 192.168.1.10",
]


def run_workflow(logs: list[str] | None = None) -> dict[str, object]:
    bus = MessageBus()
    logger = AgentLogger()
    alert_manager = AlertManager(bus, logger)

    LogParserAgent(bus, logger)
    ThreatDetectionAgent(bus, logger)
    AttackChainAgent(bus, logger)
    ResponseAgent(bus, logger)

    for line in logs or SAMPLE_LOGS:
        bus.publish("raw_log", RawLog(line=line))

    return {
        "logs": logger.lines,
        "alerts": [asdict(alert) for alert in alert_manager.alerts],
        "workflow": [
            {"id": "start", "label": "START", "type": "system"},
            {"id": "parser", "label": "LogParserAgent", "type": "agent"},
            {"id": "detector", "label": "ThreatDetectionAgent", "type": "agent"},
            {"id": "chain", "label": "AttackChainAgent", "type": "agent"},
            {"id": "response", "label": "ResponseAgent", "type": "agent"},
            {"id": "alert", "label": "AlertManager", "type": "agent"},
            {"id": "end", "label": "END", "type": "system"},
        ],
    }
