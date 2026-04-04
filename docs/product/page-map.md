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

## Proposed page areas

### Dashboard

Type:
- overview

Primary purpose:
- show global operational health and important entry points

Primary objects:
- summary views of sessions, tasks/runs, notifications, nodes

### Sessions

Type:
- list and detail

Primary purpose:
- inspect session state and drill into session context

Primary objects:
- session

### Tasks / Runs / Jobs

Type:
- list and detail

Primary purpose:
- inspect execution lifecycle and intervene when appropriate

Primary objects:
- task
- run
- job

### Notifications
n
Type:
- list and detail

Primary purpose:
- inspect delivery outcomes and related failures

Primary objects:
- notification

### Nodes / Devices

Type:
- list and detail

Primary purpose:
- inspect connected environments and readiness

Primary objects:
- node

### Operations

Type:
- support / controlled actions

Primary purpose:
- host diagnostic and operational workflows that do not belong in the main object pages

Primary objects:
- workflow-dependent

## Future expansion

As routes stabilize, this file should be extended with:

- final route names
- page ownership
- related contract references
- primary actions per page
