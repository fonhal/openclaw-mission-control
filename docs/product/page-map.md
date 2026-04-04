# Page map

## Purpose

This document provides a simple map of the main page areas Mission Control is expected to expose.
It helps the team reason about page ownership, object focus, and where users should go for common workflows.

## Audience

- frontend contributors
- product and UX collaborators
- maintainers reviewing page additions or navigation changes

## What this document does not cover

This document does not define:

- final route paths
- detailed wireframes
- implementation details
- fine-grained action contracts

## Page map structure

Each page area should answer:

- what object or workflow it centers on
- what the user is trying to do there
- whether it is overview, detail, or support

## Current page areas based on the frontend app

### Dashboard

Type:
- overview

Primary purpose:
- show operational summary, system signals, and major drill-down links

Primary objects:
- dashboard metrics
- boards
- agents
- activity events
- gateway status snapshots

### Live feed

Type:
- overview / streaming activity page

Primary purpose:
- show recent and live activity across boards, tasks, approvals, chats, and agents

Primary objects:
- activity events
- task comments
- board chat and command events
- approval events
- agent presence

### Boards area

Type:
- list and detail cluster

Primary purpose:
- manage board groups, boards, tags, approvals, and custom fields

Primary objects:
- board group
- board
- task
- approval
- tag
- custom field

### Board detail

Type:
- high-interaction detail page

Primary purpose:
- central work surface for a board, combining task board, board chat, approvals, activity context, and task field editing

Primary objects:
- board
- task
- task comment
- approval
- board memory

### Skills area

Type:
- list / management area

Primary purpose:
- expose marketplace and pack-level skill workflows

Primary objects:
- marketplace skill
- skill pack

### Administration area

Type:
- list and detail cluster

Primary purpose:
- manage organization settings, gateways, and agents

Primary objects:
- organization membership
- gateway
- agent

## Page ownership takeaway

The current product is more board-centric and administration-centric than the earlier abstract model suggested.
It is not primarily organized around sessions, notifications, and nodes at the top level of navigation.
Those concepts may still matter architecturally, but the current visible page system centers more on:

- boards and approvals
- agents and gateways
- live activity
- organization administration

## Future expansion

This file should next add:

- page-level action summaries
- per-page section breakdowns
- page-to-contract references for high-risk actions
