"""empty message

Revision ID: 7d54b7fac7e8
Revises: f31533b76516
Create Date: 2023-11-10 22:53:46.247695

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7d54b7fac7e8"
down_revision = "f31533b76516"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "base_user",
        "password",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=255),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "base_user",
        "password",
        existing_type=sa.String(length=255),
        type_=sa.VARCHAR(length=50),
        nullable=True,
    )
    # ### end Alembic commands ###
