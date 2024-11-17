"""empty message

Revision ID: 253759d83b71
Revises: 
Create Date: 2024-11-17 12:44:51.909595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '253759d83b71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
