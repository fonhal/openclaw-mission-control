# Feed item contract

## Purpose

This document defines the normalized feed-item concept used across Mission Control activity surfaces.
It focuses on feed items as UI-facing event objects rather than raw backend payloads.

## Why this matters

Mission Control currently has more than one activity-oriented surface.
At least two feed-oriented contexts are visible:

- global activity feed
- board-local live feed

These surfaces do not display raw source objects directly.
They map multiple source types into normalized display items.

## Feed item role

A feed item is a display-ready event object that combines:

- what happened
- who it relates to
- where it happened
- what the user can click to inspect more context

## Current source families

The current implementation already maps multiple families into feed items:

- task activity
- task comments
- board chat
- board commands
- approval events
- agent presence / update events

## Shared conceptual fields

Across current feed implementations, a normalized feed item may include:

- `id`
- `created_at`
- `event_type`
- `message`
- `agent_id`
- `actor_name`
- `actor_role`
- `board_id`
- `board_name`
- `board_href`
- `task_id`
- `task_title`
- `title`
- `context_href`
- `source_event_id`

Not every field is required for every feed surface, but the concept should remain coherent.

## Core contract expectations

### 1. Feed items are normalized, not raw

A feed item should already be suitable for rendering without each component needing to understand every upstream object type.

### 2. Feed items are context-aware

A feed item should carry enough context for the user to answer:

- what happened
- where it happened
- whose action or state this relates to
- where to click next

### 3. Feed items are navigation-capable

Feed items are not only records.
They also act as entry points into:

- board detail
- approvals context
- activity fallback context

### 4. Feed items must remain dedupe-safe

Because multiple data sources can feed the same surface, feed items need stable enough identities for deduplication.

## Board-local live feed vs global activity feed

### Board-local live feed

Characteristics:
- scoped to one board
- combines local comments, approvals, board chat, task events, and agent events
- optimized for in-context execution awareness

### Global activity feed

Characteristics:
- spans multiple boards
- builds a normalized cross-board event stream
- emphasizes actor, board, task, and context-link clarity

## Display expectations

A feed item should support rendering of:

- event label
- title
- message/body
- actor identity
- actor role when available
- board identity
- timestamp
- contextual navigation target

## Runtime expectations

Feed items may originate from:

- paged history loads
- snapshot seeding
- streaming updates

Therefore, the contract should tolerate:

- late-arriving items
- duplicate candidates
- partial source context before enrichment

## Documentation follow-up

This document should later add:

- concrete field-level required/optional guidance
- event-type mapping table
- board-local vs global feed comparison matrix
- sample feed-item payloads
