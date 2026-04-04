# Notification contract

## Purpose

This document defines the minimum contract for how Mission Control should represent notification-related outcomes and failures.

## Audience

- frontend contributors
- backend and integration contributors
- maintainers designing notification visibility and retry behavior

## What this document does not cover

This document does not define the entire delivery provider schema or every message payload detail.

## Contract goals

Mission Control should help users answer:

- what notification was attempted
- where it was intended to go
- whether delivery succeeded, failed, or is still pending
- whether follow-up is needed

## Minimum representation

A notification shown in Mission Control should make room for:

- stable identifier
- delivery target or channel summary
- current delivery outcome
- recent timing context
- related object or workflow context when available

## Delivery outcome buckets

The UI should preserve understandable buckets such as:

- pending
- sent or succeeded
- failed
- cancelled or dropped when applicable
- unknown or transitional

## Contract rules

### 1. Delivery state must not be overstated

If the system only knows that a request was accepted, the UI should not imply confirmed delivery.

### 2. Failure should be inspectable

If a delivery fails, Mission Control should surface enough context to understand whether retry or deeper debugging is needed.

### 3. Related context matters

When possible, a notification should be traceable back to the task, run, job, or workflow that produced it.
