"""update is_active column

Revision ID: 80c59e66fbd5
Revises: af29fbec502d
Create Date: 2023-01-17 19:12:27.163810

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT


# revision identifiers, used by Alembic.
revision = '80c59e66fbd5'
down_revision = 'af29fbec502d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        'users', 'is_active', server_default=sa.text('1')
    )


def downgrade() -> None:
    op.alter_column(
        'users', 'is_active', server_default=sa.text('0')
    )
