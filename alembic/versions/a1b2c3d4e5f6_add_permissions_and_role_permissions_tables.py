"""add permissions and role permissions tables

Revision ID: a1b2c3d4e5f6
Revises: 9e185fbb4f0c
Create Date: 2026-06-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '9e185fbb4f0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check and update permissions table
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('permissions')]
    
    # Add new columns if they don't exist
    if 'module' not in existing_columns:
        op.add_column('permissions', sa.Column('module', sa.String(length=100), nullable=True))
    if 'action' not in existing_columns:
        op.add_column('permissions', sa.Column('action', sa.String(length=100), nullable=True))
    if 'name' not in existing_columns:
        op.add_column('permissions', sa.Column('name', sa.String(length=255), nullable=True))
    if 'description' not in existing_columns:
        op.add_column('permissions', sa.Column('description', sa.Text(), nullable=True))
    
    # Add unique constraint if it doesn't exist
    constraints = inspector.get_unique_constraints('permissions')
    constraint_names = [c['name'] for c in constraints]
    if 'uq_tenant_module_action' not in constraint_names:
        try:
            op.create_unique_constraint('uq_tenant_module_action', 'permissions', ['tenant_id', 'module', 'action'])
        except Exception:
            pass
    
    # Add indexes if they don't exist
    indexes = [idx['name'] for idx in inspector.get_indexes('permissions')]
    if 'ix_permissions_name' not in indexes:
        op.create_index('ix_permissions_name', 'permissions', ['name'])
    
    # Create role_permissions table if it doesn't exist
    if 'role_permissions' not in inspector.get_table_names():
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
