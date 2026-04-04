# Task action specification

## Purpose

This document defines the current and expected task-related action model for Mission Control.
It is intended to stabilize the write-path understanding around tasks before further implementation expansion.

## Why this matters

Tasks are currently one of the main interactive objects in Mission Control.
They appear in board detail flows, activity surfaces, approval context, and reporting-oriented summaries.

Because of that, task actions need clearer documentation than a generic object description.

## Main route context

Primary route:
- `/boards/[boardId]`

Task actions currently appear most naturally inside the board detail worksurface rather than in a global task management page.

## Primary task actions

### Create task

Intent:
- create a new task within a board

Expected inputs:
- title
- description
- priority
- due date
- tags
- board-scoped custom field values

Expected behavior:
- validates required fields
- validates required custom fields when configured
- creates task within the current board scope
- makes the new task available in board views and related activity context

### Update task

Intent:
- change the current task state or metadata

Expected inputs may include:
- title
- description
- status
- priority
- due date
- assignee
- tags
- dependencies
- custom field values

Expected behavior:
- preserves board scope
- updates visible task state in the current worksurface
- keeps related detail views coherent

### Delete task

Intent:
- remove a task from the board workflow

Expected behavior:
- remains destructive by definition
- should be confirmation-gated
- should provide failure feedback if backend deletion fails
- should not silently remove the task if the final backend state is uncertain

### Comment on task

Intent:
- add contextual discussion or execution notes to a task

Expected behavior:
- appends a new task comment
- associates the comment with the selected task
- makes the comment available to task detail and activity/feed contexts

### Update task status

Intent:
- move the task through its lifecycle

Current known states:
- `inbox`
- `in_progress`
- `review`
- `done`

Expected behavior:
- the UI should make status transitions visible and understandable
- activity surfaces should be able to represent status changes

### Update task priority

Intent:
- express urgency / ordering importance

Current known priorities:
- `low`
- `medium`
- `high`

### Update task dependencies

Intent:
- express ordering or prerequisite relationships between tasks

Expected behavior:
- dependency-aware UI should help users understand blocking state
- dependency information should not be treated as purely decorative metadata

### Update task custom fields

Intent:
- apply board-scoped structured metadata to a task

Expected behavior:
- only fields visible for the board should be editable
- required fields should be validated before mutation succeeds
- field values should remain canonicalized when persisted and displayed

## Preconditions and boundaries

### Board scope is required

Task actions are board-scoped, not global by default.
The board context is therefore part of the action contract.

### Read vs write access matters

Task visibility does not imply task mutation access.
Board-level access control must continue to distinguish:

- can read
- can write

### Destructive actions need stronger safety

Delete and similar irreversible actions should not visually blend with harmless edits.
They require stronger UX and state handling.

## Expected action states

For major task actions, the UI should make these states explicit where relevant:

- idle
- submitting
- success
- failure
- permission-blocked

## Activity side effects

Task actions should be understood as having downstream visibility consequences.
Depending on the action, they may surface in:

- board-local live feed
- global activity feed
- approval context
- task detail views

## Documentation follow-up

This document should later be extended with:

- concrete payload examples
- field-level validation notes
- task deletion copy guidance
- action-to-feed mapping table
