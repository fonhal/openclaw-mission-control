# Data models

## Purpose

This document provides a working reference for the main operational object types that Mission Control is expected to display and act upon.
It is meant to support shared vocabulary and stable page design, not to serve as the final API schema source.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers discussing page and workflow boundaries

## What this document does not cover

This document does not define:

- exact database schema
- exact API payload definitions
- runtime source-of-truth semantics in full detail

## Object model principles

Mission Control should favor a stable object vocabulary across product, architecture, and UI layers.
The same object should not be described differently in different parts of the system without a strong reason.

## Candidate core objects

### Session

Represents a conversational, operational, or runtime session that the control surface may need to inspect.

Typical concerns:

- status
- recent activity
- associated runs or tasks
- last updated time
- whether intervention is needed

### Task

Represents a unit of work from the product or operational point of view.
A task may correspond to one or more execution attempts over time.

Typical concerns:

- status
- owner or initiator
- related session or board context
- retry eligibility
- visible failure summary

### Run

Represents a concrete execution attempt for a task or related action.
This is often the most useful object for debugging lifecycle and failure behavior.

Typical concerns:

- start and end timing
- execution status
- logs or error summaries
- relation to task and actor

### Job

Represents a scheduled or managed operational unit, often tied to recurring or triggered workflows.

Typical concerns:

- schedule or trigger source
- last run status
- next expected run
- whether intervention is needed

### Notification

Represents a delivery or communication outcome visible in Mission Control.

Typical concerns:

- destination or channel
- delivery status
- retry or failure context
- relation to upstream object or workflow

### Node

Represents a connected execution environment, device, or infrastructure endpoint used by the wider OpenClaw ecosystem.

Typical concerns:

- connectivity
- health
- capability availability
- last check-in or last-seen status

## Cross-object relationships

Mission Control should make the following kinds of relationships easy to understand:

- session to related task or run activity
- task to runs and resulting states
- job to recent executions
- notification to the object or action that caused it
- node to the workflows or capabilities it supports

## Documentation rule

When a new page or workflow is added, contributors should be able to answer:

- which object is primary on this page
- which related objects are secondary
- which state fields actually matter to a user decision

## Future expansion

As the product matures, this file should be extended with:

- state field summaries per object
- canonical lifecycle links
- object ownership notes
- mappings to API and contract docs
