"""empty message

Revision ID: c0f3ec2a2757
Revises: 
Create Date: 2022-05-25 13:24:16.362208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0f3ec2a2757'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photos', sa.String(length=254), nullable=True))
        batch_op.drop_index('ix_book_photo')
        batch_op.create_index(batch_op.f('ix_book_photos'), ['photos'], unique=False)
        batch_op.drop_column('photo')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo', sa.VARCHAR(length=254), nullable=True))
        batch_op.drop_index(batch_op.f('ix_book_photos'))
        batch_op.create_index('ix_book_photo', ['photo'], unique=False)
        batch_op.drop_column('photos')

    # ### end Alembic commands ###
