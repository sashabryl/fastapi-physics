"""Add created_by - created_problems relationship between Problem and User

Revision ID: 5318aff26fdd
Revises: fef7f65da458
Create Date: 2024-04-06 20:58:52.043518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5318aff26fdd'
down_revision: Union[str, None] = 'fef7f65da458'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('problem', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'problem', 'user', ['author_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'problem', type_='foreignkey')
    op.drop_column('problem', 'author_id')
    # ### end Alembic commands ###
