"""empty message

Revision ID: 4f24c47cd266
Revises: 45a475651931
Create Date: 2024-05-03 14:50:10.096790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import os
import csv

# revision identifiers, used by Alembic.
revision: str = '4f24c47cd266'
down_revision: Union[str, None] = '45a475651931'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def generate_insert_statements(table_name, csv_file_path, batch_size=100):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)[1:]  # Get the headers from the first row
        # List to accumulate insert statements
        insert_statements = []
        
        # Accumulate rows in batches
        batch = []
        for row in csv_reader:
            batch.append(row)
            if len(batch) == batch_size:
                # Create the INSERT statement for the current batch
                values_str = ', '.join(
                    f"({', '.join([f'\'{v}\'' for v in row][1:])})" for row in batch
                ).replace("''", "'0'")
                insert_sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES {values_str};"
                insert_statements.append(insert_sql)

                # Reset the batch
                batch = []
        
        # If there's any leftover data in the last batch, add it as an insert
        if batch:
            values_str = ', '.join(
                f"({', '.join([f'\'{v}\'' for v in row][1:])})" for row in batch
            )
            insert_sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES {values_str};"
            insert_statements.append(insert_sql)
        
        return insert_statements

def upgrade():
    op.create_table(
        "trigger_customer",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customer_name', sa.String(255)),
        sa.Column('inn', sa.String(255)),
        sa.Column('eid', sa.String(255)),
        sa.Column('manager', sa.String(255)),
        sa.Column('business_group', sa.String(255)),
        sa.Column('risk_flag', sa.Integer),
        sa.Column('month_and_year', sa.String(7)),
        sa.Column('credit_account_active_count', sa.Integer),
        sa.Column('credit_account_active_sum', sa.Float),
        sa.Column('credit_account_active_average_amount', sa.Float),
        sa.Column('credit_account_active_average_duration', sa.Float),
        sa.Column('credit_account_refill_sum', sa.Float),
        sa.Column('current_account_count', sa.Integer),
        sa.Column('current_account_sum_lastday', sa.Float),
        sa.Column('current_account_average_lastday', sa.Float),
        sa.Column('current_account_average_allmonth', sa.Float),
        sa.Column('current_account_credit_allmonth', sa.Float),
        sa.Column('current_account_debit_allmonth', sa.Float),
        sa.Column('debit_account_count', sa.Integer),
        sa.Column('debit_account_sum_lastday', sa.Float),
        sa.Column('debit_account_average_lastday', sa.Float),
        sa.Column('debit_account_average_allmonth', sa.Float),
        sa.Column('debit_account_credit_allmonth', sa.Float),
        sa.Column('debit_account_debit_allmonth', sa.Float),
        sa.Column('is_with_active_loan', sa.Boolean),
        sa.Column('active_loan_count', sa.Integer),
        sa.Column('is_with_active_deposit', sa.Boolean),
        sa.Column('active_deposit_count', sa.Integer),
        sa.Column('is_with_active_current', sa.Boolean),
        sa.Column('active_current_count', sa.Integer),
    )

    csv_file_path = 'sql/trigger_customer.csv'
    insert_statements = generate_insert_statements('trigger_customer', csv_file_path)
    for insert_sql in insert_statements:
        op.execute(insert_sql)

def downgrade():
    op.drop_table("trigger_customer")