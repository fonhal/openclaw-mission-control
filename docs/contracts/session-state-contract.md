# Session state contract

## Purpose

This document defines the expected contract for how Mission Control represents and reasons about session state.
It is intended to prevent drift between page behavior, contributor assumptions, and runtime-facing state interpretation.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers reviewing state-driven UI behavior

## What this document does not cover

This document does not define:

- exact runtime payloads for every session source
- every possible session subtype in the wider ecosystem
- full API schema references

## Contract goals

Mission Control should represent session state in a way that helps users answer:

- is this session active, idle, finished, or problematic
- does it require attention
- what changed recently
- can I perform any supported action from here

## Minimum session representation

At minimum, a session representation used in the UI should make room for:

- stable identifier
- current status or lifecycle phase
- recency signal such as updated time or last activity
- summary context useful for list and detail views
- action eligibility hints when relevant

## State categories

The exact backend values may evolve, but the UI contract should preserve understandable buckets such as:

### Active

Meaning:
- work or interaction is currently ongoing, or the session is recently active enough to be treated as live

Expected UI behavior:
- show it as current or hot
- make recency visible
- avoid implying completion

### Idle

Meaning:
- the session exists and may still matter, but there is no clear sign of current activity

Expected UI behavior:
- show that it is quiet, not broken
- avoid treating lack of current activity as an error

### Completed

Meaning:
- the session has reached a natural end or no longer requires active tracking

Expected UI behavior:
- make completion recognizable
- keep history discoverable

### Problematic

Meaning:
- the session is blocked, errored, or otherwise requires special attention

Expected UI behavior:
- draw attention clearly
- provide a useful next step such as opening detail or related diagnostics

## Contract rules

### 1. The UI must not overstate certainty

If the integration layer cannot confidently determine a final state, the UI should not present a stronger state than the system actually knows.

### 2. Recency matters

Session status should be interpreted alongside recency. An "active"-like label without recent activity may be misleading.

### 3. Attention state should be visible

Mission Control should make it easy to tell whether a session likely needs human attention.

### 4. Session list and detail views should align
n
The same session should not appear healthy in one place and problematic in another without an explainable reason.

## Future expansion

This file should later capture:

- state-to-badge mapping
- list vs detail state rendering rules
- refresh behavior expectations
- action eligibility tied to session state
