# Runtime integration

## Purpose

This document defines the boundary between Mission Control and the OpenClaw runtime ecosystem.
It explains how the UI should read state, trigger controlled actions, and interpret downstream results.

## Audience

- frontend contributors
- backend and integration contributors
- runtime maintainers
- reviewers of action and state model changes

## What this document does not cover

This document does not define:

- detailed UI layout
- final button copy
- exhaustive payload schemas for every action

## Integration goals

Mission Control should integrate with runtime-facing systems in a way that makes:

- important state easy to inspect
- high-value actions safe to trigger
- action outcomes visible and explainable
- source-of-truth boundaries explicit

## Integration object categories

The first-class runtime-facing object categories are expected to include:

- sessions
- tasks / runs / jobs
- notifications
- nodes
- other approved operational objects introduced later

## Two integration modes

### 1. Read-oriented integration

Use this for:

- listing objects
- viewing details
- inspecting health and history
- reading logs or summaries

Characteristics:

- lower risk
- should be prioritized early
- forms the base of most pages

### 2. Write-oriented integration

Use this for:

- retries
- cancellations
- controlled refreshes
- approved operational triggers

Characteristics:

- has side effects
- must be eligibility-aware
- must return understandable UI feedback
- should be documented in contracts

## Boundary recommendations

### UI layer

Should:

- render current state
- expose allowed actions
- display reasons when actions are unavailable
- reflect action progress and outcome

Should not:

- embed runtime-specific orchestration assumptions everywhere
- silently guess ambiguous runtime state

### Integration/backend layer

Should:

- call the underlying systems
- normalize errors and result shapes
- enforce or surface eligibility checks
- return UI-consumable responses

### Runtime layer

Should:

- execute actual operational logic
- own authoritative state transitions
- emit resulting state and errors

## Action design expectations

Every runtime-integrated action should define:

- target object type
- preconditions
- whether it is read-only or write-oriented
- expected success result
- expected failure modes
- whether state should auto-refresh afterward

## Error handling expectations

Mission Control should differentiate errors such as:

- object not found
- action not allowed in current state
- permission denied
- runtime unavailable
- timeout or temporary failure
- unknown downstream failure

## Phase-one integration priorities

Recommended first wave:

1. read-only lists for core objects
2. detail views for core objects
3. explicit refresh behavior
4. a small set of high-value, low-ambiguity write actions
5. closed-loop action feedback in the UI

## Open questions to resolve later

- exact adapter or API boundaries
- caching strategy and freshness guarantees
- when polling is sufficient vs when event-driven updates are needed
- how long-running state transitions should be represented in the UI
