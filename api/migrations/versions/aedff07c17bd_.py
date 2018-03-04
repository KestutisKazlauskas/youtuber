"""empty message

Revision ID: aedff07c17bd
Revises: ce520fc2fde8
Create Date: 2018-03-04 16:55:14.137528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aedff07c17bd'
down_revision = 'ce520fc2fde8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('description', mysql.VARCHAR(length=255), nullable=True))
    # ### end Alembic commands ###
