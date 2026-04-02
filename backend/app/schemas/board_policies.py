"""Schemas for board policy configuration and task validation."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

RUNTIME_ANNOTATION_TYPES = (datetime, UUID)


class BoardPolicyBase(SQLModel):
    """Common board policy fields."""

    policy_key: str
    enabled: bool = True
    config_json: dict[str, object] = Field(default_factory=dict)


class BoardPolicyRead(BoardPolicyBase):
    """Board policy returned by APIs."""

    id: UUID
    board_id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime


class TaskPolicyViolation(SQLModel):
    """Structured policy violation payload."""

    policy: str
    message: str


class TaskRunSafeValidation(SQLModel):
    """Result of task run-safe validation."""

    ok: bool
    status: str
    violations: list[TaskPolicyViolation] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
