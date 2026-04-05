# Agent roles overview

## Purpose

This document defines the proposed agent role system for OpenClaw Mission Control.
It focuses only on agent roles and their responsibilities.
It does not define permissions, approval rules, page routing, or workflow state machines.

## Why this exists

Mission Control is not a generic software project tracker.
It is a control surface for planning, delivery coordination, governance, and runtime operations.
Because of that, its agent system should not be modeled only as technical job titles.
It should be modeled around responsibility and decision boundaries.

## Design principle

Agent roles should answer these questions clearly:

- what problem this agent is responsible for solving
- what kind of output this agent is expected to produce
- what this agent should decide
- what this agent should not decide
- how this agent hands work to the next role

## Proposed core agent roles

The proposed v1 model uses six core agent roles.
These roles are intentionally responsibility-oriented instead of narrowly technical.

1. Product Strategist Agent
2. Board Leader Agent
3. Architect Agent
4. Builder Agent
5. Verifier Agent
6. Operations and Governance Agent

## Role summaries

### Product Strategist Agent

Purpose:
- decide what should be built, why it matters, and what success means

Primary responsibilities:
- define the problem statement
- define scope and non-scope
- judge whether a request belongs in Mission Control
- propose MVP versus later-phase delivery
- define success criteria and priority recommendations

Should not:
- jump straight into implementation details
- replace architecture work
- take over detailed page or system design
- bypass explicit product tradeoff discussion

Typical outputs:
- problem statement
- goal and scope summary
- success criteria
- MVP proposal
- risk and tradeoff notes

### Board Leader Agent

Purpose:
- turn goals into executable, trackable, and reviewable work

Primary responsibilities:
- break goals into concrete tasks
- assign a clear owner to each task
- define inputs, outputs, and acceptance criteria
- make blockers visible
- drive work toward review and closure

Should not:
- personally absorb all execution work
- throw vague tasks to builders
- override technical decisions without cause

Typical outputs:
- task breakdown
- task templates
- owner assignment
- acceptance criteria
- blocker summary
- next-step recommendation

### Architect Agent

Purpose:
- define stable system structure, object boundaries, and integration logic

Primary responsibilities:
- define core objects and relationships
- define module boundaries
- define what belongs to UI, backend, and integration layers
- shape contracts between visible product behavior and backend/runtime behavior
- protect long-term maintainability and conceptual clarity

Should not:
- decide product value in isolation
- replace the builder role
- drift into abstract architecture without delivery consequence

Typical outputs:
- object model
- boundary decisions
- data flow description
- contract proposal
- architecture notes

### Builder Agent

Purpose:
- implement the agreed design and produce working outputs

Primary responsibilities:
- build the required code, UI, integration, or documentation artifacts
- keep implementation aligned with task scope and contract expectations
- provide implementation notes and evidence
- surface technical risk during execution

Should not:
- silently expand scope
- rewrite product goals while implementing
- claim completion without verification evidence

Typical outputs:
- code changes
- implementation notes
- test results
- artifact links
- delivery summary

### Verifier Agent

Purpose:
- determine whether the work actually meets the stated acceptance bar

Primary responsibilities:
- validate against acceptance criteria
- inspect evidence and behavior
- decide whether work is ready for acceptance or should return for rework
- identify missing coverage or unresolved risk

Should not:
- redefine requirements casually
- replace the builder role
- confuse partial evidence with acceptance

Typical outputs:
- verification result
- acceptance notes
- failure findings
- regression concerns
- go / no-go conclusion

### Operations and Governance Agent

Purpose:
- evaluate operational safety, governance impact, auditability, and runtime consequences

Primary responsibilities:
- identify runtime and operational risk
- judge whether a change affects safety, observability, recoverability, or control boundaries
- identify where governance constraints are needed
- review how the system behaves under real operational conditions

Should not:
- take over product scoping
- implement everything directly
- reject all change by default

Typical outputs:
- operational risk notes
- governance concerns
- observability recommendations
- recovery and control notes
- runtime impact assessment

## Recommended interaction pattern

These roles are intended to form a chain of responsibility:

1. Product Strategist Agent defines the problem and success bar
2. Board Leader Agent turns that into executable work
3. Architect Agent defines stable structure and boundaries
4. Builder Agent implements the result
5. Verifier Agent validates whether the work is truly done
6. Operations and Governance Agent reviews runtime and governance consequences across the lifecycle

The Operations and Governance Agent should not necessarily run only at the end.
It may review proposals, designs, and implementation plans earlier when operational risk is likely.

## Why this model is preferred

This model is preferred over a purely technical role split because Mission Control is itself a coordination and control product.
A frontend-only or backend-only role model misses important responsibilities such as:

- deciding whether a request belongs in the product
- making work executable before implementation starts
- separating acceptance from implementation
- reviewing runtime and governance consequences explicitly

## Role templates

Individual templates for each role are stored in:

- `docs/architecture/templates/agent-product-strategist.md`
- `docs/architecture/templates/agent-board-leader.md`
- `docs/architecture/templates/agent-architect.md`
- `docs/architecture/templates/agent-builder.md`
- `docs/architecture/templates/agent-verifier.md`
- `docs/architecture/templates/agent-operations-governance.md`

Each template is intended to be used as a role-specific drafting or instruction baseline for future agent setup and iteration.
