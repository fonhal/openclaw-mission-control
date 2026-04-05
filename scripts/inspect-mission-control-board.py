#!/usr/bin/env python3
import argparse
import json
import os
from collections import Counter

import requests

from _mc_token import resolve_mc_token

BASE_URL = os.environ.get('MC_BASE_URL', 'http://localhost:8000').rstrip('/')


def headers():
    return {'Authorization': resolve_mc_token()}


def get(session, path):
    r = session.get(f'{BASE_URL}{path}', headers=headers(), timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    parser = argparse.ArgumentParser(description='Inspect Mission Control board state')
    parser.add_argument('board_id')
    parser.add_argument('--task-limit', type=int, default=200)
    parser.add_argument('--activity-limit', type=int, default=20)
    parser.add_argument('--chat-limit', type=int, default=10)
    args = parser.parse_args()

    s = requests.Session()
    board = get(s, f'/api/v1/boards/{args.board_id}')
    tasks = get(s, f'/api/v1/boards/{args.board_id}/tasks?limit={args.task_limit}')['items']
    activity = get(s, f'/api/v1/activity?limit={args.activity_limit}')['items']
    comments = get(s, f'/api/v1/activity/task-comments?limit={args.activity_limit}')['items']
    chat = get(s, f'/api/v1/boards/{args.board_id}/memory?is_chat=true&limit={args.chat_limit}')['items']

    status_counts = Counter(t.get('status') or 'unknown' for t in tasks)
    priority_counts = Counter(t.get('priority') or 'unknown' for t in tasks)
    active_lane = [t for t in tasks if t.get('status') == 'in_progress']
    assigned_unblocked = [t for t in tasks if t.get('assigned_agent_id') and not t.get('depends_on_task_ids')]
    blocked = [t for t in tasks if t.get('depends_on_task_ids')]
    heartbeat_events = [a for a in activity if a.get('event_type') == 'agent.heartbeat' and a.get('board_id') == args.board_id]
    board_comments = [c for c in comments if c.get('board_id') == args.board_id]

    result = {
        'board': {
            'id': board['id'],
            'name': board['name'],
            'description': board.get('description'),
            'objective': board.get('objective'),
        },
        'summary': {
            'task_count': len(tasks),
            'status_counts': dict(status_counts),
            'priority_counts': dict(priority_counts),
            'active_lane_count': len(active_lane),
            'blocked_task_count': len(blocked),
            'assigned_unblocked_count': len(assigned_unblocked),
            'recent_board_comment_count': len(board_comments),
            'recent_heartbeat_count': len(heartbeat_events),
        },
        'active_lane': [
            {
                'id': t['id'],
                'title': t['title'],
                'priority': t.get('priority'),
                'assigned_agent_id': t.get('assigned_agent_id'),
            }
            for t in active_lane
        ],
        'blocked_tasks': [
            {
                'id': t['id'],
                'title': t['title'],
                'depends_on_task_ids': t.get('depends_on_task_ids', []),
                'status': t.get('status'),
                'priority': t.get('priority'),
            }
            for t in blocked[:20]
        ],
        'assigned_unblocked': [
            {
                'id': t['id'],
                'title': t['title'],
                'status': t.get('status'),
                'priority': t.get('priority'),
                'assigned_agent_id': t.get('assigned_agent_id'),
            }
            for t in assigned_unblocked[:20]
        ],
        'recent_board_comments': [
            {
                'created_at': c.get('created_at'),
                'agent_name': c.get('agent_name'),
                'task_title': c.get('task_title'),
                'message_head': (c.get('message') or '')[:240],
            }
            for c in board_comments[:10]
        ],
        'recent_chat_memory': [
            {
                'created_at': m.get('created_at'),
                'source': m.get('source'),
                'content_head': (m.get('content') or '')[:240],
            }
            for m in chat[:10]
        ],
        'diagnosis_hints': [
            'If active_lane_count is 0 and recent_heartbeat_count > 0, expect heartbeat-driven status/comment noise.',
            'If blocked_task_count is high and only one assigned_unblocked task exists, the board likely lacks an explicit execution lane.',
            'If recent chat memory grows but task status does not move, the board may be discussing without activating work.',
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
