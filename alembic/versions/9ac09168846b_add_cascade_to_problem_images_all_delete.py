"""Add cascade to Problem.images 'all, delete'

Revision ID: 9ac09168846b
Revises: 5318aff26fdd
Create Date: 2024-04-06 21:49:37.605367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ac09168846b'
down_revision: Union[str, None] = '5318aff26fdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('explanation_image', 'problem_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('explanation_image_problem_id_fkey', 'explanation_image', type_='foreignkey')
    op.create_foreign_key(None, 'explanation_image', 'problem', ['problem_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'explanation_image', type_='foreignkey')
    op.create_foreign_key('explanation_image_problem_id_fkey', 'explanation_image', 'problem', ['problem_id'], ['id'], ondelete='CASCADE')
    op.alter_column('explanation_image', 'problem_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
