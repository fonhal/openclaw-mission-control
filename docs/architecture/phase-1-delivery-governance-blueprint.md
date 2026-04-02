# Phase 1 Delivery Governance Blueprint

This document defines the first expansion step for Mission Control to evolve from an operations/control-plane dashboard into an AI-native delivery system with run-safe execution gates.

## Goals

Phase 1 focuses on delivery governance rather than full planning automation.

Primary goals:

1. Add task-level baseline and acceptance metadata.
2. Add structured blockers and evidence.
3. Add board-level policy enforcement.
4. Prevent unsafe task transitions (`in_progress`, `review`, `done`) when required conditions are missing.
5. Surface policy violations clearly in the lead/operator UI.

Out of scope for Phase 1:

- Full objective-to-plan generation
- Multi-version planning graphs
- Automatic dependency-based replanning
- Advanced capability-based dispatch scoring

---

## Why this phase first

Mission Control already has strong foundations as a control plane:

- agents
- boards
- tasks
- gateways
- approvals
- activity history
- skills marketplace

What is currently missing is a strong delivery quality gate between task creation and task execution. Phase 1 adds that gate.

---

## Scope summary

Phase 1 introduces four capability groups:

1. **Task readiness metadata**
   - baseline reference
   - acceptance checklist
   - run-safe status
2. **Execution risk tracking**
   - blockers
   - policy violations
3. **Delivery proof capture**
   - evidence records
4. **Board governance**
   - policy configuration
   - validation before task transitions

---

## Data model changes

### 1) Extend `tasks`

Add the following fields to the task model:

- `baseline_ref: JSON | null`
- `acceptance_checklist: JSON | null`
- `run_safe_status: str | null`
- `latest_policy_check_at: datetime | null`

Suggested `run_safe_status` values:

- `unknown`
- `ready`
- `blocked_missing_baseline`
- `blocked_missing_acceptance`
- `blocked_runtime_error`
- `ready_with_warning`

Example `baseline_ref`:

```json
{
  "type": "file",
  "value": "/absolute/path/to/ui-optimized-prototype.html",
  "label": "Final reviewed UI baseline"
}
```

Example `acceptance_checklist`:

```json
[
  "Page can be opened",
  "No console red errors",
  "Key interaction closes the loop",
  "Visible copy is localized",
  "No blocking layout breakage"
]
```

### 2) Add `task_blockers`

Suggested columns:

- `id`
- `task_id`
- `type`
- `severity`
- `description`
- `evidence`
- `status`
- `opened_by_agent_id`
- `resolved_by_agent_id`
- `opened_at`
- `resolved_at`

Suggested `type` values:

- `missing_baseline`
- `missing_acceptance`
- `runtime_error`
- `dependency_blocked`
- `approval_waiting`
- `external_waiting`
- `unknown`

Suggested `status` values:

- `open`
- `mitigated`
- `resolved`

### 3) Add `task_evidence`

Suggested columns:

- `id`
- `task_id`
- `kind`
- `value`
- `summary`
- `created_by_agent_id`
- `created_at`

Suggested `kind` values:

- `commit`
- `file_path`
- `screenshot`
- `console_log`
- `repro_steps`
- `risk_note`
- `link`

### 4) Add `board_policies`

Suggested columns:

- `id`
- `board_id`
- `policy_key`
- `enabled`
- `config_json`
- `created_at`
- `updated_at`

Initial policies:

- `no_baseline_no_dev`
- `no_acceptance_no_dev`
- `require_evidence_before_done`
- `blocker_requires_escalation`
- `pause_requires_reason`

Example policy config:

```json
{
  "required_evidence_kinds": ["commit", "repro_steps"],
  "warning_only": false
}
```

---

## Backend service work

### Policy evaluation service

Add a dedicated service, for example:

- `backend/app/services/policy_engine.py`

Core responsibilities:

#### `evaluate_task_readiness(task, board_policies)`

Return a structured result such as:

```json
{
  "status": "blocked_missing_baseline",
  "violations": [
    {
      "policy": "no_baseline_no_dev",
      "message": "Task is missing baseline_ref"
    }
  ]
}
```

#### `evaluate_task_completion(task, evidence, blockers, board_policies)`

Return a structured result such as:

```json
{
  "status": "blocked",
  "violations": [
    {
      "policy": "require_evidence_before_done",
      "message": "Missing required commit evidence"
    }
  ]
}
```

### Task transition guards

Hook policy validation into task lifecycle updates.

#### Before moving a task to `in_progress`
Check:

- baseline exists (if policy enabled)
- acceptance checklist exists (if policy enabled)

If validation fails:

- block the transition, or auto-convert to blocked status based on policy behavior
- create a blocker record
- emit an activity event

#### Before moving a task to `review` or `done`
Check:

- required evidence exists
- no unresolved blockers remain

If validation fails:

- reject the transition
- return structured violations
- emit an activity event

### Validation endpoint

Add an endpoint like:

- `POST /api/v1/tasks/{task_id}/validate-run-safe`

Suggested response:

```json
{
  "ok": false,
  "status": "blocked_missing_acceptance",
  "violations": [
    {
      "policy": "no_acceptance_no_dev",
      "message": "Task is missing acceptance checklist"
    }
  ],
  "recommended_actions": [
    "Add 3-7 testable acceptance items before starting execution"
  ]
}
```

---

## Activity model additions

Add activity event types for delivery governance.

Suggested activity types:

- `task_blocker_opened`
- `task_blocker_resolved`
- `task_evidence_added`
- `task_policy_violation_detected`
- `task_run_safe_validated`
- `agent_paused`
- `agent_resumed`
- `agent_blocked`
- `agent_unblocked`

This enables operators to reconstruct why execution was blocked or allowed.

---

## Frontend work

### 1) Task detail page

Add four new sections:

#### Baseline
Show:

- baseline file/link/reference
- whether it exists
- readiness state

#### Acceptance checklist
Show:

- checklist items
- empty-state warning

#### Blockers
Show:

- active blockers
- severity
- description
- evidence
- resolve action

#### Evidence
Show:

- evidence records grouped by type
- missing required evidence warnings

### 2) Board-level violations view

Add a lead/operator-focused view with filters such as:

- ready
- blocked
- review
- violations

Prioritize these violations:

- missing baseline
- missing acceptance
- open blockers
- done/review without required evidence

### 3) Board policy settings

Add a settings page or board settings tab where operators can:

- enable/disable policies
- configure required evidence kinds
- choose hard-block vs warning-only behavior

---

## Suggested implementation order

### Step 1: database + models

Implement:

- task field extensions
- `task_blockers`
- `task_evidence`
- `board_policies`

### Step 2: schemas + CRUD + APIs

Implement:

- read/write endpoints
- activity logging for blocker/evidence/policy actions

### Step 3: policy engine

Implement:

- task readiness evaluation
- task completion evaluation
- unit tests

### Step 4: transition enforcement

Hook validation into:

- `in_progress` transitions
- `review` / `done` transitions

### Step 5: task detail UI

Add:

- baseline section
- acceptance section
- blockers section
- evidence section

### Step 6: board violations + policy settings UI

Add:

- violations dashboard
- policy settings page

---

## Suggested development tasks

### DEV-1: Task model enhancement

Scope:

- extend task model/schema
- migration
- read/write API

Acceptance:

- tasks can persist baseline and acceptance metadata
- API returns values correctly

### DEV-2: Task blockers

Scope:

- blocker model/schema/api/activity
- task detail blocker UI

Acceptance:

- blocker can be created and resolved
- blockers appear in task detail

### DEV-3: Task evidence

Scope:

- evidence model/schema/api/activity
- task detail evidence UI

Acceptance:

- evidence can be attached and listed by task
- missing required evidence is visible in UI

### DEV-4: Board policies

Scope:

- policy model/schema/api
- policy settings UI

Acceptance:

- board can enable and configure policies
- policy settings persist correctly

### DEV-5: Policy engine + validation

Scope:

- policy engine service
- validate-run-safe endpoint
- task transition guards

Acceptance:

- task without baseline/acceptance cannot enter `in_progress` when policy requires them
- task without required evidence cannot enter `done`
- structured violations are returned clearly

### DEV-6: Lead violations dashboard

Scope:

- board violations tab/list
- filters and summaries

Acceptance:

- operators can quickly identify non-compliant tasks
- violations view summarizes why a task is blocked or unsafe

### DEV-7: Agent pause/blocked lifecycle normalization

Scope:

- structured agent lifecycle actions
- reason capture
- activity logging

Acceptance:

- pause/resume/blocked transitions always record reason and timeline event

---

## Testing priorities

### Backend

Minimum tests:

- missing baseline blocks readiness
- missing acceptance blocks readiness
- missing evidence blocks completion
- open blocker blocks completion
- blocker create/resolve API works
- evidence create/list API works
- validation endpoint returns expected structure

### Frontend

Minimum tests:

- task detail renders baseline/acceptance/blockers/evidence
- violations page renders policy issues
- board policy settings save correctly

---

## Expected outcome after Phase 1

After Phase 1, Mission Control should gain:

1. A clear definition of when work is allowed to start.
2. A clear definition of what proof is required before work is done.
3. Structured blocker tracking instead of ad hoc status notes.
4. A board-level governance system that operators can configure.
5. Better operator visibility into risky or non-compliant tasks.

This phase creates the foundation required for later phases such as objective planning, dependency graphs, capability-based dispatch, and automated replanning.
