# AI Agent SOC: Traffic Analysis and Incident Response

一个面向安全运营场景的多 Agent AI 驱动项目，用于演示从原始日志输入、威胁检测、攻击链还原到响应建议生成的自动化闭环。

项目重点展示：

- 多 Agent 协同工作流
- 安全日志结构化解析
- 基于上下文状态的威胁检测
- 攻击链自动关联
- AI/规则混合响应建议生成
- 终端运行日志与可视化工作流证明

## 项目亮点

传统安全运营经常遇到日志量大、格式不统一、告警误报多、攻击路径碎片化和响应依赖人工的问题。本项目将 SOC 分析流程拆分为多个独立 Agent，并通过消息总线解耦协作。

工作流如下：

```text
Raw Logs
  -> LogParserAgent
  -> ThreatDetectionAgent
  -> AttackChainAgent
  -> ResponseAgent
  -> AlertManager
```

## Agent 设计

| Agent | 职责 |
| --- | --- |
| LogParserAgent | 解析原始安全日志，提取 IP、时间、状态、事件类型等字段 |
| ThreatDetectionAgent | 结合规则和上下文状态累计识别威胁行为，例如暴力破解 |
| AttackChainAgent | 将多个告警按照时间序列和行为上下文关联为攻击链 |
| ResponseAgent | 根据攻击类型生成处置建议，例如封禁 IP、启用 MFA、审计日志 |
| AlertManager | 统一管理告警输出、状态记录和可视化数据 |

## 快速运行

要求：Python 3.10+

```bash
python scripts/run_demo.py
```

运行测试：

```bash
python -m unittest discover -s tests
```

生成可视化数据：

```bash
python scripts/export_dashboard_data.py
```

然后打开：

```text
docs/index.html
```

## 示例输出

```text
[ParserAgent] 解析日志: Failed login from 192.168.1.10
[DetectorAgent] 更新状态: IP 192.168.1.10 失败次数 = 6
[DetectorAgent] 触发告警: BruteForce 来自 192.168.1.10
[ChainAgent] 构建攻击链: Credential Access -> Brute Force
[ResponseAgent] 生成响应建议: block_ip, enable_mfa, audit_logs
```

## 使用证明

可提交材料包括：

- 过去 30 天 OpenAI / Google AI Studio / Anthropic 账单截图
- 本项目终端运行日志截图
- `docs/index.html` Agent 工作流可视化截图
- GitHub 项目链接

当前可配合提交的账单证明：

- OpenAI: 56.21 USD
- Google AI Studio: 18.36 USD
- Anthropic Claude: 32.41 USD

## 目录结构

```text
.
├── application_answer_04.md
├── docs/
│   ├── dashboard-data.json
│   └── index.html
├── scripts/
│   ├── export_dashboard_data.py
│   └── run_demo.py
├── src/
│   └── ai_soc_agents/
│       ├── agents.py
│       ├── bus.py
│       ├── models.py
│       └── workflow.py
└── tests/
    └── test_workflow.py
```

## 后续规划

- 接入 MiMo API，用于复杂攻击路径解释与响应策略生成
- 扩展 Web 流量异常检测 Agent
- 增加 MITRE ATT&CK 技术映射
- 增加真实 SIEM / EDR 数据源适配器
- 增加人工审批与自动执行策略分级
