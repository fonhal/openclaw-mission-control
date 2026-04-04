#!/usr/bin/env python3
import json
import os
from textwrap import dedent

import requests

BASE_URL = os.environ.get('MC_BASE_URL', 'http://localhost:8000').rstrip('/')
TOKEN = os.environ.get('MC_TOKEN')
BOARD_ID = '4201eeb0-4a3c-429b-ad56-88cdf7367b3a'

TASKS = {
    'ITER-001 Phase 1 scope freeze and acceptance baseline': {
        'task_type': 'planning', 'priority': 'P0', 'depends_on': [],
        'description': dedent('''
        【任务类型】规划 / 收口
        【优先级】P0

        【背景 / 目标】
        将本轮 phase 1 从“方向明确”收口到“范围、非范围、成功标准、任务边界可执行”，为后续设计、实现、验证提供统一基线。

        【负责人】
        主 owner：MC Product Strategist
        协作者：MC Board Leader

        【范围】
        - 收口 phase 1 的目标、范围、非范围与成功标准
        - 明确首批任务边界与推进顺序原则
        - 形成可供 Architect / Builder / Verifier 引用的 baseline

        【输出物】
        - 一份 phase 1 scope baseline
        - 一版首批任务边界与优先级说明

        【验收标准】
        - 范围、非范围、优先级与成功标准清晰
        - 后续任务可直接引用，不再反复追问边界
        - P0 范围受控且可解释

        【风险 / blocker】
        - 边界不稳会导致后续返工
        - 优先级过散会失去短期焦点

        【回报格式】
        ✅ DONE：baseline 路径 + 完成点
        🧪 VERIFY：说明后续角色如何引用
        ⚠️ RISK/BLOCKER：边界争议或信息缺口
        ▶️ NEXT：建议启动的设计任务
        ''').strip()
    },
    'ITER-002 Task schema extension design': {
        'task_type': 'design', 'priority': 'P0', 'depends_on': ['ITER-001 Phase 1 scope freeze and acceptance baseline'],
        'description': dedent('''
        【任务类型】设计
        【优先级】P0

        【背景 / 目标】
        扩展 task schema，使任务可以承载 baseline、acceptance、run-safe 等治理信息，而不只是标题和描述。

        【负责人】
        主 owner：MC Architect
        协作者：MC Product Strategist / MC Board Leader

        【范围】
        - 设计 baseline_ref / acceptance_checklist / run_safe_status / latest_policy_check_at
        - 明确字段语义、状态值、边界与 API contract
        - 说明与现有 task model 的关系

        【输出物】
        - task schema extension 设计说明
        - 字段定义与 contract 草案

        【验收标准】
        - 字段定义、状态值、边界清晰
        - Builder 可直接据此实现 migration 与 API
        - Verifier 可据此判断完成态要求

        【风险 / blocker】
        - 字段过重影响可用性
        - 字段过轻不足以支撑治理闭环

        【回报格式】
        ✅ DONE：设计文档路径 + 字段清单
        🧪 VERIFY：说明 Builder 如何直接接手
        ⚠️ RISK/BLOCKER：兼容性或复杂度风险
        ▶️ NEXT：建议衔接后端实现
        ''').strip()
    },
    'ITER-003 Blocker and evidence model design': {
        'task_type': 'design', 'priority': 'P0', 'depends_on': ['ITER-001 Phase 1 scope freeze and acceptance baseline'],
        'description': dedent('''
        【任务类型】设计
        【优先级】P0

        【背景 / 目标】
        定义 blocker 与 evidence 的统一模型，使任务阻塞状态与交付证据可结构化管理。

        【负责人】
        主 owner：MC Architect
        协作者：MC Board Leader / MC Verifier

        【范围】
        - 设计 task_blockers / task_evidence 模型
        - 定义 blocker / evidence lifecycle
        - 明确与 task status、verification、policy 的关联

        【输出物】
        - blocker / evidence 结构设计说明
        - lifecycle 与关联关系说明

        【验收标准】
        - blocker 与 evidence 结构完整
        - 可支持 create / list / resolve
        - 与 task 主体关系明确且无语义冲突

        【风险 / blocker】
        - blocker 与状态关系不清会导致流转混乱
        - evidence 定义不清会影响验证判断

        【回报格式】
        ✅ DONE：模型说明 + 生命周期定义
        🧪 VERIFY：说明如何支持 CRUD 与 verify
        ⚠️ RISK/BLOCKER：边界不清或模型重叠
        ▶️ NEXT：建议衔接后端模型实现
        ''').strip()
    },
    'ITER-004 Board policy design and validation rules': {
        'task_type': 'design', 'priority': 'P0', 'depends_on': ['ITER-001 Phase 1 scope freeze and acceptance baseline','ITER-002 Task schema extension design','ITER-003 Blocker and evidence model design'],
        'description': dedent('''
        【任务类型】设计 / 运维治理
        【优先级】P0

        【背景 / 目标】
        定义 board policy、validation rules 与 hard block / warning 机制，使任务从“存在”升级为“合规”。

        【负责人】
        主 owner：MC Architect
        协作者：MC Operations and Governance / MC Board Leader

        【范围】
        - 设计 board_policies、policy keys、validation rules
        - 区分 hard block 与 warning
        - 定义任务各状态的合规要求

        【输出物】
        - policy 设计文档
        - validation rules / policy matrix

        【验收标准】
        - policy key、默认值、规则分层清晰
        - warning 与 block 边界明确
        - 可直接支持 validate-run-safe 与 transition guard

        【风险 / blocker】
        - 规则过严影响可用性
        - 规则过松失去治理价值
        - 与 schema / blocker 模型不一致会返工

        【回报格式】
        ✅ DONE：policy 设计路径 + matrix
        🧪 VERIFY：说明如何支持 validate / guard / settings
        ⚠️ RISK/BLOCKER：规则冲突或落地风险
        ▶️ NEXT：建议实现顺序
        ''').strip()
    },
    'ITER-005 Backend task model + migration implementation': {
        'task_type': 'implementation', 'priority': 'P0', 'depends_on': ['ITER-002 Task schema extension design'],
        'description': dedent('''
        【任务类型】实现
        【优先级】P0

        【背景 / 目标】
        将 task governance 设计落到后端模型、持久化与 API 层，确保新增治理字段可稳定读写。

        【负责人】
        主 owner：MC Builder
        协作者：MC Architect

        【范围】
        - 扩展 task model
        - 编写 migration
        - 更新 schema 与 read/write API
        - 保证新增字段可持久化并返回

        【输出物】
        - 后端 model 改动
        - migration
        - schema / API 更新
        - 基本验证结果

        【验收标准】
        - migration 可运行且不破坏现有数据
        - API 正确返回新增字段
        - 新字段可正常读写
        - 有基础验证证据

        【风险 / blocker】
        - migration 兼容性风险
        - 可能影响现有列表 / 详情接口

        【回报格式】
        ✅ DONE：改动点 + 文件路径 + migration 说明
        🧪 VERIFY：migration / API / 测试验证结果
        ⚠️ RISK/BLOCKER：兼容性风险或未覆盖边界
        ▶️ NEXT：建议衔接 blocker/evidence 或 policy engine
        ''').strip()
    },
    'ITER-006 Backend blockers/evidence CRUD': {
        'task_type': 'implementation', 'priority': 'P0', 'depends_on': ['ITER-003 Blocker and evidence model design'],
        'description': dedent('''
        【任务类型】实现
        【优先级】P0

        【背景 / 目标】
        落地 blocker/evidence 的后端模型、CRUD 与 activity logging，使阻塞与证据成为可管理对象。

        【负责人】
        主 owner：MC Builder
        协作者：MC Architect / MC Verifier

        【范围】
        - 实现 blocker/evidence model
        - 提供 CRUD API
        - 接入 activity logging
        - 支持任务完整维护阻塞与证据

        【输出物】
        - blocker/evidence 后端实现
        - CRUD API
        - activity logging 接入
        - 基本验证结果

        【验收标准】
        - create / list / resolve 正常
        - 数据结构与设计一致
        - activity 中能看到关键变更
        - API 结果可供 UI 与 verifier 使用

        【风险 / blocker】
        - activity 接入不完整会影响审计
        - 语义不一致会影响 policy / verify

        【回报格式】
        ✅ DONE：实现点 + 接口路径 + 关键文件
        🧪 VERIFY：CRUD 验证结果
        ⚠️ RISK/BLOCKER：数据一致性或审计风险
        ▶️ NEXT：建议衔接 validate-run-safe
        ''').strip()
    },
    'ITER-007 Policy engine + validate-run-safe endpoint': {
        'task_type': 'implementation', 'priority': 'P0', 'depends_on': ['ITER-004 Board policy design and validation rules','ITER-005 Backend task model + migration implementation','ITER-006 Backend blockers/evidence CRUD'],
        'description': dedent('''
        【任务类型】实现 / 运维治理
        【优先级】P0

        【背景 / 目标】
        实现 policy engine 与 validate-run-safe endpoint，用于判断任务是否达到“可推进 / 可评审 / 可完成”的最低治理标准。

        【负责人】
        主 owner：MC Builder
        协作者：MC Architect / MC Operations and Governance / MC Verifier

        【范围】
        - 实现 policy engine service
        - 提供 validate-run-safe endpoint
        - 编写基础测试
        - 返回结构化 violations / warnings

        【输出物】
        - policy engine 实现
        - validate-run-safe endpoint
        - 测试或等效验证证据
        - violation 结构说明

        【验收标准】
        - 缺 baseline / acceptance / evidence 时返回结构化 violations
        - warning 与 block 区分正确
        - endpoint 结果可供 guard 与 UI 使用
        - 核心规则路径有基本覆盖

        【风险 / blocker】
        - rule matrix 不稳会影响实现质量
        - 规则遗漏会导致校验不可靠

        【回报格式】
        ✅ DONE：核心实现 + endpoint + 测试证据
        🧪 VERIFY：violations / warnings 示例与覆盖说明
        ⚠️ RISK/BLOCKER：规则缺口、误判、覆盖不足
        ▶️ NEXT：建议接入 transition guard 与 UI
        ''').strip()
    },
    'ITER-008 Task transition guard integration': {
        'task_type': 'implementation', 'priority': 'P1', 'depends_on': ['ITER-007 Policy engine + validate-run-safe endpoint'],
        'description': dedent('''
        【任务类型】实现
        【优先级】P1

        【背景 / 目标】
        把治理规则挂到任务状态流转中，阻止不合规任务直接进入 in_progress / review / done。

        【负责人】
        主 owner：MC Builder
        协作者：MC Architect / MC Verifier

        【范围】
        - 接入 task lifecycle transition guard
        - 覆盖 in_progress / review / done 等关键流转点
        - 记录相关反馈或 activity

        【输出物】
        - transition guard 接入实现
        - 阻断与反馈逻辑
        - 基本验证结果

        【验收标准】
        - 非法流转被阻断
        - 阻断反馈可解释
        - 有记录说明为何被阻断

        【风险 / blocker】
        - guard 过严影响操作体验
        - 反馈不清会让使用者无法修正

        【回报格式】
        ✅ DONE：接入点 + 改动说明 + 验证结果
        🧪 VERIFY：非法流转被阻断的示例
        ⚠️ RISK/BLOCKER：误阻断、反馈不足、边界缺失
        ▶️ NEXT：建议衔接 dashboard / verify
        ''').strip()
    },
    'ITER-009 Task detail UI sections': {
        'task_type': 'implementation', 'priority': 'P1', 'depends_on': ['ITER-005 Backend task model + migration implementation','ITER-006 Backend blockers/evidence CRUD'],
        'description': dedent('''
        【任务类型】实现
        【优先级】P1

        【背景 / 目标】
        在 task detail 中承载 baseline / acceptance / blockers / evidence，使治理信息可被直观使用。

        【负责人】
        主 owner：MC Builder
        协作者：MC Architect / MC Verifier

        【范围】
        - 实现 baseline / acceptance / blockers / evidence 四个 section
        - 覆盖空态、缺失态、已填写态展示
        - 支撑 verifier / lead 日常使用

        【输出物】
        - task detail UI 改动
        - 四个 section 展示与交互
        - 基本验证结果

        【验收标准】
        - 空态 / 缺失 / 已填写状态正确展示
        - 字段语义与后端 contract 一致
        - UI 可支持后续治理使用

        【风险 / blocker】
        - contract 未稳定会导致返工
        - 信息过多会影响可读性

        【回报格式】
        ✅ DONE：UI 改动点 + 页面路径
        🧪 VERIFY：空态/缺失/已填状态验证结果
        ⚠️ RISK/BLOCKER：交互复杂度、信息密度或 contract 风险
        ▶️ NEXT：建议衔接 violations dashboard
        ''').strip()
    },
    'ITER-010 Board violations dashboard': {
        'task_type': 'implementation', 'priority': 'P1', 'depends_on': ['ITER-007 Policy engine + validate-run-safe endpoint'],
        'description': dedent('''
        【任务类型】实现 / 运维治理
        【优先级】P1

        【背景 / 目标】
        提供 board 级治理视图，让 Lead 与 Operator 快速识别哪些任务不合规、缺什么、哪里风险最高。

        【负责人】
        主 owner：MC Builder
        协作者：MC Board Leader / MC Operations and Governance

        【范围】
        - 实现 violations list、filter、summary
        - 支持快速查看任务风险与缺失项
        - 形成 board-level 治理视图

        【输出物】
        - violations dashboard
        - 基本筛选与汇总能力
        - 基本验证结果

        【验收标准】
        - 任务风险与缺失项一眼可见
        - 能按关键条件筛选或聚合
        - Lead / operator 可据此识别优先修复项

        【风险 / blocker】
        - violation 结构不稳定会影响 UI 收口
        - 信息组织不清会变成噪音面板

        【回报格式】
        ✅ DONE：dashboard 改动点 + 使用说明
        🧪 VERIFY：说明如何快速识别高风险任务
        ⚠️ RISK/BLOCKER：信息噪音、筛选不足、数据不稳定
        ▶️ NEXT：建议衔接 settings / verify / release 收口
        ''').strip()
    },
    'ITER-011 Board policy settings UI': {
        'task_type': 'implementation', 'priority': 'P1', 'depends_on': ['ITER-004 Board policy design and validation rules','ITER-007 Policy engine + validate-run-safe endpoint'],
        'description': dedent('''
        【任务类型】实现 / 运维治理
        【优先级】P1

        【背景 / 目标】
        在 board settings 中提供 policy enable/config UI，使治理策略可配置、可持久化、可回显。

        【负责人】
        主 owner：MC Builder
        协作者：MC Operations and Governance / MC Architect

        【范围】
        - 实现 board settings 中的 policy enable/config UI
        - 支持配置持久化与回显
        - 让 board 级治理策略可查看与调整

        【输出物】
        - board policy settings UI
        - 配置持久化与回显能力
        - 基本验证结果

        【验收标准】
        - 设置可持久化并正确回显
        - 配置语义清晰
        - lead / operator 可通过页面调整治理规则

        【风险 / blocker】
        - policy key / 默认值不稳会导致返工
        - 配置能力过多会增加误操作风险

        【回报格式】
        ✅ DONE：设置页改动点 + 配置能力说明
        🧪 VERIFY：持久化 / 回显验证结果
        ⚠️ RISK/BLOCKER：配置语义不清、误操作或 contract 不稳
        ▶️ NEXT：建议衔接 verifier / release 收口
        ''').strip()
    },
    'ITER-012 Verification matrix and regression plan': {
        'task_type': 'verification', 'priority': 'P2', 'depends_on': ['ITER-008 Task transition guard integration','ITER-009 Task detail UI sections','ITER-010 Board violations dashboard','ITER-011 Board policy settings UI'],
        'description': dedent('''
        【任务类型】验证
        【优先级】P2

        【背景 / 目标】
        形成 verification matrix 与 regression plan，确保 backend / frontend / transition / policy 的关键路径被系统覆盖。

        【负责人】
        主 owner：MC Verifier
        协作者：MC Builder / MC Board Leader

        【范围】
        - 制定 backend / frontend / regression / smoke 覆盖矩阵
        - 明确验证入口、方法与退出标准
        - 为 verify 阶段提供统一依据

        【输出物】
        - verification matrix
        - regression / smoke plan

        【验收标准】
        - verify 阶段有明确入口与退出标准
        - 关键主路径与高风险场景被覆盖
        - 可直接用于 release 前验证执行

        【风险 / blocker】
        - 前序实现边界不清会导致验证矩阵反复变化
        - 覆盖范围过散会降低可执行性

        【回报格式】
        ✅ DONE：矩阵 / 计划路径
        🧪 VERIFY：说明如何支撑 verify 与 release 决策
        ⚠️ RISK/BLOCKER：覆盖缺口或依赖未稳定点
        ▶️ NEXT：建议进入 release / rollback 收口
        ''').strip()
    },
    'ITER-013 Release/rollback/smoke alignment': {
        'task_type': 'operations_governance', 'priority': 'P2', 'depends_on': ['ITER-007 Policy engine + validate-run-safe endpoint','ITER-008 Task transition guard integration','ITER-010 Board violations dashboard','ITER-011 Board policy settings UI','ITER-012 Verification matrix and regression plan'],
        'description': dedent('''
        【任务类型】运维治理 / 收口
        【优先级】P2

        【背景 / 目标】
        让本轮新增治理能力可被安全发布、快速回退并稳定验证，对齐 release checklist、rollback 策略与 smoke 流程。

        【负责人】
        主 owner：MC Operations and Governance
        协作者：MC Verifier / MC Board Leader

        【范围】
        - 更新 release checklist
        - 对齐 rollback 策略
        - 明确 smoke 流程与新增治理能力的对应关系
        - 形成最终发布收口说明

        【输出物】
        - 更新后的 release checklist
        - rollback 说明
        - smoke alignment 说明

        【验收标准】
        - 可支撑 release 收口
        - rollback 路径清晰且可执行
        - smoke 步骤覆盖本轮新增能力关键点

        【风险 / blocker】
        - verify 不充分会导致发布结论失真
        - rollback 路径不清会放大发布风险

        【回报格式】
        ✅ DONE：更新内容 + 文档 / 清单路径
        🧪 VERIFY：说明如何支撑发布与回滚判断
        ⚠️ RISK/BLOCKER：上线缺口、验证不足、回退风险
        ▶️ NEXT：建议进入 release decision 或下一轮迭代
        ''').strip()
    },
}


def headers():
    if not TOKEN:
        raise SystemExit('MC_TOKEN is required')
    return {'Authorization': TOKEN if TOKEN.startswith('Bearer ') else f'Bearer {TOKEN}', 'Content-Type': 'application/json'}


def ensure_task_type_field(session):
    r = session.get(f'{BASE_URL}/api/v1/organizations/me/custom-fields', headers=headers(), timeout=30)
    r.raise_for_status()
    for field in r.json():
        if field['field_key'] == 'task_type':
            if BOARD_ID not in field.get('board_ids', []):
                patch = {'board_ids': sorted(set((field.get('board_ids') or []) + [BOARD_ID]))}
                u = session.patch(f"{BASE_URL}/api/v1/organizations/me/custom-fields/{field['id']}", headers=headers(), json=patch, timeout=30)
                u.raise_for_status()
            return field['id']
    payload = {
        'field_key': 'task_type',
        'label': 'task_type',
        'field_type': 'text',
        'ui_visibility': 'always',
        'required': False,
        'description': 'Mission Control task type classification',
        'board_ids': [BOARD_ID],
    }
    r = session.post(f'{BASE_URL}/api/v1/organizations/me/custom-fields', headers=headers(), json=payload, timeout=30)
    r.raise_for_status()
    return r.json()['id']


def main():
    s = requests.Session()
    ensure_task_type_field(s)
    r = s.get(f'{BASE_URL}/api/v1/boards/{BOARD_ID}/tasks?limit=200', headers=headers(), timeout=30)
    r.raise_for_status()
    items = r.json()['items']
    title_to_task = {t['title']: t for t in items}
    updates = []
    for title, spec in TASKS.items():
        task = title_to_task[title]
        dep_ids = [title_to_task[t]['id'] for t in spec['depends_on']]
        payload = {
            'description': spec['description'],
            'priority': spec['priority'],
            'depends_on_task_ids': dep_ids,
            'custom_field_values': {'task_type': spec['task_type']},
        }
        url = f"{BASE_URL}/api/v1/boards/{BOARD_ID}/tasks/{task['id']}"
        resp = s.patch(url, headers=headers(), json=payload, timeout=30)
        resp.raise_for_status()
        updates.append({'title': title, 'task_id': task['id'], 'priority': spec['priority'], 'task_type': spec['task_type'], 'depends_on_count': len(dep_ids)})
    print(json.dumps({'updated_count': len(updates), 'updates': updates}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
