"""Init

Revision ID: fd423331d2d7
Revises: 
Create Date: 2024-06-10 23:28:25.464291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd423331d2d7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('grades', 'grade',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('grades', 'grade_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('grades', 'grade_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('grades', 'grade',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###