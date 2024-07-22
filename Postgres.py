import Postgres
from config import *

def get_tables() -> list:
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    for i in range(len(tables)):
        tables[i] = tables[i][0]
    return tables

def get_columns(table) -> list:
    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
    columns = cur.fetchall()
    for i in range(len(columns)):
        columns[i] = columns[i][0]
    return columns

def get_column_info(table, column) -> dict:
    cur = conn.cursor()
    cur.execute(f"""
        SELECT data_type, character_maximum_length, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = '{table}' AND column_name = '{column}'
    """)
    column_info = cur.fetchone()

    if column_info:
        column_info_dict = {
            'data_type': column_info[0],
            'character_maximum_length': column_info[1],
            'is_nullable': False if column_info[2] == 'NO' else 'YES',
            'column_default': column_info[3]
        }
        return column_info_dict
    else:
        return None

def get_primary_keys(table) -> list:
    cur = conn.cursor()
    cur.execute(f"""
                SELECT a.attname
                FROM   pg_index i
                JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                     AND a.attnum = ANY(i.indkey)
                WHERE  i.indrelid = '{table}'::regclass
                AND    i.indisprimary;
    """)
    primary_keys = cur.fetchall()
    if len(primary_keys) == 1:
        return primary_keys[0][0]
    else:
        for i in range(len(primary_keys)):
            primary_keys[i] = primary_keys[i][0]
    return primary_keys

def get_data_from_column(table, column) -> list:
    cur = conn.cursor()
    cur.execute(f"SELECT {column} FROM {table}")
    data = cur.fetchall()
    for i in range(len(data)):
        data[i] = data[i][0]
    return data

def get_data_by_key_from_column(table, column, key) -> str:
    cur = conn.cursor()
    cur.execute(f"SELECT {column} FROM {table} WHERE {Postgres.get_primary_keys(table)} = '{key}'")
    data = cur.fetchone()
    return data[0]