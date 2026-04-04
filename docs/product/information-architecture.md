# Information architecture

## Purpose

This document defines how Mission Control should organize information, pages, and navigation so that operators and contributors can find critical objects and actions quickly.

## Audience

- Frontend contributors
- Product and UX collaborators
- Maintainers reviewing page structure and navigation changes

## What this document does not cover

This document does not define:

- detailed visual design
- field-level API contracts
- button-level action logic
- implementation-specific routing code

## Information architecture principles

Mission Control should follow these principles:

1. **Objects before actions**
   - Users should first understand what they are looking at.
   - Actions should be contextual, not the primary organizing principle.

2. **Overview before detail**
   - Global health and summary views should lead into object-level detail pages.

3. **High-frequency paths first**
   - Common read paths and safe actions belong in primary navigation.
   - Rare or risky workflows should be visible but not over-promoted.

4. **Group related state together**
   - A user should not need to jump across unrelated pages to understand one object.

## Recommended top-level navigation

### Dashboard

Purpose:

- provide a high-level operational snapshot
- surface urgent problems or anomalies
- point users toward the most important next drill-down path

### Sessions

Purpose:

- inspect session state and activity
- navigate into session-level context and status

### Tasks / Runs / Jobs

Purpose:

- inspect execution state
- identify failures and retry candidates
- understand lifecycle transitions for work objects

### Notifications

Purpose:

- review notification outcomes
- diagnose failed delivery or related workflow issues

### Nodes / Devices

Purpose:

- inspect node connectivity, health, and operational readiness

### Operations

Purpose:

- expose controlled operational workflows
- host lower-frequency but important system actions and diagnostics

## Page hierarchy model

### Level 1: overview and list pages

Examples:

- dashboard
- session list
- task/run/job list
- notification list
- node list

### Level 2: detail pages

Examples:

- session detail
- task detail
- run detail
- job detail
- notification detail
- node detail

### Level 3: diagnostic or support views

Examples:

- log views
- health and trace views
- operation results
- debug and workflow-specific supporting pages

## Page design checklist

Each major page should help a user answer:

- What object am I looking at?
- What is its current state?
- What changed recently?
- What can I do next?
- What can I not do right now, and why?

## To be expanded later

This document should later include:

- finalized navigation labels
- route-to-page mapping
- page ownership and dependency notes
- placement rules for high-risk actions
