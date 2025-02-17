"""add initial parcel types

Revision ID: 7525fcbce74d
Revises: c806aa9d2391
Create Date: 2025-02-17 13:30:45.521208

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7525fcbce74d"
down_revision: Union[str, None] = "c806aa9d2391"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            "parcel_types",
            sa.column("name", sa.String),
        ),
        [
            {"name": "Одежда"},
            {"name": "Электроника"},
            {"name": "Разное"},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM parcel_types WHERE name IN ('Одежда', 'Электроника', 'Разное')")
