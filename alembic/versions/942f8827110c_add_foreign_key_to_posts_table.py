"""add foreign key to posts table

Revision ID: 942f8827110c
Revises: d1563aab04a2
Create Date: 2025-12-12 13:29:26.093656

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "942f8827110c"
down_revision: Union[str, Sequence[str], None] = "d1563aab04a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    pass
