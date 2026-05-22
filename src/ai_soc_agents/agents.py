from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime

from .bus import MessageBus
from .models import AttackChain, ManagedAlert, ParsedEvent, RawLog, ResponsePlan, ThreatAlert


LOG_PATTERN = re.compile(
    r"(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<message>.+?) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)


class AgentLogger:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write(self, agent: str, message: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{now}] [{agent}] {message}"
        self.lines.append(line)
        print(line)


class LogParserAgent:
    def __init__(self, bus: MessageBus, logger: AgentLogger) -> None:
        self.bus = bus
        self.logger = logger
        bus.subscribe("raw_log", self.handle)

    def handle(self, raw_log: RawLog) -> None:
        match = LOG_PATTERN.search(raw_log.line)
        if not match:
            self.logger.write("ParserAgent", f"跳过无法解析日志: {raw_log.line}")
            return

        message = match.group("message").lower()
        status = "failed" if "failed" in message else "success"
        event_type = "login" if "login" in message else "unknown"
        event = ParsedEvent(
            timestamp=datetime.strptime(match.group("time"), "%Y-%m-%d %H:%M:%S"),
            source_ip=match.group("ip"),
            event_type=event_type,
            status=status,
            raw=raw_log.line,
        )
        self.logger.write("ParserAgent", f"解析日志: {raw_log.line}")
        self.bus.publish("parsed_event", event)


class ThreatDetectionAgent:
    def __init__(self, bus: MessageBus, logger: AgentLogger, brute_force_threshold: int = 6) -> None:
        self.bus = bus
        self.logger = logger
        self.brute_force_threshold = brute_force_threshold
        self.failed_logins: dict[str, int] = defaultdict(int)
        bus.subscribe("parsed_event", self.handle)

    def handle(self, event: ParsedEvent) -> None:
        if event.event_type != "login" or event.status != "failed":
            return

        self.failed_logins[event.source_ip] += 1
        attempts = self.failed_logins[event.source_ip]
        self.logger.write("DetectorAgent", f"更新状态: IP {event.source_ip} 失败次数 = {attempts}")

        if attempts == self.brute_force_threshold:
            alert = ThreatAlert(
                timestamp=event.timestamp,
                alert_type="BruteForce",
                source_ip=event.source_ip,
                severity="HIGH",
                evidence={"failed_login_count": attempts, "sample": event.raw},
            )
            self.logger.write("DetectorAgent", f"触发告警: BruteForce 来自 {event.source_ip}")
            self.bus.publish("threat_alert", alert)


class AttackChainAgent:
    def __init__(self, bus: MessageBus, logger: AgentLogger) -> None:
        self.bus = bus
        self.logger = logger
        self.alerts_by_ip: dict[str, list[ThreatAlert]] = defaultdict(list)
        bus.subscribe("threat_alert", self.handle)

    def handle(self, alert: ThreatAlert) -> None:
        self.alerts_by_ip[alert.source_ip].append(alert)
        chain = AttackChain(
            timestamp=alert.timestamp,
            source_ip=alert.source_ip,
            stage="Credential Access",
            technique="Brute Force",
            alerts=self.alerts_by_ip[alert.source_ip],
        )
        self.logger.write(
            "ChainAgent",
            f"构建攻击链: stage={chain.stage}, technique={chain.technique}, ip={chain.source_ip}",
        )
        self.bus.publish("attack_chain", chain)


class ResponseAgent:
    def __init__(self, bus: MessageBus, logger: AgentLogger) -> None:
        self.bus = bus
        self.logger = logger
        bus.subscribe("attack_chain", self.handle)

    def handle(self, chain: AttackChain) -> None:
        actions = [
            f"封禁 IP: {chain.source_ip}",
            "启用多因素认证 MFA",
            "检查登录日志和系统日志",
            "复核近期权限变更与异常会话",
        ]
        plan = ResponsePlan(
            timestamp=chain.timestamp,
            source_ip=chain.source_ip,
            alert_type="BruteForce",
            risk_level="HIGH",
            actions=actions,
            summary=f"检测到 {chain.source_ip} 触发暴力破解攻击链，建议立即阻断并审计。",
        )
        self.logger.write("ResponseAgent", "生成响应建议: block_ip, enable_mfa, audit_logs")
        self.bus.publish("response_plan", plan)


class AlertManager:
    def __init__(self, bus: MessageBus, logger: AgentLogger) -> None:
        self.logger = logger
        self.alerts: list[ManagedAlert] = []
        bus.subscribe("response_plan", self.handle)

    def handle(self, plan: ResponsePlan) -> None:
        alert = ManagedAlert(
            timestamp=plan.timestamp,
            alert_type=plan.alert_type,
            source_ip=plan.source_ip,
            risk_level=plan.risk_level,
            status="已处理",
            response_actions=plan.actions,
        )
        self.alerts.append(alert)
        self.logger.write("AlertManager", f"告警已处理: {alert.alert_type} {alert.source_ip} {alert.risk_level}")
