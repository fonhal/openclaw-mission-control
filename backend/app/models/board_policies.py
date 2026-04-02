"""Board-level policy configuration for delivery governance."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field

from app.core.time import utcnow
from app.models.tenancy import TenantScoped

RUNTIME_ANNOTATION_TYPES = (datetime,)


class BoardPolicy(TenantScoped, table=True):
    """Policy toggle/config attached to a board."""

    __tablename__ = "board_policies"  # pyright: ignore[reportAssignmentType]
    __table_args__ = (
        UniqueConstraint("board_id", "policy_key", name="uq_board_policies_board_key"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    board_id: UUID = Field(foreign_key="boards.id", index=True)
    organization_id: UUID = Field(foreign_key="organizations.id", index=True)
    policy_key: str = Field(index=True)
    enabled: bool = Field(default=True)
    config_json: dict[str, object] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
