"""merge heads

Revision ID: 6dcf5f99936e
Revises: 54e99867c6d6, e8d1cb6e3be5
Create Date: 2026-04-11 08:55:52.561692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dcf5f99936e'
down_revision: Union[str, None] = ('54e99867c6d6', 'e8d1cb6e3be5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
