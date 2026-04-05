# Mission Control Agent 启动必备检查

## 适用范围

适用于所有接手 OpenClaw Mission Control 项目任务的 agents。

## 默认项目工作目录

本项目默认工作输出目录统一为：
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control`

规则：
- 与 Mission Control 项目相关的文档、脚本、方案、报告、变更说明，默认优先在该目录内组织与落地
- 除非用户明确指定其它位置，否则不要把该项目产物散落到各 agent 自己的 workspace 根目录或其它无关目录

## 启动必备检查（强制）

任何 agent 在以下场景进入 Mission Control 项目前，必须先完成本检查：
- 新接手该项目任务
- 新 session 恢复后继续该项目任务
- 从其它 agent 交接到该项目任务
- 需要对 board / task / 文档 / API / UI / 运维做实际操作前

## 最小必读集合

所有 agents 至少先阅读：
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/project-working-agreement.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/guide/overview.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/operations/mission-control-api-usage-plan.md`

## 按角色补充阅读

### Lead / PM / 调度
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/board-leader-principles.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/product/page-map.md`

### Product / Scope / UX
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/product/mission.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/product/information-architecture.md`

### Architect / Design
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/architecture/system-overview.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/architecture/mission-control-role-model-and-operating-setup.md`

### Builder / Implementation
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/development/README.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/reference/api.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/reference/data-models.md`

### Verifier / Operations
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/operations/smoke-test.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/operations/release-checklist.md`
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/docs/troubleshooting/README.md`

## 工作方式要求

1. 管理动作优先 API / 脚本，不优先 UI 自动化
2. board / task / activity / memory 相关操作，优先参考 `mission-control-api-usage-plan.md`
3. 先判断当前 active lane、依赖和 board 状态，再推进任务
4. 不在未明确激活 lane 时自行拉起下游任务
5. 重大推进、lane 切换、优先级变更，应先写入 board chat / memory 或对应任务上下文

## 自检清单

开始执行前，至少确认以下问题：
- 我是否在正确的项目目录下工作？
- 我是否已读本项目的最小必读文档？
- 我是否知道当前 board / task / active lane 是什么？
- 我是否知道这次操作优先走 API、脚本还是代码变更？
- 我的输出是否会落在本项目目录里，而不是散落到其它地方？

若以上任一问题答案是否定的，应先补齐检查，再开始执行。
