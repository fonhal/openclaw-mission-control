# Task state contract

## Purpose

This document defines how Mission Control should represent task- and run-like lifecycle state so that actions, visibility, and operator expectations stay aligned.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers working on operational workflows

## What this document does not cover

This document does not define:

- exact task database schema
- every execution subtype in the system
- final backend enum values

## Contract goals

Task and run state in Mission Control should help users answer:

- what stage the work is in
- whether it succeeded, failed, or is still changing
- whether retry or cancellation is allowed
- what the next useful step is

## Minimum representation

At minimum, a task or run shown in Mission Control should make room for:

- stable identifier
- current lifecycle state
- timing or recency context
- summary of failure or blockage when present
- action eligibility hints for retry, cancel, or inspection

## Lifecycle buckets

The UI contract should preserve understandable lifecycle buckets such as:

### Pending

Meaning:
- the work is accepted but has not started meaningful execution yet

Expected UI behavior:
- show that it is queued or waiting
- avoid implying failure or completion

### Running

Meaning:
- execution is in progress or the system is actively working on it

Expected UI behavior:
- show clear progress-state styling
- indicate that cancellation may still be relevant if supported

### Succeeded

Meaning:
- execution completed successfully

Expected UI behavior:
- make success distinct from merely disappearing from attention
- preserve inspection access

### Failed

Meaning:
- execution ended unsuccessfully

Expected UI behavior:
- highlight failure clearly
- show a useful failure summary if available
- expose retry only when truly eligible

### Cancelled

Meaning:
- execution was stopped intentionally or transitioned into a cancelled end state

Expected UI behavior:
- distinguish cancellation from failure
- avoid implying it was a successful completion

### Unknown or transitional

Meaning:
- the system cannot yet determine a stable lifecycle bucket, or the object is between meaningful phases

Expected UI behavior:
- avoid false precision
- indicate that the state may still settle after refresh or time

## Contract rules

### 1. Action availability must track state honestly

Retry and cancel must not appear available when the underlying state does not support them.

### 2. Failure and cancellation are different

The UI should not collapse failed and cancelled outcomes into one generic terminal label.

### 3. Transitional states should be visible when meaningful

If the user needs to wait, the UI should make that visible instead of pretending the final result is already known.

### 4. Lists and details should not contradict each other

A task that is shown as retryable in one place should not be shown as non-retryable elsewhere without a clear reason.

## Future expansion

This file should later capture:

- concrete state mapping tables
- retry eligibility rules
- cancellation eligibility rules
- timing and freshness expectations
- task vs run relationship notes
