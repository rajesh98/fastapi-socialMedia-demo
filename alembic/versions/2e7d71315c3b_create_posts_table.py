"""create posts table

Revision ID: 2e7d71315c3b
Revises: 
Create Date: 2022-01-04 16:08:16.691619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e7d71315c3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(), nullable=False,
    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
