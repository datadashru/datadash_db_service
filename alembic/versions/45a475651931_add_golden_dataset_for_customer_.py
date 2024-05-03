"""Add golden dataset for customer_prediction and customer_summary

Revision ID: 45a475651931
Revises: 
Create Date: 2024-03-18 14:29:18.886093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45a475651931'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open('sql/2_golden_prediction.up.sql', 'r', encoding='utf-8') as f:
        sql_command = ''
        for line in f:
            # Accumulate lines until a semicolon is encountered
            sql_command += line.strip()
            if sql_command.endswith(';'):
                # Execute the accumulated SQL command
                op.execute(sql_command)
                # Reset the accumulated SQL command
                sql_command = ''
    with open('sql/3_golden_summary.up.sql', 'r', encoding='utf-8') as f:
        sql_command = ''
        for line in f:
            # Accumulate lines until a semicolon is encountered
            sql_command += line.strip()
            if sql_command.endswith(';'):
                # Execute the accumulated SQL command
                op.execute(sql_command)
                # Reset the accumulated SQL command
                sql_command = ''
    pass


def downgrade() -> None:
    with open('sql/2_golden_prediction.down.sql', 'r', encoding='utf-8') as f:
        op.execute(f.read())
    with open('sql/3_golden_summary.down.sql', 'r', encoding='utf-8') as f:
        op.execute(f.read())
    pass
