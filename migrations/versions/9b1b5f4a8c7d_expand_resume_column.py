"""expand resume column

Revision ID: 9b1b5f4a8c7d
Revises: 5b35dd9fedc4
Create Date: 2026-01-23 18:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9b1b5f4a8c7d"
down_revision: Union[str, Sequence[str], None] = "5b35dd9fedc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "books",
        "resume",
        existing_type=sa.String(length=1000),
        type_=sa.Text(),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "books",
        "resume",
        existing_type=sa.Text(),
        type_=sa.String(length=1000),
        existing_nullable=True,
    )
