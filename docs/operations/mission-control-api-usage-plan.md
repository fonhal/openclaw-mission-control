# Mission Control API 使用方案

## 目标

将 Mission Control 的日常管理从“主要依赖 UI 操作”切换为“以 API 与脚本为主、UI 为辅”的工作方式，提升稳定性、可重复性、可审计性与批量治理能力。

## 结构原则

采用 **skill 管方法，repo 管执行** 的结构。

### 1. skill 层（方法与边界）

位置：
- `~/.openclaw/skills/mission-control-api/`

职责：
- 说明 API-first 的工作原则
- 说明 user token 与 agent token 边界
- 提供路由矩阵、API map、chat/memory 诊断方法
- 记录已验证操作与常见失败模式

skill 层不承担项目专用脚本的长期存放职责。

### 2. repo 层（执行与沉淀）

位置：
- `/Users/vonpeter/codespace/ai-workspace/openclaw-mission-control/scripts/`

职责：
- 存放真实执行 Mission Control API 的脚本
- 存放 token 解析、统一入口、巡检与批量治理工具
- 随项目 API、数据模型、board/task 结构一起演进

## 权限分层

### 优先使用 user token 的路由

适用于：
- boards
- board tasks
- agents 列表/创建
- organization custom fields
- activity
- board memory / board chat

默认优先选择 user-side API 进行：
- board / task 管理
- 批量更新
- 巡检诊断
- board chat 注入

### 谨慎使用 agent token 的路由

路由前缀：
- `/api/v1/agent/*`

特点：
- 通常要求 agent token
- 部分还要求更高 actor，例如：`any_agent` / `board_lead` / `agent_main`

规则：
1. 不是必须，不走 `/api/v1/agent/*`
2. 若必须使用，先确认 token 类型
3. 再确认路由要求的 actor 级别
4. 最后再调用

## 日常工作流

### 工作流 A：问题巡检 / 定位

适用场景：
- board 一直重复回复
- task 没推进
- activity 噪音过多
- 无法判断当前执行 lane

标准顺序：
1. 获取 `board_id`
2. 查看 board tasks
3. 查看 `activity`
4. 查看 `task-comments`
5. 需要时查看 `board memory`
6. 判断属于：
   - workflow/control 问题
   - 数据状态问题
   - 权限问题
   - 真正的 UI 问题

优先工具：
- `scripts/inspect-mission-control-board.py`
- 后续统一入口：`scripts/mcctl.py inspect`

### 工作流 B：board / task 变更

适用场景：
- 批量创建任务
- 更新描述、优先级、依赖
- 绑定 custom fields
- 修改任务治理属性

标准顺序：
1. 确认目标 board/task
2. 默认走 user token API
3. 用脚本执行，而不是手工点 UI
4. 变更后 readback 校验
5. 必要时 git 备份

优先工具：
- `scripts/setup-mission-control-board.py`
- `scripts/update-mission-control-board-tasks.py`
- 后续统一入口：`scripts/mcctl.py`

### 工作流 C：board chat / 控制信息注入

适用场景：
- 给 board 注入人类指令
- 给 board 发 chat message
- 触发 board agents 对某条信息做后续响应

推荐路径：
- `POST /api/v1/boards/{boardId}/memory`
- `tags=["chat"]`

规则：
- 默认使用 board memory chat 路线
- 不直接把 `/api/v1/agent/gateway/.../lead/message` 当成常规发送手段

优先工具：
- `scripts/post-board-chat-memory.py`
- 后续统一入口：`scripts/mcctl.py chat`

## token 与环境约定

### 默认 token 来源

按以下顺序解析：
1. `MC_TOKEN`
2. 环境变量 `MC_TOKEN`
3. `~/.openclaw/secrets/mission-control-token`

推荐持久化方式：
- 创建文件：`~/.openclaw/secrets/mission-control-token`
- 文件内容一行：`Bearer <token>`

### 默认 base url

默认：
- `MC_BASE_URL=http://localhost:8000`

如 backend 不在本地默认端口，再按需覆盖。

## 已验证脚本

当前已验证脚本：
- `scripts/_mc_token.py`
- `scripts/setup-mission-control-board.py`
- `scripts/update-mission-control-board-tasks.py`
- `scripts/post-board-chat-memory.py`
- `scripts/inspect-mission-control-board.py`

## 推荐演进方向

后续统一收口到：
- `scripts/mcctl.py`

建议的子命令：
- `inspect`
- `chat`
- `setup-board`
- `update-tasks`
- `list-activity`
- `list-tasks`
- `patch-task`

## 操作准则

1. 管理动作优先 API / 脚本，不优先 UI 自动化
2. UI 主要用于结果查看与少量交互验证
3. `/api/v1/agent/*` 默认不作为主控制路径
4. 先查 activity / task-comments / memory，再判断是不是 UI 问题
5. 可重复动作应尽快沉淀为 repo 脚本

## 后续职责建议

Mission Control API-first 管理可作为主工作流之一，默认职责包括：
- board / task / activity / memory 的 API-first 管理
- board 结构初始化与批量治理
- task/custom field 批量更新
- board chat 注入
- activity 与 task-comment 巡检诊断
- 通用管理脚本沉淀与维护

对于更高权限的 `/api/v1/agent/*` 路由，默认按受控高级能力处理，不纳入日常默认路径。
