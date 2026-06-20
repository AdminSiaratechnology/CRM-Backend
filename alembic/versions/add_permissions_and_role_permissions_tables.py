"""add_permissions_and_role_permissions_tables

Revision ID: add_perm_tables
Revises: 9e185fbb4f0c
Create Date: 2026-06-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_perm_tables'
down_revision: Union[str, None] = '9e185fbb4f0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('tenant_id', sa.String(length=36), nullable=True),
        sa.Column('branch_id', sa.String(length=36), nullable=True),
        sa.Column('team_id', sa.String(length=36), nullable=True),
        sa.Column('owner_id', sa.String(length=36), nullable=True),
        sa.Column('created_by_id', sa.String(length=36), nullable=True),
        sa.Column('updated_by_id', sa.String(length=36), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('module', sa.String(length=100), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'module', 'action', name='uq_tenant_module_action'),
        sa.Index('ix_permissions_name', 'name'),
        sa.Index('ix_permissions_tenant_id', 'tenant_id'),
        sa.Index('ix_permissions_branch_id', 'branch_id'),
        sa.Index('ix_permissions_team_id', 'team_id'),
        sa.Index('ix_permissions_owner_id', 'owner_id'),
        sa.Index('ix_permissions_status', 'status'),
    )
    
    # Create role_permissions table
    op.create_table(
        'role_permissions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('tenant_id', sa.String(length=36), nullable=True),
        sa.Column('branch_id', sa.String(length=36), nullable=True),
        sa.Column('team_id', sa.String(length=36), nullable=True),
        sa.Column('owner_id', sa.String(length=36), nullable=True),
        sa.Column('created_by_id', sa.String(length=36), nullable=True),
        sa.Column('updated_by_id', sa.String(length=36), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('role_id', sa.String(length=36), nullable=False),
        sa.Column('permission_id', sa.String(length=36), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'role_id', 'permission_id', name='uq_tenant_role_permission'),
        sa.Index('ix_role_permissions_tenant_id', 'tenant_id'),
        sa.Index('ix_role_permissions_role_id', 'role_id'),
        sa.Index('ix_role_permissions_permission_id', 'permission_id'),
        sa.Index('ix_role_permissions_branch_id', 'branch_id'),
        sa.Index('ix_role_permissions_team_id', 'team_id'),
        sa.Index('ix_role_permissions_owner_id', 'owner_id'),
        sa.Index('ix_role_permissions_status', 'status'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('role_permissions')
    op.drop_table('permissions')
