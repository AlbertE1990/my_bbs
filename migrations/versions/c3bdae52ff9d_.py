"""empty message

Revision ID: c3bdae52ff9d
Revises: 
Create Date: 2018-08-03 12:20:47.878553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3bdae52ff9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follows',
    sa.Column('follower_id', sa.String(length=100), nullable=False),
    sa.Column('followed_id', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['front_user.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.add_column('front_user', sa.Column('confirm', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('front_user', 'confirm')
    op.drop_table('follows')
    # ### end Alembic commands ###