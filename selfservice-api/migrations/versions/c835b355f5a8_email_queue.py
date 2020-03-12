"""email-queue

Revision ID: c835b355f5a8
Revises: e9d01a8a0b58
Create Date: 2020-03-09 15:02:32.993751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c835b355f5a8'
down_revision = 'e9d01a8a0b58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_queue',
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('modified', sa.DateTime(), nullable=True),
                    sa.Column('created_by', sa.String(), nullable=False),
                    sa.Column('modified_by', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('subject', sa.String(), nullable=False),
                    sa.Column('recipients', sa.JSON(), nullable=False),
                    sa.Column('body', sa.String(), nullable=False),
                    sa.Column('sender', sa.String(), nullable=False),
                    sa.Column('cc', sa.JSON(), nullable=True),
                    sa.Column('bcc', sa.JSON(), nullable=True),
                    sa.Column('email_type', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_queue')
    # ### end Alembic commands ###
