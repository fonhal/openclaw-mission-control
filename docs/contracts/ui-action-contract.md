# UI action contract

## Purpose

This document defines the minimum contract for UI-triggered actions in Mission Control.
Its goal is to make sure the team shares the same expectations for what happens when a user activates an action.

## Audience

- frontend contributors
- backend and integration contributors
- runtime maintainers
- reviewers of high-risk workflows

## What this document does not cover

This document does not define:

- page layout and visual hierarchy
- exact button placement
- every low-level downstream payload detail

## Contract goals

Every action exposed in the UI should clearly define:

- target object
- preconditions
- trigger semantics
- side effects
- success feedback
- failure feedback
- post-action refresh expectations

## Minimum action contract shape

Each action should eventually be specified in terms of:

- **Action name**
- **Target object**
- **Purpose**
- **Preconditions**
- **Side effects**
- **Success result**
- **Failure result**
- **UI feedback**
- **Refresh behavior**

## Example contracts

### Action: refresh state

**Target objects**

- session
- task
- run
- job
- notification
- node

**Purpose**

Re-fetch the current state from the backing source.

**Preconditions**

- object or list exists in the current page context
- data source is reachable

**Side effects**

- no intended business mutation
- may update list or detail state in the UI

**Success result**

- latest available state is displayed

**Failure result**

- refresh fails and the UI keeps the previous state with clear failure feedback

**UI feedback**

- optional success indicator
- explicit failure message when refresh does not succeed

**Refresh behavior**

- this action is itself the refresh path

---

### Action: view details

**Target objects**

- any supported core object

**Purpose**

Open a more detailed view of the selected object.

**Preconditions**

- object exists
- user can access the target route or view

**Side effects**

- none

**Success result**

- detail page or panel opens with relevant context

**Failure result**

- UI explains that the object is unavailable or inaccessible

**UI feedback**

- route transition, panel open, or object detail render

**Refresh behavior**

- depends on the target page policy

---

### Action: retry task

**Target objects**

- task
- run

**Purpose**

Request a new execution attempt for an eligible failed object.

**Preconditions**

- current state permits retry
- user has permission to trigger retry
- downstream runtime is available

**Side effects**

- initiates a new execution attempt or retry workflow
- may change the original object's state and/or create a related run record

**Success result**

- retry request is accepted and the UI reflects the new transition or next expected state

**Failure result**

- the request is rejected or fails with a meaningful reason

**UI feedback**

- explicit success acknowledgement
- visible distinction between ineligible state, permission failure, runtime unavailability, and unknown failure

**Refresh behavior**

- the affected object should refresh automatically when practical, or the UI should clearly instruct the user to refresh

---

### Action: cancel task

**Target objects**

- task
- run

**Purpose**

Request cancellation for an execution that is still eligible to stop.

**Preconditions**

- object is in a cancellable state
- user has permission to cancel

**Side effects**

- sends a cancellation request to the underlying system
- may move the object into cancelling, cancelled, or equivalent intermediate states

**Success result**

- cancellation request is accepted or completed

**Failure result**

- system rejects the request with a meaningful reason

**UI feedback**

- clear indication that cancellation was requested, completed, or denied

**Refresh behavior**

- object state should refresh until the transition settles or the UI shows the action outcome clearly

## Design principles

### 1. Actions must be understandable

Users should not need deep runtime knowledge to understand what a button is expected to do.

### 2. High-risk actions need visible boundaries

The UI should make it clear when an action is:

- destructive or costly
- irreversible or hard to reverse
- likely to affect related objects
- gated by extra confirmation

### 3. Failure feedback must be actionable

Avoid generic failure messages when a more specific explanation is available.

### 4. Action loops should close

After the user triggers an action, they should be able to understand:

- whether the request was accepted
- whether state changed
- whether more waiting or refreshing is needed

## Current concrete example from the UI

### Action: delete agent

The current agents page already exposes a destructive delete flow backed by a confirmation dialog.

**Current route context**

- `/agents`

**Observed UI behavior**

- the page exposes row-level actions through the agents table
- delete opens a `ConfirmActionDialog`
- the dialog copy explicitly says the action cannot be undone
- the confirm button enters a pending state while deletion is in progress
- backend errors can be rendered inside the dialog

**Contract implications**

- this is a destructive action and should remain confirmation-gated
- the UI should distinguish between open-state, confirming-state, and failed-state
- optimistic list updates should not hide backend failure conditions

## Follow-up

As Mission Control grows, this document should stay aligned with:

- `../reference/commands-and-actions.md`
- `../architecture/runtime-integration.md`
- future object-state contracts for sessions, tasks, and jobs
