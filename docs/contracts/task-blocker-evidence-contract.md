# Task blocker and evidence contract

## Purpose

This document defines the canonical model and lifecycle contract for:

- `task_blockers`
- `task_evidence`

The goal is to make blockers and evidence first-class execution objects rather than vague status notes, while keeping them aligned with the task runtime metadata defined in `docs/contracts/task-schema-extension-contract.md`.

## Scope

This contract covers:

- data model shape
- enum/value sets
- ownership and mutation rules
- lifecycle transitions
- interaction with task validation
- audit/activity expectations

This contract does not cover:

- final SQL migration syntax
- detailed UI component design
- board policy CRUD schema in depth

---

## Design principles

1. **Blockers represent active execution constraints.**
   A blocker is not just any risk note. It is something currently preventing or materially constraining safe progress or completion.

2. **Evidence represents proof, not discussion.**
   Evidence should capture artifacts that support readiness, verification, or auditability. It is not a generic comment stream replacement.

3. **Missing evidence is not the same as a blocker.**
   A task can be progressing without enough completion evidence yet. That should not automatically create a blocker record unless policy or workflow explicitly requires one.

4. **Validation should consume blocker/evidence state without mutating semantics ad hoc.**
   Task validation should read structured blocker/evidence records and produce structured results rather than relying on comment parsing or tribal knowledge.

5. **Auditability matters.**
   Important blocker/evidence actions should be reconstructable from activity history.

---

## Relationship to task runtime fields

This contract works with the task fields defined in `task-schema-extension-contract.md`:

- `run_safe_status`
- `latest_policy_check_at`

Recommended interaction:

- readiness validation may fail because required baseline/acceptance metadata is missing
- completion validation may fail because required evidence is missing or blockers remain open
- blocker/evidence rows are the structured inputs that support those validation outcomes

Examples:

- open blocker exists -> completion may resolve to `blocked_open_blockers`
- required evidence missing -> completion may resolve to `blocked_missing_evidence`

---

## `task_blockers` contract

### Intent

A task blocker is a structured record of something currently preventing or materially constraining execution, review, or completion of a task.

### Ownership model

- usually created by the assigned worker, verifier, operator, or lead
- may also be auto-created by validation/policy flows when policy violations should be materialized as records
- resolved by a human or system action that explicitly closes the blocker lifecycle

### Core fields

Recommended fields:

- `id`
- `task_id`
- `type`
- `severity`
- `title`
- `description`
- `status`
- `evidence`
- `opened_by_agent_id`
- `resolved_by_agent_id`
- `opened_at`
- `resolved_at`
- `source`
- `meta`

### Field definitions

#### `task_id`
- foreign key to the owning task
- required

#### `type`

Represents the blocker class.

Suggested values:

- `missing_baseline`
- `missing_acceptance`
- `runtime_error`
- `dependency_blocked`
- `approval_waiting`
- `external_waiting`
- `policy_violation`
- `verification_failed`
- `unknown`

Rules:

- open enum for future expansion
- current implementations should preserve unknown values rather than crashing

#### `severity`

Represents urgency/impact of the blocker.

Suggested values:

- `low`
- `medium`
- `high`
- `critical`

Rules:

- severity affects visibility and triage priority, not blocker truthiness
- any open blocker can still block completion depending on policy; severity is not a substitute for status

#### `title`

Short human-readable summary.

Rules:

- required
- should fit list/table rendering

#### `description`

Longer explanation of the blocker.

Rules:

- optional but strongly recommended
- should explain what is blocked, why, and what is needed to unblock

#### `status`

Represents blocker lifecycle state.

Canonical values:

- `open`
- `mitigated`
- `resolved`

Semantics:

- `open`: blocker is active and should count as unresolved
- `mitigated`: blocker impact has been reduced or a workaround exists, but the original issue is not fully resolved
- `resolved`: blocker is no longer active

Validation consumption rule:

- `open` counts as unresolved
- `mitigated` should be policy-configurable; default recommendation is to treat it as still visible but not automatically completion-blocking unless the policy or blocker type requires it
- `resolved` does not count as unresolved

#### `evidence`

Optional structured support attached to the blocker itself.

Type:
- `object | null`

Examples:

```json
{
  "kind": "console_log",
  "value": "TypeError: Cannot read properties of undefined",
  "summary": "Error seen on board load"
}
```

Rules:

- intended for lightweight contextual support for the blocker
- not a replacement for `task_evidence`
- may reference evidence record ids later via `meta`

#### `opened_by_agent_id` / `resolved_by_agent_id`

- nullable for compatibility with system-created records
- support audit trail and ownership visibility

#### `opened_at` / `resolved_at`

- `opened_at` required at creation
- `resolved_at` null until status becomes `resolved`

#### `source`

Indicates whether the blocker came from a person or automation.

Suggested values:

- `manual`
- `policy_engine`
- `system`

#### `meta`

Type:
- `object | null`

Use for structured extension without changing the base contract.

Examples:

- dependency task ids
- approval ids
- retry counts
- external system references

---

## Blocker lifecycle

### Creation

A blocker may be created when:

- a worker discovers a real impediment
- a verifier finds a completion-stopping issue
- a dependency task blocks forward movement
- a policy engine chooses to materialize a validation failure as a blocker

Creation expectations:

- create with `status = open`
- set `opened_at`
- set `opened_by_agent_id` when a human/agent created it
- log an activity event such as `task_blocker_opened`

### Mitigation

A blocker may move to `mitigated` when:

- a workaround exists
- the issue still exists but no longer fully stops progress
- the team wants the blocker to remain visible while acknowledging partial recovery

Mitigation expectations:

- preserve original open context
- record mitigation notes in description/meta or via activity
- do not silently treat mitigated as resolved

### Resolution

A blocker may move to `resolved` when:

- the root issue no longer blocks the task
- the dependency has cleared
- required approval arrived
- policy violation has been corrected and no longer applies

Resolution expectations:

- set `resolved_at`
- set `resolved_by_agent_id` when known
- log an activity event such as `task_blocker_resolved`

### Reopening

Recommended rule:

- prefer a new blocker record for a new incident or a materially different recurrence
- allow reopen only when preserving continuity of the same blocker instance is operationally valuable

This avoids muddy audit trails.

---

## `task_evidence` contract

### Intent

Task evidence is a structured record of proof that supports implementation progress, verification, risk visibility, or completion readiness.

### Ownership model

- usually created by the worker, verifier, or operator
- may be system-created in limited cases where a machine-generated artifact is trustworthy and useful to persist

### Core fields

Recommended fields:

- `id`
- `task_id`
- `kind`
- `value`
- `summary`
- `created_by_agent_id`
- `created_at`
- `source`
- `meta`

### Field definitions

#### `task_id`
- foreign key to the owning task
- required

#### `kind`

Represents the evidence category.

Suggested values:

- `commit`
- `file_path`
- `screenshot`
- `console_log`
- `repro_steps`
- `test_result`
- `risk_note`
- `link`
- `design_doc`
- `unknown`

Rules:

- open enum for future addition
- evidence validation policies should operate on normalized `kind` values

#### `value`

Primary payload or locator for the evidence.

Type:
- `string`

Examples:

- git commit sha
- absolute or repo-relative file path
- URL
- serialized repro command
- short log excerpt id/path

Rules:

- required
- non-empty string
- should be the most direct retrievable pointer to the artifact

#### `summary`

Human-readable explanation of why the evidence matters.

Rules:

- optional but strongly recommended
- should help reviewers understand the proof without opening every artifact blindly

#### `created_by_agent_id`

- nullable for compatibility with system-generated evidence
- supports auditability

#### `created_at`

- required
- immutable after creation

#### `source`

Suggested values:

- `manual`
- `system`
- `imported`

#### `meta`

Type:
- `object | null`

Use for structured extension.

Examples:

- mime type
- file size
- screenshot dimensions
- commit branch
- test suite name

---

## Evidence lifecycle

Evidence has a simpler lifecycle than blockers.

Recommended default model:

- evidence is append-only
- avoid mutable status fields unless a strong need emerges later

### Creation

Create evidence when a materially useful proof artifact exists.

Examples:

- implementation commit recorded
- repro steps captured
- screenshot attached
- test result attached
- design doc path linked

Creation expectations:

- create immutable record with `created_at`
- log `task_evidence_added` activity when useful for auditability

### Update

Recommended rule:

- avoid general evidence mutation
- if summary or metadata must be corrected, allow minimal non-destructive edit paths
- if the artifact meaning changed materially, create a new evidence record instead

### Deletion

Recommended rule:

- prefer soft retention or explicit audit logging if evidence deletion is ever allowed
- do not silently delete evidence used for review/completion rationale

---

## Validation semantics

### Missing evidence vs blocker

These are distinct states.

#### Missing evidence

Meaning:
- the task may be complete or nearly complete, but proof required by policy is absent

Recommended validation outcome:
- completion validation returns `blocked_missing_evidence`
- no blocker record is required by default

#### Open blocker
n
Meaning:
- there is an active impediment that still constrains execution or completion

Recommended validation outcome:
- completion validation may return `blocked_open_blockers`
- open blocker count should come from structured blocker rows, not comments

### Policy integration expectations

Validation should be able to answer:

- which evidence kinds are present for the task
- whether required evidence kinds are missing
- how many blockers are still unresolved
- whether unresolved blockers include high-severity or escalation-worthy types

Recommended derived inputs to the policy engine:

- `evidence_kinds: set[str]`
- `open_blocker_count: int`
- optional future inputs:
  - `open_blocker_types: set[str]`
  - `critical_blocker_count: int`

---

## API and mutation expectations

### Task blockers

Recommended minimum flows:

- create blocker
- list blockers by task
- update blocker metadata
- resolve blocker

Preferred boundary:

- resolving a blocker should be explicit, not inferred from arbitrary PATCH side effects

### Task evidence

Recommended minimum flows:

- create evidence
- list evidence by task
- optional metadata edit

Preferred boundary:

- evidence records should be append-first and read-friendly

---

## Activity logging expectations

Recommended event kinds:

- `task_blocker_opened`
- `task_blocker_resolved`
- `task_evidence_added`
- `task_policy_violation_detected`

Optional later:

- `task_blocker_mitigated`
- `task_evidence_updated`
- `task_evidence_removed`

Activity events should help answer:

- what blocked the task
- when it became blocked
- what evidence was attached
- why completion was allowed or denied

---

## Boundary decisions

### Decision 1: blocker and evidence are separate first-class objects

Reason:
- blockers express constraints
- evidence expresses proof
- overloading one structure for both makes policy and UI logic muddy

### Decision 2: evidence should be append-first and mostly immutable

Reason:
- evidence is strongest when it behaves like an audit trail
- mutable evidence weakens trust in review history

### Decision 3: mitigated blockers should remain visible

Reason:
- partial recovery is operationally meaningful
- hiding mitigated blockers loses context reviewers may still need

### Decision 4: missing evidence should not automatically create blockers

Reason:
- otherwise blockers become a noisy mirror of every policy failure
- structured validation results already communicate the missing-proof condition well

### Decision 5: policy-engine-created blockers should be explicit when used

Reason:
- auto-created blockers can be useful for visibility, but only if humans can tell they were policy-generated rather than manually reported incidents

---

## Acceptance for this contract

This contract is satisfied when:

1. blocker and evidence records have clear, implementable field definitions
2. lifecycle states are explicit, especially for blocker resolution
3. unresolved blocker vs missing evidence semantics are clearly distinct
4. backend CRUD design can proceed without reopening core product meaning
5. validation and activity models have enough structure to consume blocker/evidence records consistently
