"""empty message

Revision ID: 85b203ef0f2f
Revises: 92c2b4ef9dea
Create Date: 2024-09-12 17:33:20.903184

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '85b203ef0f2f'
down_revision = '92c2b4ef9dea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_category', schema=None) as batch_op:
        batch_op.alter_column('level',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.drop_index('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_category', schema=None) as batch_op:
        batch_op.create_index('name', ['name'], unique=True)
        batch_op.alter_column('level',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###
