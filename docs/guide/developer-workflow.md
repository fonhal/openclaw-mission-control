# Developer workflow

## Purpose

This document describes how contributors should approach Mission Control changes so that product structure, runtime boundaries, and action semantics stay aligned.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers reviewing structural product changes

## What this document does not cover

This document does not define:

- coding standards already covered elsewhere
- release or incident operations
- product mission and scope from first principles

Refer to `AGENTS.md`, existing repo contribution guides, and the docs structure documents for those topics.

## Default developer workflow

The default workflow should be:

1. clarify the object or workflow being changed
2. identify the affected documentation layer
3. implement the smallest coherent change
4. verify behavior and state transitions
5. update documentation if boundaries or behavior changed
6. commit the change cleanly

## Step 1: anchor on object and page boundary

Before writing code, identify:

- what object is affected
- which page owns the workflow
- whether the change is read-only or action-oriented
- whether the change crosses product, architecture, or contract boundaries

## Step 2: update the right documentation layer

Use the docs structure intentionally:

- `docs/product/` for page structure and product intent
- `docs/architecture/` for system and integration boundaries
- `docs/reference/` for user-facing reference material
- `docs/contracts/` for state and action semantics

Do not collapse these into one mixed document.

## Step 3: keep implementation scope tight

Prefer small, coherent changes that map to one clear behavior or boundary shift.
If a change affects action semantics, state eligibility, or object lifecycle, document it with the code change.

## Step 4: verify before declaring done

At minimum, confirm:

- the intended page still loads
- the object still renders correctly
- the action still behaves as intended
- failure states are still understandable

## Step 5: update docs when boundaries move

Documentation should be updated when a change affects:

- object model meaning
- page purpose or structure
- action availability or semantics
- runtime integration behavior
- user-visible wording that changes expectations

## Step 6: commit cleanly

Keep commits scoped to one coherent change whenever practical.
Avoid mixing structural docs work with unrelated frontend or backend edits unless the changes are inseparable.

## Common anti-patterns

Avoid:

- changing action behavior without updating contracts
- adding pages without documenting ownership and purpose
- mixing product intent with implementation notes in one file
- treating the UI as the system of record for runtime behavior

## Recommended reading path for contributors

1. `overview.md`
2. `../product/mission.md`
3. `../product/information-architecture.md`
4. `../architecture/system-overview.md`
5. `../architecture/runtime-integration.md`
6. the relevant reference and contract files for the change
