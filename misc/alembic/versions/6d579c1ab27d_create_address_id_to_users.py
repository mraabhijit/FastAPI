"""create address_id to users

Revision ID: 6d579c1ab27d
Revises: 3d140046693d
Create Date: 2024-06-24 13:03:29.768089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d579c1ab27d'
down_revision: Union[str, None] = '3d140046693d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', 
                  sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', 
                          source_table='users', 
                          referent_table='address',
                          local_cols=['address_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_fk', 'users')
    op.drop_column('users', 'address_id')
