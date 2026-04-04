# Smoke test

## Purpose

This document defines a minimal manual smoke test for Mission Control after meaningful UI, integration, or release changes.

## Audience

- maintainers
- reviewers
- contributors validating a change before handoff or release

## What this document does not cover

This document is not a full QA plan.
It defines only the minimum checks needed to catch obvious breakage in high-value paths.

## Smoke-test goals

A smoke test should quickly answer:

- does the app load
- can users reach the primary pages
- do key objects render
- do obvious failures surface clearly

## Minimum smoke test path

### 1. App shell loads

Verify:

- the frontend opens successfully
- the initial route does not crash
- the top-level shell or navigation is visible

### 2. Primary navigation works

Verify:

- a user can move into at least one major list page
- navigation labels and structure are understandable
- no obvious dead routes are exposed

### 3. Core list page works

Verify at least one major list page such as sessions or tasks/runs.

Check:

- page renders
- loading state is understandable
- empty state is understandable
- error state is understandable when relevant

### 4. Core detail page works

Verify at least one detail path.

Check:

- detail view opens
- the primary object is recognizable
- current state is visible
- related context is not obviously broken

### 5. Refresh behavior is understandable

Verify:

- refresh is available where expected
- the UI communicates when refresh succeeds or fails
- stale data is not silently misrepresented as current

### 6. One controlled action path is checked

Pick one safe or approved action path and verify:

- the action is visible only when appropriate
- feedback is understandable
- the resulting state or next-step expectation is visible

## Failure handling

If the smoke test fails, record:

- which page or object failed
- whether the issue blocks release
- whether the failure is product, integration, or environment-related
- what follow-up is required

## Notes

This document should evolve with the product’s primary operator path.
The goal is not maximum coverage; the goal is fast detection of obvious operational regressions.
