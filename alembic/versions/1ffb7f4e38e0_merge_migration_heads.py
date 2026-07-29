"""merge migration heads

Revision ID: 1ffb7f4e38e0
Revises: 0a2aab7072e6, 34cb28fd7c7c
Create Date: 2026-07-26 16:54:45.550593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ffb7f4e38e0'
down_revision: Union[str, Sequence[str], None] = ('0a2aab7072e6', '34cb28fd7c7c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
