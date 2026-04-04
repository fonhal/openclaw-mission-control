# Quickstart

## Purpose

This document helps a team member get Mission Control running locally and verify that the minimum product path works.
It is optimized for the shortest path to a useful local environment, not for explaining every implementation detail.

## Audience

- developers joining the project
- contributors validating a local setup
- reviewers who need a quick sanity path before digging deeper

## What this document does not cover

This document does not define:

- full deployment strategy
- production hardening
- page-by-page product behavior
- backend or frontend internals

For those, see:

- deployment docs under `../deployment/`
- architecture docs under `../architecture/`
- product docs under `../product/`

## Prerequisites

Before starting, make sure you have:

- Node.js installed at the project-supported version
- the repository checked out locally
- the required package manager and backend toolchain available
- Docker available if you are using the compose-based flow

## Recommended fast path

### 1. Prepare environment files

At minimum, confirm the required example files are copied into usable local env files.

Typical examples include:

- root `.env`
- backend env file
- frontend env file

Use the repo examples as the base and fill in any required non-placeholder values.

## 2. Install dependencies

Use the repository-standard install flow.

Preferred entry points:

```bash
make setup
```

Or use the documented frontend/backend-specific setup flow if you are working on only one side.

## 3. Start the application

Choose one supported development path.

### Option A: Docker-based local stack

```bash
docker compose -f compose.yml --env-file .env up -d --build
```

### Option B: Faster split local loop

Use the project's documented backend and frontend local commands if you are iterating quickly.

Examples:

```bash
# backend
cd backend && uv run uvicorn app.main:app --reload --port 8000

# frontend
cd frontend && npm run dev
```

## 4. Verify minimum product path

After startup, verify at least the following:

- the frontend loads
- the backend health path responds
- the main shell or landing route renders
- at least one core list page loads without a blocking error

## Suggested minimum checks

### UI availability

Confirm the main UI opens in the browser.

### API availability

Confirm the backend health route responds successfully.

### Core object visibility

Confirm at least one important object view can load, such as a session, task, or dashboard page.

### Empty-state quality

If there is little or no data, confirm the UI still behaves clearly instead of failing silently.

## What counts as success

Quickstart is successful when a contributor can:

- start the app locally
- open the UI
- reach the backend
- load a meaningful primary page
- understand the next step without needing oral handoff

## Next reading

After quickstart, continue with:

- `overview.md`
- `operator-workflow.md`
- `developer-workflow.md`
- `../architecture/system-overview.md`
