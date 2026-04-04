# Activity feed runtime model

## Purpose

This document describes how the current global activity page builds and maintains its feed.
It is based on the actual implementation in `frontend/src/app/activity/page.tsx`.

## Route

- `/activity`

## Page role

The activity page is currently the cross-board event visibility surface.
It does not rely on one backend endpoint alone.
Instead, it builds a unified feed by seeding historical data and then appending real-time events from multiple streams.

## Initial load model

The page first loads board inventory, then uses that to seed additional state.

Current initial loading stages include:

### 1. Load boards

The page fetches the board list in pages.
These boards become the scope for later snapshot and stream work.

### 2. Load board snapshots

For each board, the page loads a board snapshot and uses it to seed:

- task metadata
- agent snapshot events
- approval events
- board chat events

### 3. Load paged activity history

The page then loads paged activity history and maps task-related activity into feed items.

## Real-time update model

After initial load, the page opens multiple board-scoped SSE streams.

Observed stream types include:

- task stream
- approval stream
- board memory stream
- agent stream

The page therefore behaves like a fan-in aggregator: many board-local streams become one global feed.

## Feed item construction

The page maps different source objects into a normalized `FeedItem` shape.
The feed normalizes:

- event type
- actor
- actor role
- board identity
- board link
- task identity
- task title
- title
- message
- context href

## Navigation behavior

The activity page is not only a passive log.
Feed items build context-aware links that route users into:

- `/boards/[boardId]`
- `/boards/[boardId]/approvals`
- `/activity?...` fallback links

This means feed items are already acting as navigation-entry objects, not only display objects.

## Reliability model

The page includes reconnect and backoff behavior for SSE streams.
It also spaces stream connection attempts across boards, reducing burst pressure.

Observed resilience techniques include:

- exponential backoff
- delayed per-board stream connection spacing
- deduplication via seen-id tracking
- bounded feed size

## Architectural implication

The activity page is one of the clearest runtime-heavy pages in the product.
It should be documented as a streaming aggregation layer rather than just a list page.

## Documentation consequence

Future docs should continue breaking this page into:

- initial seed flow
- stream fan-in model
- normalized feed item contract
- route-mapping behavior
- reconnection and dedupe behavior
