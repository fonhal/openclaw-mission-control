# Task schema extension contract

## Purpose

This document defines the canonical contract for the Phase 1 task governance fields:

- `baseline_ref`
- `acceptance_checklist`
- `run_safe_status`
- `latest_policy_check_at`

The goal is to make backend persistence, API behavior, and UI interpretation align on one shape and one lifecycle model.

## Scope

This contract covers:

- field shape
- null/default semantics
- allowed values
- mutation boundaries
- transition-driven update behavior
- compatibility rules for existing tasks

This contract does not cover:

- blocker/evidence table design in depth
- board policy table schema in depth
- UI component layout details

## Design principles

1. **Human-authored metadata should stay editable.**
   `baseline_ref` and `acceptance_checklist` are author-defined task metadata.

2. **Derived runtime metadata should stay system-owned.**
   `run_safe_status` and `latest_policy_check_at` reflect policy evaluation results and must not be treated as arbitrary user-editable fields.

3. **Missing metadata should be representable without ambiguity.**
   New and legacy tasks must support an explicit "not evaluated yet" shape.

4. **The API should preserve forward compatibility.**
   Existing clients that do not send the new metadata should continue to work.

---

## Field contract

### 1) `baseline_ref`

### Intent

`baseline_ref` points to the baseline artifact or anchor that defines what the task should be compared against before execution or verification.

Typical examples:

- existing screen/file used as design baseline
- requirement or spec document
- prior approved implementation reference
- prototype or mock reference

### Type

`object | null`

### Canonical shape

```json
{
  "type": "file",
  "value": "/absolute/path/to/file",
  "label": "Reviewed baseline"
}
```

### Required keys

- `type: string`
- `value: string`

### Optional keys

- `label: string`
- `meta: object`

### Rules

- `null` means no baseline has been defined.
- Empty object `{}` is invalid by contract and should be normalized to `null` or rejected at write boundaries.
- `value` must be a non-empty string.
- `type` should be an open string, but common values should include:
  - `file`
  - `url`
  - `task`
  - `doc`
  - `note`
- `meta` is reserved for future structured expansion and must not be required by current consumers.

### Ownership

Human-authored. Editable through task create/update flows.

---

### 2) `acceptance_checklist`

### Intent

`acceptance_checklist` captures the concrete, testable conditions that define when the task output is acceptable.

### Type

`string[]`

### Canonical shape

```json
[
  "Page can be opened",
  "No console red errors",
  "Key interaction closes the loop"
]
```

### Rules

- Default should be `[]`, not `null`, in read payloads.
- Write payloads may accept `null` for compatibility, but should normalize to `[]` unless explicit null persistence is required by a migration boundary.
- Items must be strings.
- Blank or whitespace-only items should be removed during validation.
- Checklist order is meaningful and should be preserved.
- Recommended authoring range: `3-7` meaningful items, but the storage contract should not hard-enforce that range unless policy explicitly requires it.

### Ownership

Human-authored. Editable through task create/update flows.

---

### 3) `run_safe_status`

### Intent

`run_safe_status` is a system-derived summary of the latest policy evaluation outcome for the task.

It answers: **is this task currently safe to start or complete under active board policy?**

### Type

`string`

### Allowed values

- `unknown`
- `ready`
- `blocked_missing_baseline`
- `blocked_missing_acceptance`
- `blocked_missing_evidence`
- `blocked_open_blockers`
- `blocked_runtime_error`
- `ready_with_warning`

### Rules

- `unknown` means the task has not yet been evaluated, or the current result is stale/unspecified.
- `ready` means the latest evaluation passed with no blocking violations.
- `blocked_*` values must correspond to a concrete validation failure class.
- `ready_with_warning` is reserved for warning-only policy outcomes.
- New values may be added later, but existing clients must treat unknown future values as non-fatal display strings.

### Ownership

System-owned. Should be updated only by policy evaluation logic.

### Mutation boundary

- Must be returned in read payloads.
- Must **not** be client-writable in general task create/update payloads.
- If internal services need to override it, that should happen through service-layer policy evaluation helpers, not generic PATCH semantics.

---

### 4) `latest_policy_check_at`

### Intent

`latest_policy_check_at` records when `run_safe_status` was last recomputed.

### Type

`datetime | null`

### Rules

- `null` means no policy evaluation has run yet.
- It must be written whenever readiness or completion validation executes, regardless of pass/fail.
- It should reflect the policy evaluation timestamp, not arbitrary task update time.

### Ownership

System-owned. Updated only by validation/evaluation flows.

### Mutation boundary

- Must be returned in read payloads.
- Must not be client-writable in generic task create/update flows.

---

## Read/write contract

### Create payload

Task create may accept:

- `baseline_ref`
- `acceptance_checklist`

Task create must not rely on client-supplied:

- `run_safe_status`
- `latest_policy_check_at`

### Update payload

Task update may accept:

- `baseline_ref`
- `acceptance_checklist`

Task update must reject or ignore client-supplied:

- `run_safe_status`
- `latest_policy_check_at`

Preferred behavior: do not expose those two fields on public write schemas at all.

### Read payload

Task read must include all four fields:

- `baseline_ref`
- `acceptance_checklist`
- `run_safe_status`
- `latest_policy_check_at`

### Normalization rules

To reduce ambiguity, API responses should normalize as follows:

- `baseline_ref`: `null` when absent
- `acceptance_checklist`: `[]` when absent
- `run_safe_status`: `unknown` when absent or not yet evaluated
- `latest_policy_check_at`: `null` when no evaluation has occurred

---

## Transition behavior

### On task create

- Persist author-provided `baseline_ref` and `acceptance_checklist`.
- Initialize `run_safe_status` to `unknown`.
- Initialize `latest_policy_check_at` to `null`.

### Before transition to `in_progress`

System runs readiness evaluation.

Inputs:

- active board policies
- `baseline_ref`
- `acceptance_checklist`

Outputs:

- update `run_safe_status`
- update `latest_policy_check_at`
- if validation fails, reject the transition with structured violations

### Before transition to `review` or `done`

System runs completion evaluation.

Inputs may include:

- active board policies
- evidence state
- blocker state
- task metadata

Outputs:

- update `run_safe_status`
- update `latest_policy_check_at`
- if validation fails, reject the transition with structured violations

### On metadata-only edits

Editing `baseline_ref` or `acceptance_checklist` does not need to synchronously recompute policy status on every change.

Recommended rule:

- keep existing `run_safe_status` until the next explicit validation or guarded status transition
- treat `latest_policy_check_at` as the timestamp of the actual evaluation, not of metadata edits

This keeps the meaning of both runtime fields precise.

---

## Compatibility and migration notes

### Existing persisted tasks

Legacy tasks may already contain:

- `baseline_ref = null`
- `acceptance_checklist = null`
- `run_safe_status = null` or `unknown`
- `latest_policy_check_at = null`

Read-path normalization should make those appear as:

- `baseline_ref = null`
- `acceptance_checklist = []`
- `run_safe_status = "unknown"`
- `latest_policy_check_at = null`

### Recommended backend tightening

1. **Model layer**
   - keep database columns nullable for migration safety
   - keep `run_safe_status` defaulted to `unknown`

2. **Schema layer**
   - `TaskRead.acceptance_checklist` should always serialize as list
   - `TaskCreate`/`TaskUpdate` should strip blank acceptance items
   - consider a dedicated typed schema for `baseline_ref` instead of raw `dict[str, Any]`

3. **API layer**
   - generic task PATCH should not accept derived runtime fields
   - policy validation endpoints and guarded transitions own runtime-field updates

---

## Boundary decisions

### Decision 1: `acceptance_checklist` should be list-first, not nullable-first

Reason:
- consumers almost always want iterable semantics
- `[]` is easier to reason about than `null`
- it reduces frontend conditional complexity

### Decision 2: `run_safe_status` is advisory for display, but authoritative for latest evaluation outcome

Reason:
- validation responses remain the source of detailed truth
- the task row still needs a compact status summary for list/detail rendering

### Decision 3: runtime fields should be system-owned only

Reason:
- user-writable derived state will drift from real policy evaluation
- status timestamps lose meaning if generic PATCH can set them arbitrarily

### Decision 4: `baseline_ref` remains flexible but not shapeless

Reason:
- different task types need different baseline anchors
- a minimal object contract preserves flexibility without making the field opaque junk

---

## Acceptance for this contract

This contract is satisfied when:

1. backend model/schema/API all agree on field ownership and read/write behavior
2. `run_safe_status` values are documented and stable enough for UI/backend coordination
3. `acceptance_checklist` null-vs-empty behavior is unambiguous
4. `baseline_ref` shape is minimally defined instead of treated as arbitrary JSON
5. `latest_policy_check_at` clearly represents evaluation time, not generic mutation time
