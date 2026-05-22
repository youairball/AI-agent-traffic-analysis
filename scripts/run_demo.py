from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_soc_agents.workflow import run_workflow


def main() -> None:
    result = run_workflow()
    alerts = result["alerts"]

    print("\n=== 告警响应 ===")
    for alert in alerts:
        print(f"告警类型: {alert['alert_type']}")
        print(f"风险等级: {alert['risk_level']}")
        print(f"攻击 IP: {alert['source_ip']}")
        print("处置建议:")
        for index, action in enumerate(alert["response_actions"], start=1):
            print(f"  {index}. {action}")


if __name__ == "__main__":
    main()
