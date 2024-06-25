"""add apt_num col

Revision ID: c2c0fd66d18c
Revises: 6d579c1ab27d
Create Date: 2024-06-24 13:47:43.186503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2c0fd66d18c'
down_revision: Union[str, None] = '6d579c1ab27d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('address', 
                  sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
