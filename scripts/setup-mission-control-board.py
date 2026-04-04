#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

import requests

BASE_URL = os.environ.get('MC_BASE_URL', 'http://localhost:8000').rstrip('/')
TOKEN = os.environ.get('MC_TOKEN')
BOARD_ID = '4201eeb0-4a3c-429b-ad56-88cdf7367b3a'
TASK_CARDS = Path('/Users/vonpeter/codespace/agent-workspace/workspace-robot02/projects/openclaw-mission-control-iteration/docs/task-cards.md')

AGENTS = [
    {
        'name': 'omc Product Strategist',
        'role': 'Product Strategist Agent',
        'communication_style': 'scope-first, product-boundary-aware, concise, outcome-driven',
        'emoji': '🧭',
    },
    {
        'name': 'omc Board Leader',
        'role': 'Board Leader Agent',
        'communication_style': 'structured, conclusion-first, executable, risk-aware',
        'emoji': '📋',
    },
    {
        'name': 'omc Architect',
        'role': 'Architect Agent',
        'communication_style': 'systems-oriented, contract-first, explicit about boundaries',
        'emoji': '🏗️',
    },
    {
        'name': 'omc Builder',
        'role': 'Builder Agent',
        'communication_style': 'implementation-focused, direct, evidence-aware',
        'emoji': '🛠️',
    },
    {
        'name': 'omc Verifier',
        'role': 'Verifier Agent',
        'communication_style': 'acceptance-driven, skeptical, precise',
        'emoji': '✅',
    },
    {
        'name': 'omc Operations and Governance',
        'role': 'Operations and Governance Agent',
        'communication_style': 'safety-first, operationally grounded, audit-aware',
        'emoji': '🛡️',
    },
]

ROLE_TO_AGENT = {
    'Product Strategist': 'omc Product Strategist',
    'Board Leader': 'omc Board Leader',
    'Architect': 'omc Architect',
    'Builder': 'omc Builder',
    'Verifier': 'omc Verifier',
    'Operations and Governance': 'omc Operations and Governance',
}


def headers():
    if not TOKEN:
        raise SystemExit('MC_TOKEN is required')
    return {
        'Authorization': TOKEN if TOKEN.startswith('Bearer ') else f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }


def parse_tasks(text: str):
    tasks = []
    blocks = re.split(r'\n(?=## ITER-)', text)
    for block in blocks:
        block = block.strip()
        if not block.startswith('## ITER-'):
            continue
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        title = lines[0][3:].strip()
        meta = {}
        for line in lines[1:]:
            if line.startswith('- '):
                key, value = line[2:].split(':', 1)
                meta[key.strip()] = value.strip()
        owner = meta.get('owner', '')
        assignee_name = None
        for key, agent_name in ROLE_TO_AGENT.items():
            if key in owner:
                assignee_name = agent_name
                break
        description = (
            f"Owner: {meta.get('owner', '')}\n"
            f"Scope: {meta.get('scope', '')}\n"
            f"Output: {meta.get('output', '')}\n"
            f"Acceptance: {meta.get('acceptance', '')}\n"
            f"Estimated total tokens: {meta.get('estimated_total_tokens', '')}"
        )
        tasks.append({
            'title': title,
            'description': description,
            'priority': 'high',
            'status': 'inbox',
            'assignee_name': assignee_name,
        })
    return tasks


def get_existing_agents(session):
    r = session.get(f'{BASE_URL}/api/v1/agents', headers=headers(), timeout=30)
    r.raise_for_status()
    items = r.json().get('items', [])
    return {item['name']: item for item in items if item.get('board_id') == BOARD_ID}


def ensure_agents(session):
    existing = get_existing_agents(session)
    created = []
    for agent in AGENTS:
        if agent['name'] in existing:
            created.append(existing[agent['name']])
            continue
        payload = {
            'name': agent['name'],
            'board_id': BOARD_ID,
            'heartbeat_config': {'every': '30m', 'target': 'last', 'includeReasoning': False},
            'identity_profile': {
                'role': agent['role'],
                'communication_style': agent['communication_style'],
                'emoji': agent['emoji'],
            },
        }
        r = session.post(f'{BASE_URL}/api/v1/agents', headers=headers(), json=payload, timeout=30)
        r.raise_for_status()
        created.append(r.json())
    return {item['name']: item['id'] for item in get_existing_agents(session).values()}


def get_existing_tasks(session):
    r = session.get(f'{BASE_URL}/api/v1/boards/{BOARD_ID}/tasks?limit=200', headers=headers(), timeout=30)
    r.raise_for_status()
    return {item['title']: item for item in r.json().get('items', [])}


def ensure_tasks(session, agent_ids):
    cards = parse_tasks(TASK_CARDS.read_text())
    existing = get_existing_tasks(session)
    created = []
    for card in cards:
        if card['title'] in existing:
            continue
        payload = {
            'title': card['title'],
            'description': card['description'],
            'priority': card['priority'],
            'status': card['status'],
        }
        if card['assignee_name'] and card['assignee_name'] in agent_ids:
            payload['assigned_agent_id'] = agent_ids[card['assignee_name']]
        r = session.post(f'{BASE_URL}/api/v1/boards/{BOARD_ID}/tasks', headers=headers(), json=payload, timeout=30)
        r.raise_for_status()
        created.append(r.json())
    return created


def main():
    session = requests.Session()
    board = session.get(f'{BASE_URL}/api/v1/boards/{BOARD_ID}', headers=headers(), timeout=30)
    board.raise_for_status()
    agent_ids = ensure_agents(session)
    created_tasks = ensure_tasks(session, agent_ids)
    result = {
        'board_id': BOARD_ID,
        'agent_count': len(agent_ids),
        'created_task_count': len(created_tasks),
        'agent_names': sorted(agent_ids.keys()),
        'created_task_titles': [t['title'] for t in created_tasks],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
