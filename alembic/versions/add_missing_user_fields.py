"""add_missing_user_fields

Revision ID: add_missing_user_fields_001
Revises: 9e185fbb4f0c
Create Date: 2026-06-18 14:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_missing_user_fields_001'
down_revision: Union[str, None] = '9e185fbb4f0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add missing user profile fields."""
    op.add_column('users', sa.Column('manager_id', sa.String(length=36), nullable=True))
    op.add_column('users', sa.Column('login_access', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('users', sa.Column('gps_access', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('monthly_target', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_users_manager_id'), 'users', ['manager_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_manager_id'), table_name='users')
    op.drop_column('users', 'monthly_target')
    op.drop_column('users', 'gps_access')
    op.drop_column('users', 'login_access')
    op.drop_column('users', 'manager_id')
