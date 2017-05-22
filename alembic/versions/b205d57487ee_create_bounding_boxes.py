"""create bounding boxes

Revision ID: b205d57487ee
Revises: 
Create Date: 2017-05-22 13:36:06.607653+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b205d57487ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bounding_boxes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('state', sa.Text(), nullable=False),
    )

def downgrade():
    op.drop_table('bounding_boxes')
