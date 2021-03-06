"""empty message

Revision ID: df796d2e6d4f
Revises: 70f9f940b680
Create Date: 2018-08-22 15:32:25.786479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df796d2e6d4f'
down_revision = '70f9f940b680'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('names', sa.Column('comment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'names', 'comments', ['comment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'names', type_='foreignkey')
    op.drop_column('names', 'comment_id')
    # ### end Alembic commands ###
