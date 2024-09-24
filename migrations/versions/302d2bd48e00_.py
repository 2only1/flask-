"""empty message

Revision ID: 302d2bd48e00
Revises: 724e0df8555d
Create Date: 2024-09-23 17:29:38.289951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '302d2bd48e00'
down_revision = '724e0df8555d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('pay_status', sa.Integer(), nullable=True),
    sa.Column('is_send', sa.Integer(), nullable=True),
    sa.Column('fapiao_title', sa.String(length=255), nullable=True),
    sa.Column('fapiao_content', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['t_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('t_express',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('oid', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.Column('update_time', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['oid'], ['t_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('t_order_detail',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('oid', sa.Integer(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['oid'], ['t_order.id'], ),
    sa.ForeignKeyConstraint(['pid'], ['t_product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_order_detail')
    op.drop_table('t_express')
    op.drop_table('t_order')
    # ### end Alembic commands ###
