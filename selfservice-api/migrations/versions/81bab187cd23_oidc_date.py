"""oidc-date

Revision ID: 81bab187cd23
Revises: 21a4a3ff3229
Create Date: 2020-03-24 15:05:59.216218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81bab187cd23'
down_revision = '21a4a3ff3229'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('oidc_dev_date', sa.DateTime(), nullable=True))
    op.add_column('project', sa.Column('oidc_prod_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'oidc_prod_date')
    op.drop_column('project', 'oidc_dev_date')
    # ### end Alembic commands ###