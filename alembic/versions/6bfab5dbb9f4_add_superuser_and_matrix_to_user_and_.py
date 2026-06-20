"""add_superuser_and_matrix_to_user_and_user_permissions

Revision ID: 6bfab5dbb9f4
Revises: 0126012afe65
Create Date: 2026-06-20 12:23:42.585205
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6bfab5dbb9f4"
down_revision: Union[str, None] = "0126012afe65"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    if "user_permissions" not in tables:
        op.create_table(
            "user_permissions",
            sa.Column("user_id", sa.String(length=36), nullable=False),
            sa.Column("permission_id", sa.String(length=36), nullable=False),
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("tenant_id", sa.String(length=36), nullable=True),
            sa.Column("branch_id", sa.String(length=36), nullable=True),
            sa.Column("team_id", sa.String(length=36), nullable=True),
            sa.Column("owner_id", sa.String(length=36), nullable=True),
            sa.Column("created_by_id", sa.String(length=36), nullable=True),
            sa.Column("updated_by_id", sa.String(length=36), nullable=True),
            sa.Column("status", sa.String(length=50), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("tenant_id", "user_id", "permission_id", name="uq_tenant_user_permission"),
        )

        op.create_index("ix_user_permissions_branch_id", "user_permissions", ["branch_id"], unique=False)
        op.create_index("ix_user_permissions_owner_id", "user_permissions", ["owner_id"], unique=False)
        op.create_index("ix_user_permissions_permission_id", "user_permissions", ["permission_id"], unique=False)
        op.create_index("ix_user_permissions_status", "user_permissions", ["status"], unique=False)
        op.create_index("ix_user_permissions_team_id", "user_permissions", ["team_id"], unique=False)
        op.create_index("ix_user_permissions_tenant_id", "user_permissions", ["tenant_id"], unique=False)
        op.create_index("ix_user_permissions_user_id", "user_permissions", ["user_id"], unique=False)

    # permissions table alter skipped because previous permission migrations are inconsistent

    user_columns = [col["name"] for col in inspector.get_columns("users")]

    if "agency_name" not in user_columns:
        op.add_column("users", sa.Column("agency_name", sa.String(length=255), nullable=True))

    if "is_superuser" not in user_columns:
        op.add_column("users", sa.Column("is_superuser", sa.Boolean(), server_default="false", nullable=False))

    if "permissions_matrix" not in user_columns:
        op.add_column("users", sa.Column("permissions_matrix", sa.Text(), nullable=True))


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS user_permissions CASCADE")

    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if "users" in inspector.get_table_names():
        user_columns = [col["name"] for col in inspector.get_columns("users")]

        if "permissions_matrix" in user_columns:
            op.drop_column("users", "permissions_matrix")

        if "is_superuser" in user_columns:
            op.drop_column("users", "is_superuser")

        if "agency_name" in user_columns:
            op.drop_column("users", "agency_name")