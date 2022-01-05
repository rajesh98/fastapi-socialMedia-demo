"""create user table

Revision ID: 7af49641c42e
Revises: 3a547297d678
Create Date: 2022-01-04 19:13:15.760181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7af49641c42e'
down_revision = '3a547297d678'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id',sa.Integer(), nullable=False), 
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('NOW()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
