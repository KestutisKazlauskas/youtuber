"""empty message

Revision ID: 57755e9ff581
Revises: ca89626dd497
Create Date: 2018-03-05 20:39:33.489886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57755e9ff581'
down_revision = 'ca89626dd497'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'tag', ['name'], unique=True)
    # ### end Alembic commands ###