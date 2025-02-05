"""empty message

Revision ID: edefe7f778ab
Revises: 958e1e0cff25
Create Date: 2024-09-14 10:16:11.452899

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'edefe7f778ab'
down_revision = '958e1e0cff25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_attribute',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('val', sa.String(length=255), nullable=True),
    sa.Column('_type', sa.Enum('static', 'dynamic'), nullable=True),
    sa.Column('cid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['t_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('t_attributes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_attributes',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=32), nullable=False),
    sa.Column('val', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('_type', mysql.ENUM('static', 'dynamic'), nullable=True),
    sa.Column('cid', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['t_category.id'], name='t_attributes_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('t_attribute')
    # ### end Alembic commands ###
