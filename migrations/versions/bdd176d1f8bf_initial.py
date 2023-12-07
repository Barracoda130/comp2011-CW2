"""initial

Revision ID: bdd176d1f8bf
Revises: 
Create Date: 2023-12-06 21:30:27.791561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdd176d1f8bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.Column('required', sa.Double(), nullable=True),
    sa.Column('diff', sa.Double(), nullable=True),
    sa.Column('supplier', sa.String(), nullable=True),
    sa.Column('price', sa.Double(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.Column('course', sa.Integer(), nullable=True),
    sa.Column('numberOfKids', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('kit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('course', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_in_kit',
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('kit_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['stock_item.id'], ),
    sa.ForeignKeyConstraint(['kit_id'], ['kit.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item_in_kit')
    op.drop_table('kit')
    op.drop_table('event')
    op.drop_table('stock_item')
    op.drop_table('course')
    # ### end Alembic commands ###