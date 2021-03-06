"""email-queue-and-add-column-technical_req 

Revision ID: 52ef5bcf6ce2
Revises: e9d01a8a0b58
Create Date: 2020-03-13 10:08:11.984000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52ef5bcf6ce2'
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

    op.add_column('technical_req', sa.Column('id_token_encrypted_response_alg', sa.String(length=10), nullable=True))
    op.add_column('technical_req', sa.Column('userinfo_encrypted_response_alg', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_queue')

    op.drop_column('technical_req', 'userinfo_encrypted_response_alg')
    op.drop_column('technical_req', 'id_token_encrypted_response_alg')
    # ### end Alembic commands ###
