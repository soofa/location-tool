"""add google tags scores

Revision ID: 04fa912853f0
Revises: 6ebcec5aebdf
Create Date: 2017-05-23 20:02:00.759889+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04fa912853f0'
down_revision = '6ebcec5aebdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bounding_boxes', sa.Column('googlescores', sa.Text(), nullable=True))
    op.add_column('bounding_boxes', sa.Column('googletags', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bounding_boxes', 'googletags')
    op.drop_column('bounding_boxes', 'googlescores')
    # ### end Alembic commands ###