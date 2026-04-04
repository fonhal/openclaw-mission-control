# UI sections

## Purpose

This document describes the major UI section patterns Mission Control should use across key pages so the product stays structurally consistent as it grows.

## Audience

- frontend contributors
- product and UX collaborators
- maintainers reviewing page composition changes

## What this document does not cover

This document does not define visual styling details or final wireframes.
It focuses on structural section roles.

## Section design principles

Across major pages, Mission Control should reuse a predictable section pattern so users do not need to relearn where to look.

## Recommended section types

### Page header

Should answer:

- what page or object the user is looking at
- the most important current status
- what the highest-priority next action is, if any

### Summary section

Should provide:

- short operational summary
- key counts or highlights
- obvious attention indicators

### Primary object area

Should show the main object or object list that the page is about.
This section should dominate the page, not be visually buried.

### Related context section

Should show adjacent information needed to interpret the object, such as:

- recent activity
- related runs
- related notifications
- related node or environment context

### Actions section

Should group allowed actions in a way that makes risk and purpose clear.
High-risk actions should not visually blend with harmless navigation links.

### Diagnostics section

Should provide supporting signals such as:

- logs or log summaries
- error context
- recent changes
- timestamps and freshness signals

## Page composition expectation

Each major page should make it easy to visually distinguish:

- current status
- primary object data
- related context
- allowed actions
- supporting diagnostics

## Future expansion

As pages stabilize, this document should later include examples for:

- dashboard section layout
- list page layout
- detail page layout
- action/result panel layout
