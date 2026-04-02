# Mission Control Expansion Roadmap

This document captures the product direction, requirement goals, and expansion roadmap for evolving OpenClaw Mission Control beyond a control-plane dashboard into an AI-native delivery operating system.

## Vision

Mission Control should evolve from:

- an operations dashboard for agents, boards, and gateways

into:

- an AI-native delivery system that can:
  - accept objectives
  - generate and refine execution plans
  - dispatch work according to agent capabilities
  - enforce run-safe delivery rules
  - track blockers and evidence
  - support human review and approvals
  - learn from execution over time

## Product positioning

Recommended positioning:

**OpenClaw-native Agent Delivery Control Plane**

This means the system is not merely a kanban UI, and not a replacement runtime for OpenClaw. Instead, it is the operational and governance layer above OpenClaw Gateway and agents.

## Current foundation

Mission Control already provides strong control-plane primitives:

- organizations
- board groups
- boards
- tasks
- agents
- gateways
- approvals
- activity timeline
- skills marketplace
- gateway-aware provisioning
- template-driven agent setup

These are the right foundations for expansion.

## Core gap to solve

The main gap is that Mission Control currently emphasizes orchestration and visibility more than planning quality and delivery governance.

The most important missing capabilities are:

1. structured objective-to-task planning
2. explicit dependency management
3. capability-aware dispatch
4. run-safe task gating
5. durable execution learning and retrospectives

---

## Expansion pillars

### 1. Planning Layer

Add a planning layer above tasks so the system can transform a higher-level goal into execution-ready work.

Key capabilities:

- objective intake
- plan generation
- milestones / epics / tasks / subtasks
- plan versioning
- dependency graphs
- replanning when blocked or drifted
- acceptance generation
- risk generation

Suggested new objects:

- `objectives`
- `objective_plans`
- `plan_items`
- `task_dependencies` (expanded usage)

### 2. Agent Capability Layer

Agent behavior should not rely only on templates and prompts. It should also include structured capability metadata.

Key capabilities:

- capability profiles
- role presets / agent bundles
- skill routing preferences
- dispatch scoring
- workload-aware assignment

Suggested additions:

- `capability_profile` on agents
- `agent_role_presets`
- `agent_skill_policies`
- assignee recommendation APIs

### 3. Execution Governance Layer

Mission Control should enforce safe execution and completion standards.

Key capabilities:

- baseline required before development
- acceptance required before execution
- evidence required before done
- blocker escalation
- pause/resume/blocked lifecycle recording
- policy-driven task transitions

Suggested additions:

- `board_policies`
- `task_blockers`
- `task_evidence`
- task run-safe validation APIs
- operator violations dashboard

### 4. Learning and Retrospective Layer

Execution should continuously improve the system.

Key capabilities:

- board memory
- recurring blocker patterns
- postmortems / retrospectives
- planning quality feedback
- reusable acceptance patterns
- improved role defaults over time

Suggested additions:

- richer board memory structures
- retrospective records
- planner feedback summaries

---

## Strategic roadmap

### Phase 1: Delivery governance foundation

Focus:

- baseline metadata
- acceptance metadata
- blockers
- evidence
- board policies
- task run-safe validation
- operator-facing violations visibility

This phase is the minimum safe foundation for AI-native execution.

Reference:

- [Phase 1 Delivery Governance Blueprint](./phase-1-delivery-governance-blueprint.md)

### Phase 2: Objective and planning layer

Focus:

- objectives
- plan drafts
- plan versions
- milestones and epics
- objective-to-task generation
- dependency-aware plan commit
- replanning flows

### Phase 3: Capability-aware dispatch

Focus:

- capability profiles
- role presets
- skill routing matrix
- candidate assignee scoring
- workload balancing

### Phase 4: Learning and optimization

Focus:

- retrospectives
- board memory improvements
- planning feedback loops
- recurring blocker analytics
- policy tuning recommendations

---

## Phase 1 requirements summary

Phase 1 is the first and most practical expansion step.

It should introduce:

1. task-level baseline and acceptance metadata
2. structured blockers and evidence
3. board-level governance policies
4. validation before starting or completing tasks
5. lead/operator visibility into policy violations

The detailed implementation plan lives in:

- [Phase 1 Delivery Governance Blueprint](./phase-1-delivery-governance-blueprint.md)

---

## Development priorities

Recommended first implementation priorities:

1. task schema/model enhancement
2. policy engine and validation endpoint
3. board policies CRUD and configuration UI
4. blocker/evidence data model
5. lead/operator violations dashboard

If resources are constrained, the most valuable first three are:

1. task baseline + acceptance fields
2. policy engine + validation endpoint
3. violations dashboard

---

## Definition of success

Mission Control expansion is successful when the platform can do all of the following reliably:

- reject unsafe execution when a task lacks baseline or acceptance
- reject incomplete delivery when evidence is missing
- show operators which tasks are risky or non-compliant
- preserve a clear audit trail for blockers, validation, and delivery evidence
- provide a clean path toward objective planning and smarter dispatch in later phases

---

## Relationship to the existing platform

This roadmap assumes Mission Control remains:

- the control plane
- the governance layer
- the operator UI
- the gateway-aware orchestration layer

It does **not** attempt to replace:

- OpenClaw Gateway as the runtime bridge
- OpenClaw agents as the execution runtime
- skills as runtime-discoverable capabilities

Instead, it strengthens how Mission Control governs and structures those existing systems.
