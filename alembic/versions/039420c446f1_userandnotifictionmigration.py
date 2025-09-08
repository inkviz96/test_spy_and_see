"""UserAndNotifictionMigration

Revision ID: 039420c446f1
Revises:
Create Date: 2025-09-08 17:35:06.503301

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "039420c446f1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("username", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "avatar_url",
            sa.String(),
            nullable=False,
            server_default="https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fimage.pngaaa.com%2F689%2F2189689-middle.png&lr=2&pos=4&rpt=simage&text=avatar%20user",
        ),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.String(length=15), nullable=False),
        sa.Column("text", sa.String(length=255), nullable=False),
    )


def downgrade():
    op.drop_table("notifications")
    op.drop_table("users")
