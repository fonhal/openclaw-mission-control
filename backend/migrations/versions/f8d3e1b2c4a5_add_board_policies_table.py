"""Add board_policies table.

Revision ID: f8d3e1b2c4a5
Revises: f7a2c4d6e8b1
Create Date: 2026-04-05 11:35:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "f8d3e1b2c4a5"
down_revision = "f7a2c4d6e8b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "board_policies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("board_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("policy_key", sa.String(length=255), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("config_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["boards.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("board_id", "policy_key", name="uq_board_policies_board_key"),
    )
    op.create_index("ix_board_policies_board_id", "board_policies", ["board_id"], unique=False)
    op.create_index(
        "ix_board_policies_organization_id", "board_policies", ["organization_id"], unique=False
    )
    op.create_index("ix_board_policies_policy_key", "board_policies", ["policy_key"], unique=False)
    op.alter_column("board_policies", "enabled", server_default=None)
    op.alter_column("board_policies", "config_json", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_board_policies_policy_key", table_name="board_policies")
    op.drop_index("ix_board_policies_organization_id", table_name="board_policies")
    op.drop_index("ix_board_policies_board_id", table_name="board_policies")
    op.drop_table("board_policies")
