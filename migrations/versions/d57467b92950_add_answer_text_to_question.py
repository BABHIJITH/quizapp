"""Add answer_text to Question

Revision ID: d57467b92950
Revises: dfed4f069d0d
Create Date: 2025-02-04 17:05:16.709454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd57467b92950'
down_revision = 'dfed4f069d0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer_text', sa.String(length=128), nullable=True))
        batch_op.drop_column('answer')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer', sa.VARCHAR(length=64), nullable=True))
        batch_op.drop_column('answer_text')

    # ### end Alembic commands ###
