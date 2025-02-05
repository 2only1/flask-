"""empty message

Revision ID: 55edf318540e
Revises: edefe7f778ab
Create Date: 2024-09-21 09:51:35.611556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55edf318540e'
down_revision = 'edefe7f778ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=512), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('introduce', sa.Text(), nullable=True),
    sa.Column('big_img', sa.String(length=255), nullable=True),
    sa.Column('small_img', sa.String(length=255), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('is_promote', sa.Integer(), nullable=True),
    sa.Column('hot_number', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('cid_one', sa.Integer(), nullable=True),
    sa.Column('cid_two', sa.Integer(), nullable=True),
    sa.Column('cid_three', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cid_one'], ['t_category.id'], ),
    sa.ForeignKeyConstraint(['cid_three'], ['t_category.id'], ),
    sa.ForeignKeyConstraint(['cid_two'], ['t_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_product')
    # ### end Alembic commands ###
