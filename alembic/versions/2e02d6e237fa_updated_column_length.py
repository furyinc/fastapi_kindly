"""Updated column length

Revision ID: 2e02d6e237fa
Revises: d849c83f215f
Create Date: 2025-01-10 00:56:15.489377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '2e02d6e237fa'
down_revision: Union[str, None] = 'd849c83f215f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('donations', 'description',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('donations', 'photos',
               existing_type=mysql.VARCHAR(length=1024),
               type_=sa.Text(),
               existing_nullable=True)
    op.drop_column('donations', 'current_amount')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donations', sa.Column('current_amount', mysql.FLOAT(), nullable=True))
    op.alter_column('donations', 'photos',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=1024),
               existing_nullable=True)
    op.alter_column('donations', 'description',
               existing_type=mysql.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
