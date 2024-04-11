"""Add CommentReaction model & likes and dislikes fields to Comment

Revision ID: eada7ed992cf
Revises: 154101f7e1fc
Create Date: 2024-04-11 22:04:56.253641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eada7ed992cf'
down_revision: Union[str, None] = '154101f7e1fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment_reaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('LIKE', 'DISLIKE', name='reactiontype'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('comment', sa.Column('likes', sa.Integer(), nullable=False))
    op.add_column('comment', sa.Column('dislikes', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'dislikes')
    op.drop_column('comment', 'likes')
    op.drop_table('comment_reaction')
    # ### end Alembic commands ###
