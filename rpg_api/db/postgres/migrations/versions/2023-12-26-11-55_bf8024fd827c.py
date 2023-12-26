"""Change radius type to float

Revision ID: bf8024fd827c
Revises: f24e163963f2
Create Date: 2023-12-26 11:55:13.612483

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bf8024fd827c"
down_revision = "f24e163963f2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "place",
        "radius",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "place",
        "radius",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
