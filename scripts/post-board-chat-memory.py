#!/usr/bin/env python3
import argparse
import json
import os

import requests

BASE_URL = os.environ.get('MC_BASE_URL', 'http://localhost:8000').rstrip('/')
TOKEN = os.environ.get('MC_TOKEN')


def headers():
    if not TOKEN:
        raise SystemExit('MC_TOKEN is required')
    return {
        'Authorization': TOKEN if TOKEN.startswith('Bearer ') else f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }


def main():
    parser = argparse.ArgumentParser(description='Post a board chat message through board memory API')
    parser.add_argument('board_id')
    parser.add_argument('content')
    parser.add_argument('--source', default='Sage API')
    parser.add_argument('--tag', action='append', default=[])
    args = parser.parse_args()

    tags = ['chat', *args.tag]
    payload = {'content': args.content, 'tags': tags, 'source': args.source}
    r = requests.post(f'{BASE_URL}/api/v1/boards/{args.board_id}/memory', headers=headers(), json=payload, timeout=30)
    r.raise_for_status()
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
