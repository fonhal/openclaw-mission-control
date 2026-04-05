from __future__ import annotations

import os
from pathlib import Path

DEFAULT_TOKEN_PATH = Path.home() / '.openclaw' / 'secrets' / 'mission-control-token'


def resolve_mc_token(explicit: str | None = None) -> str:
    candidates = [
        explicit,
        os.environ.get('MC_TOKEN'),
        _read_token_file(DEFAULT_TOKEN_PATH),
    ]
    for value in candidates:
        if not value:
            continue
        token = value.strip()
        if not token:
            continue
        if token.lower().startswith('bearer '):
            return token
        return f'Bearer {token}'
    raise SystemExit(
        'Mission Control token not found. Provide MC_TOKEN or create ~/.openclaw/secrets/mission-control-token'
    )


def _read_token_file(path: Path) -> str | None:
    try:
        if not path.exists():
            return None
        value = path.read_text(encoding='utf-8').strip()
        return value or None
    except OSError:
        return None
