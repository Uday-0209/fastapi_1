"""Create phone number col on users table

Revision ID: b939ecda4502
Revises: 
Create Date: 2025-05-09 21:17:17.838341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b939ecda4502'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
