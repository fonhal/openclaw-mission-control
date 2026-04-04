# Mission

## Purpose

This document defines why Mission Control exists, what team problem it solves, and how to evaluate scope decisions.
It should be used when prioritizing features, reviewing proposals, and deciding whether a new page or workflow belongs in the product.

## Audience

- Product and technical leads
- Contributors proposing or implementing product changes
- Team members aligning on scope and priorities

## What this document does not cover

This document does not specify:

- Detailed interaction design
- Runtime integration mechanics
- API or event contracts
- Delivery timelines

## Mission statement

Mission Control exists to give the OpenClaw team a unified internal control surface where critical operational state is visible, controlled actions are explicit, and outcomes can be tracked without relying on scattered tools or tribal knowledge.

## Why we need it

Without Mission Control, important workflows tend to spread across:

- CLI commands
- multiple logs and dashboards
- session-specific context
- ad hoc team knowledge
- manual debugging paths

Mission Control reduces this fragmentation by giving the team one consistent place to observe, decide, and act.

## Primary goals

### Goal 1: unify observation

The team should be able to quickly answer:

- Is the system healthy enough for normal use?
- Which sessions, tasks, or jobs need attention?
- What failed recently?
- What is currently active?

### Goal 2: unify controlled actions

High-value operational actions should have a consistent and understandable entry point, rather than requiring people to remember one-off commands or internal shortcuts.

### Goal 3: unify object language

Mission Control should encourage a shared vocabulary around stable objects such as sessions, tasks, runs, jobs, notifications, and nodes.
This lowers communication overhead across product, engineering, and operations work.

### Goal 4: support future operational maturity

Mission Control should create a foundation for stronger governance, auditability, workflow visibility, and safer runtime interaction over time.

## Non-goals

Mission Control is not trying to:

- expose every low-level capability in the runtime
- replace all CLI and script-based workflows
- become a general-purpose external-facing SaaS product
- optimize for novelty over operational clarity

## Scope decisions

When deciding whether something belongs in Mission Control, prefer work that:

1. improves visibility into important operational state
2. reduces friction in common team workflows
3. makes action boundaries safer and more explicit
4. helps the team reason about stable objects and lifecycles
5. reduces dependency on undocumented habits and personal memory

Avoid work that primarily:

- duplicates niche tooling without improving clarity
- adds pages without anchoring them to clear objects or workflows
- expands scope faster than the team can document and maintain it

## Success criteria

Mission Control is delivering value when:

- core operational objects are easy to inspect
- common actions are understandable and controlled
- team members can explain major page boundaries consistently
- action outcomes are easier to follow than in the current tool mix
- onboarding requires less oral transfer and guesswork
