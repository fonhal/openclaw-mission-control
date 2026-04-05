from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import tasks as tasks_api
from app.api.deps import ActorContext
from app.models.agents import Agent
from app.models.boards import Board
from app.models.gateways import Gateway
from app.models.organizations import Organization
from app.models.tasks import Task
from app.schemas.tasks import TaskRead, TaskUpdate


async def _make_engine() -> AsyncEngine:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.connect() as conn, conn.begin():
        await conn.run_sync(SQLModel.metadata.create_all)
    return engine


async def _make_session(engine: AsyncEngine) -> AsyncSession:
    return AsyncSession(engine, expire_on_commit=False)


async def _seed_board_task_and_agent(session: AsyncSession) -> tuple[Board, Task, Agent]:
    organization_id = uuid4()
    gateway = Gateway(
        id=uuid4(),
        organization_id=organization_id,
        name="gateway",
        url="https://gateway.local",
        workspace_root="/tmp/workspace",
    )
    board = Board(
        id=uuid4(),
        organization_id=organization_id,
        gateway_id=gateway.id,
        name="board",
        slug=f"board-{uuid4()}",
        require_approval_for_done=False,
    )
    agent = Agent(
        id=uuid4(),
        board_id=board.id,
        gateway_id=gateway.id,
        name="agent",
        status="online",
    )
    task = Task(
        id=uuid4(),
        board_id=board.id,
        title="Task",
        status="inbox",
        assigned_agent_id=agent.id,
    )

    session.add(Organization(id=organization_id, name=f"org-{organization_id}"))
    session.add(gateway)
    session.add(board)
    session.add(task)
    session.add(agent)
    await session.commit()
    return board, task, agent


@pytest.mark.asyncio
async def test_update_task_returns_governance_metadata_fields() -> None:
    engine = await _make_engine()
    try:
        async with await _make_session(engine) as session:
            _board, task, agent = await _seed_board_task_and_agent(session)

            payload = TaskUpdate(
                baseline_ref={"value": "spec://iter-005"},
                acceptance_checklist=["returns metadata", "migration applies cleanly"],
            )

            updated = await tasks_api.update_task(
                payload=payload,
                task=task,
                session=session,
                actor=ActorContext(actor_type="agent", agent=agent),
            )

            assert isinstance(updated, TaskRead)
            assert updated.baseline_ref == {"value": "spec://iter-005"}
            assert updated.acceptance_checklist == [
                "returns metadata",
                "migration applies cleanly",
            ]
            assert updated.run_safe_status == "unknown"
            assert updated.latest_policy_check_at is None
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_in_progress_transition_updates_policy_check_metadata() -> None:
    engine = await _make_engine()
    try:
        async with await _make_session(engine) as session:
            _board, task, agent = await _seed_board_task_and_agent(session)

            updated = await tasks_api.update_task(
                payload=TaskUpdate(
                    status="in_progress",
                    baseline_ref={"value": "spec://iter-005"},
                    acceptance_checklist=["ready to build"],
                ),
                task=task,
                session=session,
                actor=ActorContext(actor_type="agent", agent=agent),
            )

            assert updated.status == "in_progress"
            assert updated.run_safe_status == "ready"
            assert updated.latest_policy_check_at is not None
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_task_read_serializes_existing_policy_check_timestamp() -> None:
    engine = await _make_engine()
    try:
        async with await _make_session(engine) as session:
            _board, task, agent = await _seed_board_task_and_agent(session)
            timestamp = datetime(2026, 4, 4, 9, 0, tzinfo=UTC).replace(tzinfo=None)
            task.baseline_ref = {"value": "spec://iter-005"}
            task.acceptance_checklist = ["persist metadata"]
            task.run_safe_status = "ready"
            task.latest_policy_check_at = timestamp
            session.add(task)
            await session.commit()
            await session.refresh(task)

            updated = await tasks_api.update_task(
                payload=TaskUpdate(comment="Confirm metadata is still serialized."),
                task=task,
                session=session,
                actor=ActorContext(actor_type="agent", agent=agent),
            )

            assert updated.priority == "medium"
            assert updated.baseline_ref == {"value": "spec://iter-005"}
            assert updated.acceptance_checklist == ["persist metadata"]
            assert updated.run_safe_status == "ready"
            assert updated.latest_policy_check_at == timestamp
    finally:
        await engine.dispose()
