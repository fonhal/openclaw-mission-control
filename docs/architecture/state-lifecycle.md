# State lifecycle

## Purpose

This document describes how Mission Control should reason about lifecycle-oriented operational state across its core objects.
It is intended to align list views, detail views, and action eligibility with the same lifecycle model.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers working on stateful workflows

## Scope

This document is a cross-object lifecycle overview.
Detailed state rules for individual object types should live in contract documents.

## Lifecycle thinking

Mission Control should treat state as more than a single label.
A useful lifecycle view usually needs to communicate:

- current phase
- recency
- whether the state is stable or still changing
- whether the object needs attention
- whether a follow-up action is allowed

## Common lifecycle phases

Across objects, Mission Control may need to represent phases such as:

- waiting or pending
- active or running
- idle or quiet
- succeeded or completed
- failed or problematic
- cancelled
- transitional or unknown

## UI implications

Lifecycle state should influence:

- badge wording
- sort and prioritization behavior
- attention highlighting
- action availability
- refresh expectations

## Cross-document relationship

Use this document as the high-level lifecycle reference, and use object-specific contract docs for:

- session state details
- task/run state details
- future job or notification state details
