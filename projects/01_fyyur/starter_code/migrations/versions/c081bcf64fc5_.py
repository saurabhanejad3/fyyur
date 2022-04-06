"""empty message

Revision ID: c081bcf64fc5
Revises: e4f2b02a2859
Create Date: 2022-04-03 21:25:05.028966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c081bcf64fc5'
down_revision = 'e4f2b02a2859'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.drop_column('artists', 'description')
    op.add_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.drop_column('venues', 'description')
    op.drop_column('venues', 'looking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('looking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('venues', sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('venues', 'seeking_description')
    op.drop_column('venues', 'seeking_talent')
    op.add_column('artists', sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('artists', 'seeking_description')
    # ### end Alembic commands ###
