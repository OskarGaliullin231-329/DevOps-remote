"""Initial migration: Create database tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-03 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create owners table
    op.create_table(
        'owners',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create jockeys table
    op.create_table(
        'jockeys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create horses table
    op.create_table(
        'horses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create races table
    op.create_table(
        'races',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create race_entries table (many-to-many with placement)
    op.create_table(
        'race_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('race_id', sa.Integer(), nullable=False),
        sa.Column('jockey_id', sa.Integer(), nullable=False),
        sa.Column('horse_id', sa.Integer(), nullable=False),
        sa.Column('place', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['horse_id'], ['horses.id'], ),
        sa.ForeignKeyConstraint(['jockey_id'], ['jockeys.id'], ),
        sa.ForeignKeyConstraint(['race_id'], ['races.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('race_id', 'jockey_id', 'horse_id', name='unique_race_entry')
    )


def downgrade() -> None:
    op.drop_table('race_entries')
    op.drop_table('races')
    op.drop_table('horses')
    op.drop_table('jockeys')
    op.drop_table('owners')
