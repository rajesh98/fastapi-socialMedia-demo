"""Add content Column to posts table

Revision ID: 3a547297d678
Revises: 2e7d71315c3b
Create Date: 2022-01-04 18:56:36.688383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a547297d678'
down_revision = '2e7d71315c3b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(), nullable=False,))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
