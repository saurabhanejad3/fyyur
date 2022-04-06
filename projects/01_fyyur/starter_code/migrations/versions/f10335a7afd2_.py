"""empty message

Revision ID: f10335a7afd2
Revises: c081bcf64fc5
Create Date: 2022-04-03 22:09:18.327041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f10335a7afd2'
down_revision = 'c081bcf64fc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('artists', 'looking_venues')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('looking_venues', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###
