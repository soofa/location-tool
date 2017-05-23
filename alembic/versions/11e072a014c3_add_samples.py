"""add samples

Revision ID: 11e072a014c3
Revises: 04fa912853f0
Create Date: 2017-05-23 20:50:34.435432+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11e072a014c3'
down_revision = '04fa912853f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bounding_boxes', sa.Column('samples', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bounding_boxes', 'samples')
    # ### end Alembic commands ###