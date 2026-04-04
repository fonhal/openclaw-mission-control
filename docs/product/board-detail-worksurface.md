# Board detail worksurface

## Purpose

This document describes the current `board detail` page as it actually exists in the frontend implementation.
It focuses on the page as a composite operator worksurface rather than a simple object-detail page.

## Route

- `/boards/[boardId]`

## Why this page matters

The board detail page is currently one of the highest-density pages in Mission Control.
It is where multiple object types and action flows converge.

Rather than only showing board metadata, it acts as the main working surface for day-to-day execution.

## Primary objects on the page

The implementation currently combines these object types on one page:

- board
- task
- task comment
- approval
- board chat / board memory
- board-level agents
- board group snapshot
- board-scoped custom field definitions and values
- tags

## Page responsibilities

The page currently handles all of the following responsibilities:

### 1. Board snapshot loading

It loads board snapshot data and uses it as the base state for the page.

### 2. Task work surface

It exposes a task-board oriented work area with:

- task list / board view
- task detail side panel behavior
- task selection from URL state
- task comments
- task create, edit, and delete flows
- task status and priority editing
- task dependency handling
- task due date and assignee editing
- task tag editing
- task custom field editing

### 3. Approval work surface

It manages board-scoped approvals and approval status transitions.

### 4. Board chat work surface

It exposes board chat / command interaction using board memory APIs.

### 5. Live feed work surface

It builds a board-local live feed that merges multiple event sources into one stream.

### 6. Agent control surface

It includes board-agent presence and control-oriented state, including pause/resume style control flows.

## URL-driven panel behavior

The page is not purely local-state driven.
It also uses URL parameters to control focus and side panels.

Current observed query parameters include:

- `taskId`
- `commentId`
- `panel`

This means the page already supports deep-linking into:

- a specific task
- a highlighted task comment
- a specific auxiliary panel such as chat

## Permission model already visible in code

The page resolves board access from organization membership and board-specific access entries.

Current read/write resolution includes:

- all boards write
- all boards read
- per-board access entries
- explicit `canRead` / `canWrite` logic

This is important because board detail is not just a view page; it gates actual mutation capability.

## Real-time model

The page is not based on one stream only.
It combines snapshot state, paged history, and streaming updates.

Current live sources include:

- board snapshot fetch
- task stream SSE
- approval stream SSE
- board memory stream SSE
- agent stream SSE
- paged activity history fetch
- paged task comments fetch

## State model takeaway

Board detail is currently a composite, stateful, real-time page with multiple side effects and mutation paths.
It should be treated in documentation as a `worksurface` instead of only a detail page.

## Documentation consequence

Future docs for this page should split concerns into:

- layout sections
- object model
- URL state contract
- mutation/action contract
- streaming/state refresh model
