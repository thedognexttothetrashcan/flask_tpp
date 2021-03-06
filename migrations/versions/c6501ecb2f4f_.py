"""empty message

Revision ID: c6501ecb2f4f
Revises: e4702973e92a
Create Date: 2018-11-20 09:38:37.878610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6501ecb2f4f'
down_revision = 'e4702973e92a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cinema',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('c_name', sa.String(length=32), nullable=True),
    sa.Column('c_address', sa.String(length=128), nullable=True),
    sa.Column('c_phone', sa.String(length=32), nullable=True),
    sa.Column('c_city', sa.String(length=32), nullable=True),
    sa.Column('c_user', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['c_user'], ['cinema_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('c_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cinema')
    # ### end Alembic commands ###
