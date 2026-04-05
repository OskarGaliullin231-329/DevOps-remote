"""Initial migration: Create database tables

Revision ID: 001_initial
Revises:
Create Date: 2026-04-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create hosts table
    op.create_table(
        'hosts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('host_name', sa.String(length=255), nullable=True),
        sa.Column('surname', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create jockeys table
    op.create_table(
        'jockeys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('jockey_name', sa.String(length=255), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create races table
    op.create_table(
        'races',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('race_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create horses table
    op.create_table(
        'horses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('host_id', sa.Integer(), nullable=False),
        sa.Column('horse_name', sa.String(length=255), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create races_results table
    op.create_table(
        'races_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('horse_id', sa.Integer(), nullable=False),
        sa.Column('jockey_id', sa.Integer(), nullable=False),
        sa.Column('race_id', sa.Integer(), nullable=False),
        sa.Column('place', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['horse_id'], ['horses.id'], ),
        sa.ForeignKeyConstraint(['jockey_id'], ['jockeys.id'], ),
        sa.ForeignKeyConstraint(['race_id'], ['races.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('races_results')
    op.drop_table('horses')
    op.drop_table('races')
    op.drop_table('jockeys')
    op.drop_table('hosts')