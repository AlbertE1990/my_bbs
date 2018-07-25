"""empty message

Revision ID: 13bab32ee15d
Revises: 76732951c083
Create Date: 2018-07-24 23:26:15.100222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13bab32ee15d'
down_revision = '76732951c083'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('disabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'disabled')
    # ### end Alembic commands ###
