# Approval flow specification

## Purpose

This document defines the approval-oriented flow model in Mission Control at a specification level.
It is intended to stabilize how approval objects behave across pages, activity surfaces, and operator decision points.

## Why this matters

Approvals are one of the clearest governance-oriented primitives in Mission Control.
They are not only data objects; they are decision points that affect operator trust, safety, and workflow pacing.

## Main route contexts

Observed or implied route contexts include:

- `/approvals`
- `/boards/[boardId]/approvals`
- `/boards/[boardId]`
- `/activity`

This means approvals are both:

- a dedicated object/workflow area
- a supporting concept embedded into broader board and activity surfaces

## Core approval lifecycle

Current observable statuses include:

- `pending`
- `approved`
- `rejected`

## Main approval events

The runtime and feed layers already expose approval-oriented event types such as:

- `approval.created`
- `approval.updated`
- `approval.approved`
- `approval.rejected`

## Flow stages

### Stage 1 — approval appears

An approval enters the system as a pending request.
At this point the UI should help the operator understand:

- what action is being requested
- what object or board context it belongs to
- what confidence or metadata is attached
- where the user can review it in more detail

### Stage 2 — operator reviews the request

The operator should be able to inspect the approval in enough context to decide whether it is safe or appropriate.
Relevant context may include:

- board
- task
- triggering agent
- confidence score
- surrounding activity

### Stage 3 — operator resolves the request

The operator chooses an action such as:

- approve
- reject

At this point the system should make:

- pending state
- result state
- error state

clear to the user.

### Stage 4 — approval result propagates

After resolution, the result should be representable across:

- approvals pages
- board detail context
- live feed surfaces
- audit/activity surfaces

## Required specification concerns

### Context clarity

An approval should never feel contextless.
Users should be able to tell what the approval is about, not only that an approval exists.

### Confidence is supporting context, not authority

Confidence helps interpret the request but should not replace operator judgment.

### Approval state transitions must stay legible

The UI should not make it hard to distinguish:

- still pending
- already approved
- already rejected
- failed to update

### Approval actions are governance-sensitive

Even if technically simple, approval decisions are high-importance actions.
They deserve stronger clarity than ordinary metadata edits.

## Expected UI states

For approval mutation flows, the UI should account for:

- idle
- loading current approval state
- submitting resolution
- success
- failure
- stale or already-resolved cases

## Relationship to activity surfaces

Approval flow is not isolated.
It already participates in global and board-local event streams.
This means the approval model should stay aligned with feed/event documentation.

## Documentation follow-up

This document should later add:

- approval object field summary
- approval decision payload examples
- approval result copy conventions
- approval-to-feed mapping examples
