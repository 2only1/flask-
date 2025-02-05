"""empty message

Revision ID: aca7c965d568
Revises: 3915e023b5ab
Create Date: 2024-09-02 23:47:16.351941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca7c965d568'
down_revision = '3915e023b5ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_menu',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(length=32), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_menu')
    # ### end Alembic commands ###
