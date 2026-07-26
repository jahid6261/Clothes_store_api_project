"""Move product images to variants

Revision ID: 34cb28fd7c7c
Revises: 7ce14b5499ac
Create Date: 2026-07-26 06:36:20.230558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34cb28fd7c7c'
down_revision: Union[str, Sequence[str], None] = '7ce14b5499ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add variant_id column first
    op.add_column(
        'product_images',
        sa.Column('variant_id', sa.Integer(), nullable=True)
    )

    # Remove old product relation
    op.drop_constraint(
        op.f('product_images_product_id_fkey'),
        'product_images',
        type_='foreignkey'
    )

    op.drop_column(
        'product_images',
        'product_id'
    )

    # Add new variant relation
    op.create_foreign_key(
        'product_images_variant_id_fkey',
        'product_images',
        'product_variants',
        ['variant_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'product_images_variant_id_fkey',
        'product_images',
        type_='foreignkey'
    )

    op.add_column(
        'product_images',
        sa.Column('product_id', sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        op.f('product_images_product_id_fkey'),
        'product_images',
        'products',
        ['product_id'],
        ['id'],
        ondelete='CASCADE'
    )

    op.drop_column(
        'product_images',
        'variant_id'
    )