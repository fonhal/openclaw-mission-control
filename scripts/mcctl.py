#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable
DEFAULT_BASE_URL = os.environ.get("MC_BASE_URL", "http://localhost:8000")

COMMANDS = {
    "inspect": SCRIPT_DIR / "inspect-mission-control-board.py",
    "chat": SCRIPT_DIR / "post-board-chat-memory.py",
    "setup-board": SCRIPT_DIR / "setup-mission-control-board.py",
    "update-tasks": SCRIPT_DIR / "update-mission-control-board-tasks.py",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mission Control API unified entrypoint",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Mission Control backend base url (default: %(default)s)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect board state")
    inspect_parser.add_argument("board_id")
    inspect_parser.add_argument("--task-limit", type=int)
    inspect_parser.add_argument("--activity-limit", type=int)
    inspect_parser.add_argument("--chat-limit", type=int)

    chat_parser = subparsers.add_parser("chat", help="Post a board chat message")
    chat_parser.add_argument("board_id")
    chat_parser.add_argument("content")
    chat_parser.add_argument("--source")
    chat_parser.add_argument("--tag", action="append", default=[])

    subparsers.add_parser(
        "setup-board",
        help="Run the validated board setup script with repo defaults",
    )
    subparsers.add_parser(
        "update-tasks",
        help="Run the validated bulk task update script with repo defaults",
    )

    return parser


def run_script(script: Path, base_url: str, extra_args: list[str]) -> int:
    env = os.environ.copy()
    env["MC_BASE_URL"] = base_url
    cmd = [PYTHON, str(script), *extra_args]
    return subprocess.call(cmd, env=env)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "inspect":
        extra_args = [args.board_id]
        if args.task_limit is not None:
            extra_args += ["--task-limit", str(args.task_limit)]
        if args.activity_limit is not None:
            extra_args += ["--activity-limit", str(args.activity_limit)]
        if args.chat_limit is not None:
            extra_args += ["--chat-limit", str(args.chat_limit)]
        return run_script(COMMANDS["inspect"], args.base_url, extra_args)

    if args.command == "chat":
        extra_args = [args.board_id, args.content]
        if args.source:
            extra_args += ["--source", args.source]
        for tag in args.tag:
            extra_args += ["--tag", tag]
        return run_script(COMMANDS["chat"], args.base_url, extra_args)

    if args.command == "setup-board":
        return run_script(COMMANDS["setup-board"], args.base_url, [])

    if args.command == "update-tasks":
        return run_script(COMMANDS["update-tasks"], args.base_url, [])

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
