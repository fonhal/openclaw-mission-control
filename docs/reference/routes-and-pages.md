# Routes and pages

## Purpose

This document maps major Mission Control pages to their intended purpose so contributors can reason about routing and page ownership consistently.

## Audience

- frontend contributors
- product and UX collaborators
- maintainers reviewing route additions or page restructuring

## What this document does not cover

This document does not define final route implementation or nested layout code.
It is a product-facing reference for page intent.

## Page reference template

Each page entry should eventually define:

- page name
- expected route
- primary object or workflow
- page purpose
- likely actions
- related docs

## Current route and page map

The current frontend app exposes these route groups under `frontend/src/app/`.

### Overview

#### Dashboard
Expected route:
- `/dashboard`

Primary purpose:
- provide a high-level operational overview
- surface metrics, boards, agents, activity, and gateway status snapshots

Primary objects:
- dashboard metrics
- boards
- agents
- activity events
- gateway snapshots

#### Live feed
Expected route:
- `/activity`

Primary purpose:
- provide a real-time activity surface for task, board, agent, and approval events

Primary objects:
- activity events
- task comments
- board chat and command events
- approval events
- agent presence events

### Boards

#### Board groups
Expected routes:
- `/board-groups`
- `/board-groups/new`
- `/board-groups/[groupId]`

Primary purpose:
- manage and inspect board-group level organization

#### Boards
Expected routes:
- `/boards`
- `/boards/new`
- `/boards/[boardId]`

Primary purpose:
- inspect a board and work directly with tasks, approvals, board chat, activity, and custom fields

Primary objects:
- board
- task
- task comment
- approval
- board memory / chat
- board custom fields

#### Tags
Expected routes:
- `/tags`
- `/tags/add`

Primary purpose:
- inspect and manage task-tagging primitives

#### Approvals
Expected route:
- `/approvals`

Primary purpose:
- review approval-oriented workflows across boards

#### Custom fields
Expected routes:
- `/custom-fields`
- `/custom-fields/new`

Primary purpose:
- manage organization-level task custom fields

### Skills

#### Marketplace
Expected route:
- `/skills/marketplace`

#### Packs
Expected route:
- `/skills/packs`

Primary purpose:
- browse and manage skill-related inventory and installation workflows

### Administration

#### Organization
Expected route:
- `/organization`

Primary purpose:
- inspect organization-level membership and access settings

#### Gateways
Expected routes:
- `/gateways`
- `/gateways/new`
- `/gateways/[gatewayId]`

Primary purpose:
- inspect and manage gateway-connected environments

#### Agents
Expected routes:
- `/agents`
- `/agents/new`
- `/agents/[agentId]`

Primary purpose:
- inspect and manage agents

Primary actions already visible in the UI:
- create a new agent
- delete an existing agent with confirmation

## Supporting routes

Additional routes currently present include:

- `/organization`
- `/settings`
- `/invite`
- `/onboarding`
- `/sign-in/[[...rest]]`
- `/page.tsx` root landing route

## Notes for follow-up

This file should next be extended with:

- page ownership notes
- route-level permission expectations
- links to action contracts for routes with write operations
