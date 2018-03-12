"""empty message

Revision ID: 0b5893014638
Revises: dfe9bdfb19ca
Create Date: 2018-03-11 11:06:33.248695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b5893014638'
down_revision = 'dfe9bdfb19ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('author', sa.Column('dolzh', sa.String(length=80), nullable=True))
    op.add_column('author', sa.Column('stepen', sa.String(length=80), nullable=True))
    op.add_column('author', sa.Column('zvanie', sa.String(length=80), nullable=True))
    op.add_column('coauthor', sa.Column('dolzh', sa.String(length=80), nullable=True))
    op.add_column('coauthor', sa.Column('stepen', sa.String(length=80), nullable=True))
    op.add_column('coauthor', sa.Column('zvanie', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coauthor', 'zvanie')
    op.drop_column('coauthor', 'stepen')
    op.drop_column('coauthor', 'dolzh')
    op.drop_column('author', 'zvanie')
    op.drop_column('author', 'stepen')
    op.drop_column('author', 'dolzh')
    # ### end Alembic commands ###
