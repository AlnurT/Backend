"""make email unique

Revision ID: 31f24f4bea3c
Revises: ecef231a7d2a
Create Date: 2025-06-22 21:28:09.118346

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "31f24f4bea3c"
down_revision: Union[str, None] = "ecef231a7d2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
