"""Add task governance metadata columns.

Revision ID: f7a2c4d6e8b1
Revises: e3a1b2c4d5f6
Create Date: 2026-04-04 17:38:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "f7a2c4d6e8b1"
down_revision = "e3a1b2c4d5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add governance metadata columns to tasks."""
    op.add_column("tasks", sa.Column("baseline_ref", sa.JSON(), nullable=True))
    op.add_column("tasks", sa.Column("acceptance_checklist", sa.JSON(), nullable=True))
    op.add_column(
        "tasks",
        sa.Column("run_safe_status", sa.String(length=255), nullable=False, server_default="unknown"),
    )
    op.add_column("tasks", sa.Column("latest_policy_check_at", sa.DateTime(), nullable=True))
    op.create_index(
        "ix_tasks_run_safe_status",
        "tasks",
        ["run_safe_status"],
        unique=False,
    )
    op.alter_column("tasks", "run_safe_status", server_default=None)


def downgrade() -> None:
    """Remove governance metadata columns from tasks."""
    op.drop_index("ix_tasks_run_safe_status", table_name="tasks")
    op.drop_column("tasks", "latest_policy_check_at")
    op.drop_column("tasks", "run_safe_status")
    op.drop_column("tasks", "acceptance_checklist")
    op.drop_column("tasks", "baseline_ref")
