"""base

Revision ID: c4864fc5d004
Revises: 
Create Date: 2020-01-15 13:19:38.498147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4864fc5d004'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('org_whitelist',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_name', sa.String(length=250), nullable=False),
    sa.Column('head_of_org', sa.String(length=250), nullable=False),
    sa.Column('domain', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scope_package',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('claim_names', sa.JSON(), nullable=False),
    sa.Column('scope', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('first_name', sa.String(length=250), nullable=False),
    sa.Column('last_name', sa.String(length=250), nullable=False),
    sa.Column('oauth_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_info',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('modified_by', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_name', sa.String(length=100), nullable=False),
    sa.Column('project_name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('my_role', sa.Integer(), nullable=False),
    sa.Column('developer_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('cto_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cto_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['developer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['manager_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('technical_req',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=False),
    sa.Column('modified_by', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_name', sa.String(length=100), nullable=True),
    sa.Column('client_uri', sa.String(length=500), nullable=True),
    sa.Column('redirect_uris', sa.JSON(), nullable=True),
    sa.Column('jwks_uri', sa.String(length=500), nullable=True),
    sa.Column('id_token_signed_response_alg', sa.String(length=10), nullable=True),
    sa.Column('userinfo_signed_response_alg', sa.String(length=10), nullable=True),
    sa.Column('scope_package_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['scope_package_id'], ['scope_package.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('technical_req')
    op.drop_table('project_info')
    op.drop_table('user')
    op.drop_table('scope_package')
    op.drop_table('org_whitelist')
    # ### end Alembic commands ###
