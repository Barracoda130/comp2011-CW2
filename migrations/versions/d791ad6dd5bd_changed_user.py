"""changed user

Revision ID: d791ad6dd5bd
Revises: 913319d163e6
Create Date: 2023-12-07 09:22:58.004309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd791ad6dd5bd'
down_revision = '913319d163e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
