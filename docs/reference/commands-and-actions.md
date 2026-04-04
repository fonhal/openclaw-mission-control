# Commands and actions

## Purpose

This document lists the main user-facing actions exposed in Mission Control and explains what they mean operationally.
It is a reference guide, not the source of truth for implementation details.

## Audience

- operators and internal users
- frontend contributors
- maintainers reviewing action scope and wording

## What this document does not cover

This document does not define:

- full CLI manuals
- visual button placement
- low-level adapter implementation

## Action categories

### Read actions

Examples:

- view a list
- open a detail page
- inspect logs
- open a related object

Characteristics:

- usually no business side effects
- should be widely available and easy to understand

### Refresh actions

Examples:

- refresh a list
- refresh object state
- re-fetch status information

Characteristics:

- low operational risk
- still requires a clear success and failure model

### Control actions

Examples:

- retry a failed execution
- cancel an eligible execution
- trigger an approved operational workflow

Characteristics:

- has side effects
- depends on permissions and state eligibility
- must be documented in contracts

### Diagnostic actions

Examples:

- inspect runtime details
- open debugging context
- review error details
- inspect supporting history

## Recommended action entry format

Each action should eventually be documented with at least:

- action name
- target object
- purpose
- preconditions
- whether it has side effects
- success feedback
- failure feedback
- whether a refresh is required afterward

## Phase-one priority actions

### View sessions

Target object:
- session

Purpose:
- inspect active, recent, and problematic sessions

Side effects:
- none

### View session details

Target object:
- session

Purpose:
- inspect a specific session more deeply

Side effects:
- none

### View task/run/job details

Target objects:
- task
- run
- job

Purpose:
- understand execution state, errors, and lifecycle

Side effects:
- none

### Refresh state

Target objects:
- session
- task
- run
- job
- notification
- node

Purpose:
- re-fetch current state from the backing source

Side effects:
- low-risk, no direct business mutation expected

### Retry execution

Target objects:
- task
- run

Purpose:
- re-attempt a failed execution path

Side effects:
- yes
- should only be allowed when the underlying system says retry is valid

### Cancel execution

Target objects:
- task
- run

Purpose:
- stop an execution that is still eligible for cancellation

Side effects:
- yes
- should clearly communicate whether cancellation is requested, pending, or complete

### View notifications

Target object:
- notification

Purpose:
- inspect delivery outcomes and related issues

Side effects:
- none

## Naming guidelines

Action names should:

- start with a clear verb
- describe what the user expects to happen
- avoid vague or overloaded wording

Preferred examples:

- Refresh state
- View details
- View logs
- Retry task
- Cancel task

Avoid unless the meaning is already very clear in context:

- Process
- Execute
- Submit
- Sync

## Follow-up

As actions become real product features, this file should be kept aligned with:

- `../contracts/ui-action-contract.md`
- `../architecture/runtime-integration.md`
