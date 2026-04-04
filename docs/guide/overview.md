# Mission Control overview

## Purpose

This document explains what OpenClaw Mission Control is, what it is for, and how the team should think about its scope.
It is the starting point for contributors and operators who need a shared mental model before reading product, architecture, or contract documents.

## Audience

- Team members using Mission Control in day-to-day operations
- Developers contributing frontend, backend, or integration changes
- Maintainers aligning product scope and system boundaries

## What this document does not cover

This document does not define:

- Detailed page layouts
- API payloads and schemas
- Fine-grained UI action behavior
- Release and incident procedures

Refer to the following instead:

- Product intent and page structure: `../product/`
- System boundaries and runtime integration: `../architecture/`
- Action and state rules: `../contracts/`
- Command and object references: `../reference/`

## What Mission Control is

OpenClaw Mission Control is the internal operations console for OpenClaw environments.
Its job is to provide a unified place to observe important runtime objects, perform controlled actions, and understand what happened across the system.

Mission Control should be treated as:

- An observation surface for key operational state
- An action surface for controlled, high-value workflows
- A coordination surface for team-level shared understanding

## What Mission Control is not

Mission Control is not:

- A replacement for the OpenClaw runtime itself
- A one-to-one visual copy of every CLI capability
- An unbounded admin panel for every possible workflow
- The source of truth for all runtime state

It should stay focused on high-value team workflows with clear boundaries.

## Core concepts

### Objects

Mission Control should organize information around stable operational objects, such as:

- sessions
- tasks
- runs
- jobs
- notifications
- nodes

These objects should anchor page structure, state rendering, and action design.

### Actions

Mission Control does not only display state. It also exposes controlled actions, such as:

- refresh state
- open details
- inspect logs
- retry a failed execution
- cancel an eligible execution
- trigger approved operational workflows

Each action must have a clear boundary, side-effect model, and feedback path.

### State

State in Mission Control must help answer:

- what is happening now
- what just happened
- whether action is allowed
- what changed after an action

### Boundaries

Mission Control must clearly separate:

- UI responsibilities
- integration/backend responsibilities
- runtime responsibilities
- read-only workflows vs write workflows
- low-risk actions vs high-risk actions

## Recommended reading order

1. This document
2. `../product/mission.md`
3. `../product/information-architecture.md`
4. `../architecture/system-overview.md`
5. `../architecture/runtime-integration.md`
6. The relevant reference or contract file for the task at hand

## Current documentation priority

At this stage, the documentation should optimize for four things:

1. Shared team understanding
2. Stable page and object boundaries
3. Safe action design
4. Low-friction onboarding for contributors and operators
