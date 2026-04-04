# Rollback

## Purpose

This document describes the minimum rollback thinking for Mission Control releases and operational changes.
It is intended to reduce hesitation and ambiguity when a recent change needs to be backed out quickly.

## Audience

- maintainers
- release reviewers
- contributors responsible for recovering from a bad change

## What this document does not cover

This document does not replace incident response or environment-specific deployment instructions.
It focuses on rollback principles and checks.

## Rollback goals

A rollback path should help the team answer:

- what needs to be reverted
- how urgent the rollback is
- what user-visible risk remains if rollback is delayed
- what to verify after rollback

## Rollback checklist

### 1. Identify the failing scope

Confirm:

- which change likely caused the issue
- whether the issue is frontend-only, integration-related, or broader
- whether the impact is read-path only or action-path related

### 2. Choose the rollback unit

Prefer rolling back the smallest coherent change that restores safe behavior.
Avoid mixing unrelated reversions unless necessary for recovery.

### 3. Re-verify critical paths

After rollback, verify:

- the app loads
- the main operator path still works
- affected actions no longer exhibit the broken behavior
- state is presented coherently

### 4. Record follow-up

After rollback, capture:

- what was reverted
- why it was reverted
- what still needs investigation
- whether documentation needs to be updated

## Rollback guidance

If a recent change breaks action safety, object visibility, or high-frequency pages, rollback should generally be favored over prolonged live debugging in the primary environment.
