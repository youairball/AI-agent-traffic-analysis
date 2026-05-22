from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_soc_agents.workflow import SAMPLE_LOGS, run_workflow


class WorkflowTest(TestCase):
    def test_brute_force_alert_is_generated(self) -> None:
        result = run_workflow(SAMPLE_LOGS)

        self.assertEqual(len(result["alerts"]), 1)
        alert = result["alerts"][0]
        self.assertEqual(alert["alert_type"], "BruteForce")
        self.assertEqual(alert["source_ip"], "192.168.1.10")
        self.assertEqual(alert["risk_level"], "HIGH")
        self.assertIn("启用多因素认证 MFA", alert["response_actions"])

    def test_alert_requires_context_threshold(self) -> None:
        result = run_workflow(SAMPLE_LOGS[:5])

        self.assertEqual(result["alerts"], [])
