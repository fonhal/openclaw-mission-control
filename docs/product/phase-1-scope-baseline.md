# Phase 1 scope baseline

## Purpose

This document freezes the first implementation phase for Mission Control board execution governance.
It defines what this phase includes, what it explicitly excludes, how success will be judged, and how the first batch of implementation tasks should be bounded.

The goal of phase 1 is not to solve all board workflow problems.
The goal is to establish the minimum governance baseline that makes task execution more structured, reviewable, and implementation-safe.

## Phase goal

Deliver a usable governance foundation for board task execution so that Mission Control can:

- capture an explicit baseline for a task before execution
- represent acceptance criteria in a structured way
- record blockers and evidence as first-class task context
- validate whether a task is ready to start or ready to complete
- support implementation with clear backend contracts for these behaviors

## Why this phase exists

Current task handling is too light for reliable agent-assisted delivery.
Important execution decisions still rely on implicit context, task descriptions, or manual interpretation.
That increases ambiguity in at least four places:

- what is actually in scope for a task
- what must be true before work is considered acceptable
- what blocks execution or completion
- what evidence proves a task is ready for review or done

Phase 1 addresses those gaps by adding a small, coherent governance layer around tasks.

## In scope

Phase 1 includes the minimum product, contract, and backend work required to make governance metadata operational for tasks.

### 1. Scope and acceptance baseline for this delivery wave

Mission Control should have one explicit baseline artifact that defines:

- phase scope
- non-scope
- success criteria
- priority order
- first-batch implementation boundaries

This baseline is the planning source for the linked delivery tasks in this phase.

### 2. Task schema extensions for governance metadata

The task model should support the minimum fields needed to anchor governance behavior.

Included fields for phase 1:

- `baseline_ref`
  - points to the planning or scope baseline that governs the task
- `acceptance_checklist`
  - stores explicit acceptance items that can be inspected and validated
- `run_safe_status`
  - indicates whether the system considers the task safe to execute or complete
- `latest_policy_check_at`
  - records when governance validation last ran

Phase 1 scope includes defining field meaning, allowed states where relevant, read/write behavior, and response shape expectations.

### 3. Blocker model and evidence model

Tasks need first-class support for execution blockers and delivery evidence.

Included concepts:

- blocker records attached to tasks
- evidence records attached to tasks
- lifecycle expectations for creation, update, and resolution
- visibility needed for validation and operator review

The model should make it possible to distinguish:

- work that is not started because it is blocked
- work that progressed but lacks evidence
- work that is complete enough to review or close

### 4. Board policy design and validation rules

Phase 1 includes a first policy layer for task governance.

Included policy areas:

- readiness-to-start checks
- readiness-for-review checks
- readiness-for-done checks
- severity categories such as hard-block vs warning

Included validation outcomes:

- structured violations
- clear mapping from missing task data to operator-visible validation results
- enough rule definition to support backend implementation without re-deciding product intent

### 5. Validation-safe backend support

The backend should support storage, retrieval, update, and validation for the phase 1 governance slice.

Included backend capabilities:

- schema/model support for new task governance fields
- migrations for persisted storage changes
- CRUD support for blockers and evidence
- validation endpoint or service that evaluates task readiness/completion safety
- structured API responses for violations and status
- activity logging where needed to preserve traceability

### 6. Documentation sufficient for implementation and review

Phase 1 includes the product/design artifacts needed so implementation work is not forced to infer missing intent.

Included documentation outputs:

- this phase baseline
- schema/contract design notes
- blocker/evidence model design
- board policy matrix and validation rule summary

## Explicitly out of scope

The following items are not part of phase 1, even if they are likely future work.

### 1. Full workflow redesign of all board experiences

Phase 1 is not a complete re-think of all board UX, navigation, or task page structure.
It only establishes the governance slice needed to improve execution quality.

### 2. Rich visual workflow builders or policy authoring UI

No advanced UI for composing policies, drag-and-drop workflows, or rule builders is required in this phase.
Policy definition may be configuration- or contract-driven.

### 3. Cross-board governance unification

Phase 1 is board-task focused.
It does not need to generalize governance across every object type such as sessions, jobs, notifications, or nodes.

### 4. Full approval system redesign

This phase does not redesign approval flows broadly.
It may interact with readiness rules, but approval orchestration itself is not the main deliverable.

### 5. Advanced analytics, scoring, or reporting

No dashboards for policy trends, execution scoring, SLA reporting, or board health analytics are required for phase 1.

### 6. Automation beyond the governance baseline

This phase does not need to implement autonomous planning, automatic task decomposition, or deep orchestration features outside the specific governance checks required by the scoped tasks.

### 7. Broad frontend polish work unrelated to governance

Unless a frontend change is required to support or expose the phase 1 governance baseline, visual polish and unrelated UI refinements are out of scope.

## Priority order

Phase 1 priorities should be interpreted in this order.

### P0 — must land for phase success

1. Freeze the phase baseline and first-batch task boundaries.
2. Define task schema extensions clearly enough for implementation.
3. Define blocker and evidence models clearly enough for implementation.
4. Define validation policy matrix and hard-block/warning behavior.
5. Implement backend persistence and validation support for the above.

If any of these are missing, phase 1 is incomplete.

### P1 — should land within the same delivery wave

1. Activity logging tied to blocker/evidence changes where it materially improves auditability.
2. Response shapes and validation outputs refined enough for frontend/UI consumption.
3. Clear contract language for readiness vs completion validation semantics.

These are part of a strong phase 1 but subordinate to the P0 baseline.

### P2 — useful follow-on, not required to declare phase 1 complete

1. Additional UI affordances beyond the minimum implementation path.
2. Broader policy coverage outside the initial task-governance slice.
3. Secondary operational reporting derived from governance data.

## Success criteria

Phase 1 is successful when all of the following are true.

### Product clarity

- Scope, non-scope, priorities, and first-batch boundaries are explicit and stable.
- Contributors can explain what phase 1 is for without reinterpreting task descriptions.

### Contract clarity

- Task governance fields have clear meaning and boundaries.
- Blocker and evidence concepts have clear lifecycle expectations.
- Validation rules distinguish hard blocks from warnings.

### Implementation readiness

- Architecture/backend contributors can implement without reopening core product intent questions.
- Acceptance conditions for each first-batch task are directly traceable to this baseline.

### Runtime usefulness

- The system can identify when key governance prerequisites are missing.
- Missing baseline, acceptance, or evidence can be surfaced as structured validation results.

### Reviewability

- A reviewer can inspect a task and understand scope anchor, acceptance anchor, blockers, evidence, and validation state without relying on tribal knowledge.

## First-batch task boundaries

These task boundaries define the intended cut for the first delivery wave.

### ITER-001 — Phase 1 scope freeze and acceptance baseline

Purpose:

- establish the source planning artifact for the entire phase

Must include:

- phase scope
- non-scope
- priority order
- success criteria
- task boundaries for ITER-002 through ITER-007

Done when:

- the baseline artifact exists
- downstream tasks can reference it directly
- scope ambiguity is materially reduced

### ITER-002 — Task schema extension design

Purpose:

- define the task-level governance fields and contracts

Must include:

- field definitions for `baseline_ref`, `acceptance_checklist`, `run_safe_status`, `latest_policy_check_at`
- expected value types and lifecycle semantics
- edge cases and update behavior

Done when:

- field boundaries are explicit enough for backend implementation and API contract review

### ITER-003 — Blocker and evidence model design

Purpose:

- define task blocker/evidence structures and lifecycle

Must include:

- model fields
- relation to task state
- creation/update/resolve expectations
- distinction between unresolved blocker and missing evidence

Done when:

- the model is implementable without reopening core semantics

### ITER-004 — Board policy design and validation rules

Purpose:

- define the rules that determine readiness and completion safety

Must include:

- policy keys or matrix
- hard-block vs warning distinctions
- validation expectations for missing baseline, acceptance, blockers, and evidence

Done when:

- backend implementation can encode rule logic from a stable product definition

### ITER-005 — Backend task model and migration implementation

Purpose:

- persist governance metadata on tasks

Must include:

- migration(s)
- schema/model changes
- read/write API support for new fields

Done when:

- governance fields are stored, returned, and updateable through supported backend paths

### ITER-006 — Backend blocker/evidence CRUD

Purpose:

- make blockers and evidence operational in the backend

Must include:

- create/list/update/resolve flows as applicable
- schema and activity logging support where needed

Done when:

- blocker/evidence records can be used by validation and inspection flows

### ITER-007 — Policy engine and validate-run-safe endpoint

Purpose:

- evaluate governance readiness in a structured way

Must include:

- validation service or policy engine
- endpoint behavior for readiness/completion-safe checks
- structured violations for missing baseline, acceptance, blockers, or evidence

Done when:

- callers receive machine-usable validation results aligned with the policy matrix

## Dependency logic across first-batch tasks

The tasks are related, but phase 1 should treat their dependency shape clearly.

### Definition dependencies

- ITER-001 anchors scope for all downstream tasks.
- ITER-002, ITER-003, and ITER-004 define the contract layer.

### Implementation dependencies

- ITER-005 depends primarily on ITER-002.
- ITER-006 depends primarily on ITER-003.
- ITER-007 depends primarily on ITER-004 and secondarily on the implemented persistence model from ITER-005 and ITER-006.

### Practical delivery rule

Detailed implementation should not invent semantics that belong in ITER-002 through ITER-004.
If those semantics are missing, the correct action is to tighten the design artifacts, not to let implementation fill the gap ad hoc.

## Acceptance baseline for the phase

The phase-level acceptance baseline is satisfied when:

1. a stable scope baseline exists and is referenced by downstream work
2. task governance fields are defined with clear semantics
3. blocker/evidence models are defined with lifecycle clarity
4. validation rules are defined with structured outcomes
5. backend implementation supports storage and validation of the defined governance slice
6. missing prerequisites can be surfaced as structured validation failures rather than hidden tribal knowledge

## Decision rules for ambiguous requests during this phase

If a proposed addition does not strengthen the task-governance baseline directly, it should usually be deferred.

Use these rules:

- include it now if it is required to make governance data explicit, validateable, or implementation-safe
- defer it if it mainly improves polish, breadth, or future flexibility without being necessary for phase 1 execution quality
- ask for a follow-on task if it extends beyond board task governance into broader product surfaces

## Follow-on areas after phase 1

Likely next-phase candidates include:

- frontend UX for richer governance visibility and editing
- expanded policy coverage across more object types
- approval/policy interaction refinement
- audit/reporting views derived from governance metadata
- broader workflow automation on top of validated task state

## Source references

This baseline is aligned with:

- `docs/product/mission.md`
- `docs/product/information-architecture.md`
- `docs/reference/data-models.md`
- `docs/contracts/task-state-contract.md`
