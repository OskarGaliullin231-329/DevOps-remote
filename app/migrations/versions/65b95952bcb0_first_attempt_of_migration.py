"""first attempt of migration

Revision ID: 65b95952bcb0
Revises: 001_initial
Create Date: 2026-04-05 02:35:02.935543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65b95952bcb0'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('horses', sa.Column('age', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('horses', 'age')
