"""empty message

Revision ID: 4c07b64d02fe
Revises: ff874ec03ce1
Create Date: 2024-01-28 10:42:24.608218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c07b64d02fe'
down_revision = 'ff874ec03ce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=False))
        batch_op.create_index(batch_op.f('ix_tasks_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tasks_timestamp'))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###
