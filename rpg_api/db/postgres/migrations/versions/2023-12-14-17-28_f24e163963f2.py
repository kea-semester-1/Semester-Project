"""Trigger for audit log

Revision ID: f24e163963f2
Revises: 852baab5b87e
Create Date: 2023-12-14 17:28:15.770132

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f24e163963f2"
down_revision = "852baab5b87e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # ### end Alembic commands ###
    with op.get_context().autocommit_block():
        func_query = """
            CREATE OR REPLACE FUNCTION audit_trigger_func() 
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO audit_log(id, db_user, table_name, action, old_values, new_values, created_at)
                VALUES (gen_random_uuid(), current_user, TG_TABLE_NAME, 
                    TG_OP, row_to_json(OLD), row_to_json(NEW), NOW()
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        op.execute(func_query)

        model_names = [
            "ability",
            "ability_type",
            "attribute",
            "base_class",
            "base_user",
            "character",
            "class_ability",
            # "character_attribute",
        ]

        for model_name in model_names:
            trg_add_query = f"""
                CREATE TRIGGER audit_log_trigger
                AFTER INSERT OR UPDATE OR DELETE ON {model_name}
                FOR EACH ROW EXECUTE PROCEDURE audit_trigger_func();
            """

            op.execute(trg_add_query)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # ### end Alembic commands ###

    with op.get_context().autocommit_block():
        op.execute("DROP TRIGGER audit_log_trigger ON ability;")
        op.execute("DROP FUNCTION audit_trigger_func();")
