# System overview

## Purpose

This document describes the overall system shape of Mission Control and the relationship between the UI, application logic, integration boundaries, and the OpenClaw runtime ecosystem.

## Audience

- Frontend contributors
- Backend and integration contributors
- Maintainers working on system-level design

## What this document does not cover

This document does not define:

- page copy and visual layout
- field-level schemas
- detailed action contracts
- release operations

## System role

Mission Control is a control-surface layer.
It is not the runtime, and it should not become the sole source of truth for operational state.
Its job is to:

- gather important operational information
- present it in stable and understandable views
- route controlled actions into underlying systems
- show users what happened after an action

## Layers

### 1. UI layer

Responsible for:

- route structure and page composition
- state rendering
- action entry points
- immediate user feedback

Not responsible for:

- generating authoritative runtime state
- embedding complex runtime orchestration logic

### 2. application layer

Responsible for:

- shaping data for page needs
- managing frontend state and transitions
- coordinating reads, mutations, and refresh behavior

### 3. integration layer

Responsible for:

- talking to backend and OpenClaw-connected systems
- adapting data from runtime-facing sources into UI-consumable shapes
- translating action requests into controlled downstream calls

### 4. runtime and external systems

Includes:

- OpenClaw runtime and sessions
- cron, messaging, nodes, browser, and related operational services
- logs, activity streams, and external execution results

## Core operational objects

Mission Control should organize around stable objects such as:

- session
- task
- run
- job
- notification
- node

These objects should anchor both page structure and contract design.

## Core data flow

A typical end-to-end flow should be understood as:

1. runtime or connected systems produce state and events
2. the integration layer reads and normalizes those signals
3. the application layer prepares UI-friendly state
4. the UI renders lists, details, and action availability
5. the user triggers a controlled action
6. the integration layer forwards the request downstream
7. the runtime or connected system executes and reports results
8. the UI reflects the updated state and action outcome

## Key constraints

### Mission Control is not the source of truth

It should present and coordinate operational state, not redefine authoritative runtime behavior inside the UI.

### High-risk actions need explicit boundaries

Any action with meaningful side effects should have:

- clear eligibility rules
- visible feedback
- failure semantics
- documentation in contracts

### UI should not hide system ambiguity

If the system does not know whether an action is allowed or whether state is fresh, the UI should represent that uncertainty instead of pretending certainty.

## Follow-up documents

After reading this document, most contributors should continue with:

- `runtime-integration.md`
- `../reference/commands-and-actions.md`
- `../contracts/ui-action-contract.md`
