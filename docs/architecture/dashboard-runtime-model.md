# Dashboard runtime model

## Purpose

This document describes how the current dashboard page behaves as a runtime aggregation surface.
It is based on the actual frontend implementation rather than a hypothetical dashboard design.

## Route

- `/dashboard`

## Page role

The dashboard is currently a polling-based operational summary page.
It aggregates signals from several APIs and turns them into summary cards, status blocks, approval lists, session summaries, and recent activity.

## Main data sources

The current page pulls from:

- boards list API
- agents list API
- dashboard metrics API
- activity list API
- gateway status API

## Refresh model

The dashboard is not built around SSE.
It currently relies on repeated polling.

Observed refresh intervals:

- boards: 30s
- agents: 15s
- dashboard metrics: 15s
- activity: 15s
- gateway statuses: 15s

## Main UI sections

### Top metric cards

The page shows top-level cards for:

- online agents
- tasks in progress
- error rate
- completion speed

### Summary blocks

The page builds structured status blocks for:

- workload
- throughput
- gateway health

### Pending approvals section

This section surfaces pending approval items and links users toward the global approvals page or board-specific approvals pages.

### Sessions section

The sessions area is derived indirectly from gateway status payloads rather than from a dedicated session page model.
It merges gateway session lists and main session information into a single summary list.

### Recent activity section

The dashboard only shows a shortened recent-activity slice and routes the user into `/activity` or board-related contexts for deeper inspection.

## Runtime characteristics

The dashboard currently behaves as:

- a read-heavy page
- a many-source aggregation page
- a frequent polling page
- a summary-to-drilldown page

It is not the primary place for detailed mutation workflows.

## Architectural implication

If dashboard complexity continues to grow, the code and docs should increasingly separate:

- source acquisition
- metric derivation
- gateway/session aggregation
- activity row navigation mapping
- presentation-only components

## Documentation consequence

Dashboard documentation should continue to describe:

- data-source composition
- polling cadence
- summary-vs-detail boundaries
- drill-down destinations
