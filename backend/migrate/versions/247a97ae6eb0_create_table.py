"""create_table

Revision ID: 247a97ae6eb0
Revises: 
Create Date: 2024-12-08 00:45:21.122407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '247a97ae6eb0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('host', sa.String(), nullable=True),
    sa.Column('execution_time', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('open_port', sa.String(), nullable=True),
    sa.Column('vulnerabilities', sa.JSON(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('data', sa.Column('source', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data', 'source')
    op.drop_table('users')
    op.drop_table('requests')
    # ### end Alembic commands ###