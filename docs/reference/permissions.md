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

Examples already visible in the current UI include:

- agents page access is restricted to organization owners and admins
- gateways page access is restricted to admins
- custom fields access is restricted to admins
- skill marketplace and packs navigation is shown only for admins
- deleting an agent is a destructive action guarded by an explicit confirmation dialog

## Current observable permission patterns

From the current frontend structure, Mission Control already distinguishes between at least:

- signed-in vs signed-out users
- admin-only navigation and page access
- action-level confirmation for destructive operations

This means permissions are not only a backend concern; they are already shaping:

- sidebar visibility
- page accessibility
- destructive action flow

## UI expectations

When permission affects a page or action, the UI should help the user understand whether the limit is due to:

- lack of access
- object state
- environment unavailability
- another gating condition

## Follow-up

This file should next be extended with a concrete mapping of:

- admin-only routes
- signed-in-only routes
- destructive actions that require confirmation
- actions that are hidden vs disabled
