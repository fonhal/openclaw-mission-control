# Permissions

## Purpose

This document defines how Mission Control should think about permission-sensitive viewing and action behavior.
It is meant to guide page and action design, even before every permission rule is fully implemented.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers reviewing access-sensitive features

## What this document does not cover

This document does not define the final auth provider implementation or every role in the system.
It focuses on permission design expectations.

## Permission principles

### 1. Visibility and action are different

A user may be allowed to view an object without being allowed to mutate it.
The UI should not assume these permissions are identical.

### 2. Unavailable actions should be understandable

If a user cannot perform an action, Mission Control should prefer clear disabled-state or explanatory handling over silent disappearance when that would improve understanding.

### 3. High-risk actions need stronger gating

Actions with meaningful side effects should be more tightly permissioned and, where appropriate, confirmation-gated.

### 4. Page access should match object sensitivity

Pages centered on operational control or sensitive diagnostics may require stricter access than general status views.

## Permission categories

Mission Control should be able to reason separately about:

- page access
- object visibility
- detail visibility
- action execution
- diagnostic depth

## Example permission-sensitive cases

Examples that often need explicit design:

- viewing session summaries vs full session detail
- viewing task state vs retrying or cancelling a task
- viewing notification status vs re-triggering a notification workflow
- viewing node health vs triggering node-affecting actions

## UI expectations

When permission affects a page or action, the UI should help the user understand whether the limit is due to:

- lack of access
- object state
- environment unavailability
- another gating condition

## Future expansion

As roles and auth modes stabilize, this document should add:

- concrete roles or access categories
- page-level permission mapping
- action-level permission mapping
- guidance for disabled vs hidden actions
