"""add foreign key to posts  table

Revision ID: 56d4875200c8
Revises: 7af49641c42e
Create Date: 2022-01-04 19:53:33.686461

"""
from typing import List
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '56d4875200c8'
down_revision = '7af49641c42e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
    sa.Column('owner_id', sa.Integer(),nullable=False)
    )

    op.create_foreign_key('posts_users_fkey',source_table='posts',referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey','posts')
    op.drop_column('posts','owner_id')
    pass
