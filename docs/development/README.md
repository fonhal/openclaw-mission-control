# Development

This section is for contributors developing Mission Control locally.

## Recommended workflow (fast loop)

Run Postgres in Docker, run backend + frontend on your host.

### 1) Start Postgres

From repo root:

```bash
cp .env.example .env
docker compose -f compose.yml --env-file .env up -d db
```

### 2) Run the backend (dev)

```bash
cd backend
cp .env.example .env

uv sync --extra dev
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify:

```bash
curl -f http://localhost:8000/healthz
```

### 3) Run the frontend (dev)

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000.

## Current product development focus

The current expansion focus is to evolve Mission Control from an operations/control-plane dashboard into an AI-native delivery system with stronger planning and governance.

Recommended reading order for contributors working on this initiative:

1. [Mission Control Expansion Roadmap](../architecture/mission-control-expansion-roadmap.md)
2. [Phase 1 Delivery Governance Blueprint](../architecture/phase-1-delivery-governance-blueprint.md)
3. [Architecture index](../architecture/README.md)

These docs describe:

- product positioning
- roadmap phases
- Phase 1 implementation scope
- required backend/frontend changes
- suggested DEV task split

## Useful repo-root commands

```bash
make help
make setup
make check
```

- `make setup`: sync backend + frontend deps
- `make check`: lint + typecheck + tests + build (closest CI parity)

## Related docs

- [Testing](../testing/README.md)
- [Release checklist](../release/README.md)
- [Docs home](../README.md)
