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

## Initial page map

### Dashboard

Expected route:
- to be confirmed

Primary purpose:
- provide a high-level operational overview

Primary objects:
- summary state across sessions, tasks/runs, notifications, and nodes

### Sessions

Expected route:
- to be confirmed

Primary purpose:
- inspect session lists and open session details

Primary objects:
- session

### Session detail

Expected route:
- to be confirmed

Primary purpose:
- inspect a single session’s current state and related context

Primary objects:
- session

### Tasks / Runs / Jobs

Expected route:
- to be confirmed

Primary purpose:
- inspect execution-oriented objects and identify intervention points

Primary objects:
- task
- run
- job

### Notifications

Expected route:
- to be confirmed

Primary purpose:
- inspect delivery outcomes and related context

Primary objects:
- notification

### Nodes / Devices

Expected route:
- to be confirmed

Primary purpose:
- inspect connectivity and readiness of connected environments

Primary objects:
- node

### Operations

Expected route:
- to be confirmed

Primary purpose:
- host controlled operational and diagnostic workflows that do not belong on a core object page

## Future expansion

As the product becomes more concrete, this file should add:

- actual route paths
- page ownership notes
- route guard or permission notes
- main action entry points per page
