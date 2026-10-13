"""initial

Revision ID: db15dbfea051
Revises: 
Create Date: 2026-10-13 17:10:15.847431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db15dbfea051'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Baseline: schema as it existed in production before Alembic was added.
# Production was stamped past this revision, so it only runs on fresh databases.
def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('pass_hash', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('username', name='users_username_key'),
    )
    op.create_table(
        'clients',
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('cpf', sa.String(), nullable=False),
        sa.Column('cep', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('tel', sa.String(), nullable=True),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('expired', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('client_id'),
        sa.UniqueConstraint('cpf', name='clients_cpf_key'),
        sa.UniqueConstraint('email', name='clients_email_key'),
    )
    op.create_table(
        'vehicles',
        sa.Column('vehicle_id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('plate', sa.String(), nullable=False),
        sa.Column('kind', sa.String(), nullable=True),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], name='vehicles_client_id_fkey'),
        sa.PrimaryKeyConstraint('vehicle_id'),
        sa.UniqueConstraint('plate', name='vehicles_plate_key'),
    )
    op.create_table(
        'services',
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('vehicle_id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('desc', sa.String(), nullable=False),
        sa.Column('date_release', sa.DateTime(), nullable=True),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('labor_value', sa.Float(), nullable=True),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('finish', sa.Boolean(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], name='services_client_id_fkey'),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.vehicle_id'], name='services_vehicle_id_fkey'),
        sa.PrimaryKeyConstraint('service_id'),
    )
    op.create_table(
        'materials',
        sa.Column('material_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('mark', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('date_available', sa.DateTime(), nullable=True),
        sa.Column('expired', sa.Boolean(), nullable=False),
        sa.Column('available', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('material_id'),
    )
    op.create_table(
        'expenses',
        sa.Column('expense_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('origin', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('expense_id'),
    )


def downgrade() -> None:
    op.drop_table('expenses')
    op.drop_table('materials')
    op.drop_table('services')
    op.drop_table('vehicles')
    op.drop_table('clients')
    op.drop_table('users')
