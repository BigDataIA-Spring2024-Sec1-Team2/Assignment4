from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from dotenv import load_dotenv

load_dotenv()

import os

# Step 1: Connect to Snowflake database using SQLAlchemy
snowflake_username = os.getenv("snowflake_username")
snowflake_password = os.getenv("snowflake_password")
snowflake_account = os.getenv("snowflake_account")
snowflake_database = os.getenv("snowflake_database")
snowflake_schema = os.getenv("snowflake_schema")

engine = create_engine(
    f'snowflake://{snowflake_username}:{snowflake_password}@{snowflake_account}/{snowflake_database}?schema={snowflake_schema}'
)

# Step 2: Define table schema and create a table if not exists
metadata = MetaData()
table_name = 'GROCERIES'
table = Table(
    table_name,
    metadata,
    Column('item_id', String, primary_key=True),
    Column('item_name', String),
    Column('quantity', Integer),
    # Add more columns as necessary
)

metadata.create_all(engine, checkfirst=True)

def add_item(item_id, item_name, quantity):
    row = {
        'item_id': item_id, 
        'item_name': item_name, 
        'quantity': quantity
        }
    with engine.connect() as connection:
        connection.execute(table.insert().values(row))