# Operator workflow

## Purpose

This document describes the intended workflow for internal users operating Mission Control day to day.
It focuses on how a user should move through the UI to inspect state, decide what matters, and use controlled actions safely.

## Audience

- internal operators
- on-call or support contributors
- team members using Mission Control as a day-to-day control surface

## What this document does not cover

This document does not define:

- implementation details
- API schemas
- all underlying command behavior
- release or rollback procedures

## Default operator loop

The expected operator loop is:

1. scan high-level state
2. identify the object that needs attention
3. inspect details and recent changes
4. decide whether action is needed
5. trigger a controlled action if eligible
6. verify the result or resulting transition

## Recommended page flow

### Step 1: start from overview

An operator should usually begin with the top-level dashboard or a comparable high-level page.
The goal is to answer:

- Is anything obviously wrong?
- Which object category needs attention first?
- Is this an observation-only situation or an action-needed situation?

### Step 2: drill into the relevant object list

Move into the relevant list page, such as:

- sessions
- tasks / runs / jobs
- notifications
- nodes

The goal is to narrow the problem down to a specific object.

### Step 3: inspect the object detail

Once an object is selected, the operator should confirm:

- current state
- recent transitions
- visible failure reasons or blockers
- whether any available action is actually allowed

### Step 4: take action only when justified

If an action is exposed in the UI, the operator should still verify:

- the current state permits the action
- the action matches the intended outcome
- the risk level is acceptable for the current situation

### Step 5: confirm the post-action state

After any write action, the operator should check:

- was the request accepted
- did state visibly change
- is the object still transitioning
- is more waiting or refresh needed

## Operator design expectations

Mission Control should help operators:

- understand what they are seeing before acting
- distinguish safe read paths from risky write paths
- avoid guessing whether a control actually worked
- recognize when a follow-up step is needed

## Anti-patterns

Avoid workflows where operators must:

- guess which page owns an object
- trigger actions without understanding side effects
- infer success from missing error messages
- switch through too many unrelated surfaces to understand one object

## Follow-up documents

Operators commonly move next into:

- `../reference/commands-and-actions.md`
- `../contracts/ui-action-contract.md`
- relevant object detail documentation as it is added
