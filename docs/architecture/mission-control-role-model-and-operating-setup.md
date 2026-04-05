# Mission Control role model and operating setup

## Purpose

This document proposes a concrete role model, board structure, status flow, RACI mapping, and seed-ready object setup for OpenClaw Mission Control.
It is intended to turn the current product direction into an operable software engineering and operations model that can later be implemented in permissions, board configuration, approval flows, and initial data seeding.

## Audience

- product leads
- board leaders and delivery managers
- frontend, backend, and platform contributors
- QA and governance reviewers
- operators responsible for day-to-day use of Mission Control

## What this document does not cover

This document does not define:

- final database schema
- final API payloads for role or permission management
- visual design details
- exact route implementation
- organization-specific HR ownership rules

## Why this document exists

Mission Control is not only a development project.
It is also an operations and governance surface for OpenClaw.
That means the operating model cannot be reduced to a generic engineering split such as frontend, backend, and QA.
The product itself is meant to coordinate controlled actions, approvals, boards, gateways, agents, and activity state.

Because of that, role design should cover both:

1. **build roles**: who defines, implements, validates, and releases Mission Control
2. **run roles**: who observes, operates, approves, and responds in Mission Control

This document proposes a practical first version of that model.

## Design principles

The role model should follow these principles:

1. **Object-aware design**
   - permissions and ownership should map to stable product objects such as board, task, approval, gateway, and agent
   - related runtime objects such as session, run, job, node, and notification should be modeled as secondary but visible objects

2. **Separation between delivery and control**
   - implementing the control surface and operating the control surface are related but different jobs
   - the same person may hold multiple roles, but the responsibilities should remain distinct in the model

3. **Risk-aware action boundaries**
   - high-risk actions should never be silently mixed with normal task editing
   - approval, audit, and execution responsibilities should be modeled explicitly

4. **Board-centric execution**
   - current Mission Control page structure is more board-centric and administration-centric than a pure runtime-object navigation model
   - the proposed setup should align with the current product shape, not with an imagined future-only architecture

5. **Verification-first delivery**
   - status transitions, ownership, and acceptance should reflect the project working agreement and board leader principles already documented in this repository

## Current product shape that this setup aligns to

Based on the current docs, Mission Control currently centers its visible UI around the following primary areas:

- dashboard
- live feed
- boards and board detail
- skills area
- administration

The visible primary objects are therefore closer to:

- board group
- board
- task
- approval
- gateway
- agent
- activity event
- organization membership

The following objects remain important at the architecture and runtime level and should be treated as secondary but supported objects:

- session
- run
- job
- notification
- node
- audit record
- policy

## Proposed role model

The proposed first-phase role model uses eight practical roles.
This is enough to create clear ownership without over-fragmenting the system.

### Product lead

Purpose:
- define product scope, priorities, and milestone outcomes

Primary responsibilities:
- decide what belongs in Mission Control and what does not
- approve scope changes and phase priorities
- align object boundaries, page purpose, and roadmap sequencing
- accept major cross-functional delivery outcomes

Typical objects:
- board group
- board
- task
- tag
- custom field
- roadmap item
- approval outcome

### Board leader

Purpose:
- make work executable, assignable, visible, and reviewable

Primary responsibilities:
- break goals into executable tasks
- enforce single-owner task assignment
- ensure every task has scope, non-scope, inputs, outputs, and acceptance criteria
- drive status transitions and delivery closure
- keep blockers visible and actionable

Typical objects:
- board
- task
- approval request
- board activity
- board memory

### Frontend engineer

Purpose:
- implement the user-facing control surface and state presentation

Primary responsibilities:
- build pages, components, and route-level workflows
- implement state rendering that honestly reflects action eligibility and system uncertainty
- align visible UI behavior with action contracts and page ownership rules

Typical objects:
- task
- board
- UI section
- validation artifact

### Backend and integration engineer

Purpose:
- implement service behavior and translate operational state into UI-consumable shapes

Primary responsibilities:
- build backend APIs and integration adapters
- normalize runtime-facing state into stable product objects
- implement action handling, result feedback, and downstream coordination
- keep contracts aligned across product, UI, and runtime boundaries

Typical objects:
- task
- run
- approval
- gateway
- agent
- integration event

### Platform and runtime engineer

Purpose:
- maintain the execution environment, gateways, agents, and runtime stability

Primary responsibilities:
- operate deployment and environment setup
- manage gateway and agent lifecycle paths
- support incident recovery and runtime diagnostics
- maintain the reliability boundary between Mission Control and the underlying runtime systems

Typical objects:
- gateway
- agent
- node
- operation
- job
- deployment record

### QA and verification owner

Purpose:
- validate behavior, state transitions, and release readiness

Primary responsibilities:
- define verification criteria and test plans
- validate task and session state behavior
- confirm that action eligibility and result handling match contracts
- own VERIFY to DONE transition evidence

Typical objects:
- task
- verification artifact
- test report
- regression issue

### Security and governance reviewer

Purpose:
- define and review governance, approval, and audit boundaries

Primary responsibilities:
- classify high-risk actions
- define approval requirements and audit expectations
- review auth, policy, and permission-sensitive changes
- approve or reject high-risk operations where required

Typical objects:
- approval
- policy
- audit record
- sensitive operation
- auth setting

### Operator and incident commander

Purpose:
- observe day-to-day system state, respond to issues, and coordinate recovery when needed

Primary responsibilities:
- monitor dashboard, live feed, boards, and administrative health signals
- perform low- and medium-risk operational actions
- create escalation and incident tracking work
- coordinate or direct response during active incidents

Typical objects:
- dashboard signal
- activity event
- task
- gateway snapshot
- agent status
- approval request

## Permission model recommendation

Mission Control should use **RBAC with object-scoped permissions**.
A simple global admin versus non-admin split is not sufficient for a product that mixes delivery coordination, approvals, operations, and governance.

### Permission verbs

Recommended permission verbs:

- `read`
- `create`
- `update`
- `assign`
- `transition`
- `approve`
- `execute`
- `admin`

### Permission object types

Recommended permission object types:

- `organization`
- `board_group`
- `board`
- `task`
- `approval`
- `tag`
- `custom_field`
- `gateway`
- `agent`
- `activity`
- `job`
- `node`
- `policy`
- `audit_record`

## Role-to-permission matrix

The following table is a recommended first-cut matrix.
It is intended to drive initial product and permission design discussions, not to serve as a final enforcement source.

| Role | Board and task | Approval | Gateway and agent | Policy and audit | High-risk execute |
|---|---|---|---|---|---|
| Product lead | read, create, update | read | read | read | no |
| Board leader | read, create, update, assign, transition | read, create, update | read | read | no |
| Frontend engineer | read, update own work items | read | read | no | no |
| Backend and integration engineer | read, create, update, transition relevant work | read | read, update limited | read | limited |
| Platform and runtime engineer | read, create, update, transition | read, create, update | read, create, update, admin limited scope | read | yes, some approval-gated |
| QA and verification owner | read, create, update verification items | read | read | no | no |
| Security and governance reviewer | read | approve, reject, read | read | read, create, update | yes, with explicit governance rules |
| Operator and incident commander | read, create, update operational items | create, read | read, update limited | read | limited, approval-gated |

> **Warning**
> High-risk actions should never be exposed solely on the basis of generic edit rights.
> They should be tied to explicit `execute` permission and approval requirements when applicable.

## Recommended board group structure

To fit the current product shape, boards should be organized by operational responsibility domain rather than by raw technical layer alone.

### Board group: product strategy

Purpose:
- manage product boundary, scope, information architecture, and roadmap decisions

Recommended boards:
- `Roadmap & Scope`
- `Information Architecture`
- `UX / Page Design`

Primary roles:
- product lead
- board leader
- frontend engineer
- documentation owner if later introduced

### Board group: core delivery

Purpose:
- manage implementation work across frontend, backend, and integration boundaries

Recommended boards:
- `Frontend Delivery`
- `Backend Delivery`
- `Integration & Contracts`

Primary roles:
- frontend engineer
- backend and integration engineer
- platform and runtime engineer
- QA and verification owner

### Board group: runtime operations

Purpose:
- manage gateway, agent, runtime stability, and incident response work

Recommended boards:
- `Gateway & Agents`
- `Runtime Stability`
- `Incidents & Recovery`

Primary roles:
- platform and runtime engineer
- operator and incident commander
- security and governance reviewer

### Board group: governance and quality

Purpose:
- manage approvals, risk, verification, audit, and documentation closure

Recommended boards:
- `Approvals & Risk`
- `QA & Verification`
- `Documentation & Onboarding`

Primary roles:
- QA and verification owner
- security and governance reviewer
- product lead
- board leader

## Board design rules

Each board should optimize for one primary responsibility type.
Do not mix planning, implementation, incident handling, and documentation closure into one generic catch-all board.

Recommended board categories:

- planning board
- delivery board
- runtime board
- governance board

This keeps state transitions meaningful and makes drill-down behavior easier to interpret.

## Recommended tags

### Object tags

- `board`
- `task`
- `approval`
- `gateway`
- `agent`
- `activity`
- `job`
- `node`
- `policy`

### Page-area tags

- `dashboard`
- `live-feed`
- `boards`
- `board-detail`
- `skills`
- `admin`

### Work-type tags

- `research`
- `proposal`
- `design`
- `implementation`
- `integration`
- `verification`
- `incident`
- `documentation`
- `release`
- `governance`

### Risk tags

- `low-risk`
- `medium-risk`
- `high-risk`
- `approval-required`
- `audit-required`

### Priority tags

- `P0`
- `P1`
- `P2`
- `P3`

## Task lifecycle recommendation

Mission Control should adopt the six-state lifecycle already aligned with this repository's board leader principles.

Recommended states:

- `TODO`
- `DOING`
- `BLOCKED`
- `VERIFY`
- `DONE`
- `CLOSED`

### State definitions

#### TODO

Meaning:
- work has been defined well enough to start

Entry expectations:
- single owner assigned
- scope defined
- non-scope defined where needed
- inputs and expected outputs defined
- acceptance criteria present

#### DOING

Meaning:
- work is actively being executed

Entry expectations:
- a single primary owner exists
- progress can be reported
- known blockers can be surfaced quickly

#### BLOCKED

Meaning:
- work cannot progress due to a meaningful dependency or issue

Entry expectations:
- blocker reason is captured
- unblock owner or path is named
- next recommended action is visible

#### VERIFY

Meaning:
- implementation is complete enough to validate

Entry expectations:
- completion summary provided
- changed files, artifact links, or commit references attached
- verification method defined
- known risks recorded

#### DONE

Meaning:
- verification passed and the deliverable is accepted

Entry expectations:
- acceptance criteria met
- verification complete
- no unresolved critical issue remains for the task's intended outcome

#### CLOSED

Meaning:
- the work has been fully closed out from a delivery tracking perspective

Entry expectations:
- state has been synchronized
- results archived or referenced
- follow-up tasks are explicit if still needed
- no further tracking is required for this work item

### Allowed transitions

Primary path:

- `TODO -> DOING -> VERIFY -> DONE -> CLOSED`

Exception paths:

- `DOING -> BLOCKED`
- `BLOCKED -> DOING`
- `VERIFY -> DOING`
- `DONE -> DOING` in rare reopen cases
- `DONE -> CLOSED`

## Recommended role-to-state interaction rules

| Role | TODO | DOING | BLOCKED | VERIFY | DONE | CLOSED |
|---|---|---|---|---|---|---|
| Product lead | create, inspect | inspect | inspect | inspect | confirm major outcomes | close major scope items |
| Board leader | create | transition | transition | transition | confirm | close |
| Frontend engineer | claim | update own work | raise blocker | submit for verify | no | no |
| Backend and integration engineer | claim | update own work | raise blocker | submit for verify | no | no |
| Platform and runtime engineer | claim | update own work | raise blocker | submit for verify | no | no |
| QA and verification owner | inspect | inspect | inspect | verify | confirm verification outcomes | no |
| Security and governance reviewer | inspect | inspect | inspect | review governance-sensitive work | confirm governance-sensitive outcomes | no |
| Operator and incident commander | create operational work | update operational work | raise incident blockers | attach evidence | no | no |

## RACI model

The following RACI tables are intended to make ownership explicit for common Mission Control work patterns.

### Product scope change

| Activity | R | A | C | I |
|---|---|---|---|---|
| decide whether a new page belongs in Mission Control | Product lead | Product lead | Board leader, frontend engineer, backend engineer | QA, operator |
| define a new primary object or workflow | Product lead | Product lead | Backend engineer, security reviewer, frontend engineer | all affected roles |
| reprioritize a milestone | Board leader | Product lead | QA, platform engineer | all affected roles |

### Page and feature delivery

| Activity | R | A | C | I |
|---|---|---|---|---|
| page design | Frontend engineer | Product lead | Board leader, backend engineer | QA |
| frontend implementation | Frontend engineer | Board leader | Backend engineer | QA |
| backend or integration implementation | Backend engineer | Board leader | Platform engineer, frontend engineer | QA |
| action-contract implementation | Backend engineer | Product lead | Frontend engineer, security reviewer | QA, operator |

### Runtime and incident response

| Activity | R | A | C | I |
|---|---|---|---|---|
| routine monitoring | Operator and incident commander | Operator and incident commander | Platform engineer | Product lead |
| incident response execution | Platform engineer | Operator and incident commander | Backend engineer, security reviewer | Product lead |
| recovery action execution | Platform engineer or operator | Operator and incident commander | Security reviewer for high-risk actions | affected teams |
| post-incident review | Operator and incident commander | Product lead | Platform engineer, backend engineer, QA | all affected roles |

### Verification and release

| Activity | R | A | C | I |
|---|---|---|---|---|
| verification planning | QA and verification owner | Board leader | Frontend engineer, backend engineer | Product lead |
| verification execution | QA and verification owner | Board leader | implementation owner | Product lead |
| release readiness | Platform engineer | Product lead | QA, security reviewer, board leader | all affected roles |
| post-release acceptance | QA and verification owner and operator | Product lead | Platform engineer, backend engineer | all affected roles |

### Governance and approvals

| Activity | R | A | C | I |
|---|---|---|---|---|
| classify high-risk actions | Security reviewer | Product lead | Platform engineer, backend engineer | operator |
| define approval flow | Security reviewer | Product lead | Backend engineer, frontend engineer | all affected roles |
| approve or reject a high-risk operation | Security reviewer | Security reviewer | Operator, platform engineer | Product lead |
| audit a sensitive workflow | Security reviewer | Product lead | Platform engineer | Board leader |

## Seed-ready organization setup

The following YAML-like examples are intended as a seed-ready conceptual baseline.
They are not final schema, but they are concrete enough to guide implementation.

### Organization

```yaml
organization:
  key: openclaw-mission-control
  name: OpenClaw Mission Control
  description: Control-surface delivery and operations organization for OpenClaw
```

### Board groups

```yaml
board_groups:
  - key: product-strategy
    name: Product Strategy
    purpose: Manage scope, information architecture, page planning, and milestones

  - key: core-delivery
    name: Core Delivery
    purpose: Manage frontend, backend, and integration implementation work

  - key: runtime-operations
    name: Runtime Operations
    purpose: Manage gateways, agents, incidents, and runtime stability

  - key: governance-quality
    name: Governance & Quality
    purpose: Manage approvals, risks, verification, documentation, and closure
```

### Boards

```yaml
boards:
  - key: roadmap-scope
    group: product-strategy
    name: Roadmap & Scope

  - key: ia-ux
    group: product-strategy
    name: IA & UX

  - key: frontend-delivery
    group: core-delivery
    name: Frontend Delivery

  - key: backend-delivery
    group: core-delivery
    name: Backend Delivery

  - key: integration-contracts
    group: core-delivery
    name: Integration & Contracts

  - key: gateway-agents
    group: runtime-operations
    name: Gateway & Agents

  - key: runtime-stability
    group: runtime-operations
    name: Runtime Stability

  - key: incidents-recovery
    group: runtime-operations
    name: Incidents & Recovery

  - key: approvals-risk
    group: governance-quality
    name: Approvals & Risk

  - key: qa-verification
    group: governance-quality
    name: QA & Verification

  - key: docs-onboarding
    group: governance-quality
    name: Documentation & Onboarding
```

### Roles

```yaml
roles:
  - key: product_lead
    name: Product Lead

  - key: board_leader
    name: Board Leader

  - key: frontend_engineer
    name: Frontend Engineer

  - key: backend_engineer
    name: Backend and Integration Engineer

  - key: platform_engineer
    name: Platform and Runtime Engineer

  - key: qa_owner
    name: QA and Verification Owner

  - key: security_reviewer
    name: Security and Governance Reviewer

  - key: operator_ic
    name: Operator and Incident Commander
```

### Task fields

```yaml
task_fields:
  - title
  - task_type
  - priority
  - owner
  - board
  - related_object
  - scope
  - non_scope
  - inputs
  - outputs
  - acceptance_criteria
  - verification_method
  - risk_blocker
  - rollback_plan
  - approval_required
  - status
```

### Task types

```yaml
task_types:
  - research
  - proposal
  - design
  - implementation
  - integration
  - verification
  - incident
  - release
  - documentation
  - governance
```

### Statuses

```yaml
statuses:
  - TODO
  - DOING
  - BLOCKED
  - VERIFY
  - DONE
  - CLOSED
```

### Approval policies

```yaml
approval_policies:
  - key: destructive-runtime-action
    applies_to:
      - gateway
      - agent
      - policy
    approver_role: security_reviewer

  - key: production-config-change
    applies_to:
      - gateway
      - deployment
    approver_role: product_lead

  - key: sensitive-access-change
    applies_to:
      - organization
      - role
      - auth
    approver_role: security_reviewer
```

## Recommended implementation sequence

### Phase 1: minimum operating model

Implement first:

- board groups
- the eight core roles
- six-state task lifecycle
- tags for risk, object, and work type
- basic approval gate placeholders

### Phase 2: permission refinement

Implement next:

- object-scoped permission checks for gateway, agent, approval, and policy
- board-detail enforcement for owner, verification evidence, and acceptance criteria
- explicit `execute` permission for high-risk actions

### Phase 3: operations maturity

Implement later:

- incident templates
- release templates
- verification templates
- audit and retrospective views
- policy-driven action eligibility badges in the UI

## Open questions to resolve before full implementation

1. Should operator and incident commander remain one role in v1, or should they split early?
2. Should approvals be modeled as a dedicated board object, a task subtype, or both?
3. Which administrative actions should be approval-gated in the first release?
4. Should task templates be board-level, organization-level, or both?
5. How much of this setup should be seed data versus configurable through the UI?

## Recommended next documents

After this document, the most useful follow-up specs would be:

1. a permissions specification that maps these roles to concrete action and route rules
2. a seed-data specification for board groups, boards, roles, tags, and statuses
3. a board-detail task template specification aligned with the board leader principles
4. an approval flow specification for high-risk actions in administration and runtime operations
