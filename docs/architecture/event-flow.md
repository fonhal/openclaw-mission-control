# Event flow

## Purpose

This document describes how important events and state changes should move through Mission Control so contributors can reason about feedback loops, refresh behavior, and action outcomes.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers working on state visibility and action feedback

## What this document does not cover

This document does not define exact transport protocols or every event schema.
Those should be documented separately where needed.

## Core flow

A typical Mission Control event flow should be understood as:

1. a runtime or connected system changes state
2. an event, result, or updated state becomes available
3. the integration layer normalizes the signal
4. the application layer updates UI-facing state
5. the UI reflects the change in a list, detail page, badge, or feedback area

## Action-triggered flow

For write actions, the flow should be:

1. a user triggers an action from the UI
2. the request is validated and sent downstream
3. the downstream system accepts, rejects, or fails the request
4. the UI receives a result and reflects the immediate outcome
5. the relevant object is refreshed or updated until its visible state settles

## Design expectations

Mission Control should avoid leaving users in ambiguous states after actions.
The user should be able to tell:

- whether the action was accepted
- whether the object changed
- whether the system is still waiting for a final state

## Failure cases

The event flow should make room for:

- downstream errors
- temporary unavailability
- stale object state
- delayed state transitions

The UI should not collapse all of these into a single indistinguishable failure path.
