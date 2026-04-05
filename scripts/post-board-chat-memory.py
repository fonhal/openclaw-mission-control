#!/usr/bin/env python3
import argparse
import json
import os

import requests

from _mc_token import resolve_mc_token

BASE_URL = os.environ.get('MC_BASE_URL', 'http://localhost:8000').rstrip('/')


def headers():
    token = resolve_mc_token()
    return {
        'Authorization': token,
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
