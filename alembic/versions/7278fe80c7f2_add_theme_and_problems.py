"""Add Theme and Problems

Revision ID: 7278fe80c7f2
Revises: 
Create Date: 2024-03-15 20:07:20.092964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7278fe80c7f2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('theme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('problem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('difficulty_level', sa.Enum('EASY', 'MEDIUM', 'HARD', name='difficultylevel'), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('explanation', sa.String(), nullable=False),
    sa.Column('theme_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['theme_id'], ['theme.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('problem')
    op.drop_table('theme')
    # ### end Alembic commands ###
