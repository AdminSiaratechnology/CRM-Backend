"""merge all heads

Revision ID: 0126012afe65
Revises: a1b2c3d4e5f6, add_missing_user_fields_001, add_perm_tables
Create Date: 2026-06-20 11:13:24.649939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0126012afe65'
down_revision: Union[str, None] = ('a1b2c3d4e5f6', 'add_missing_user_fields_001', 'add_perm_tables')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
