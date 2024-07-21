from dotenv import load_dotenv
import telebot
from telebot import types
import psycopg2
import os
from prettytable import PrettyTable

load_dotenv(dotenv_path="config.env")

conn = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))

token = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)

def get_tables():
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    for i in range(len(tables)):
        tables[i] = tables[i][0]
    return tables

def get_columns(table):
    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
    columns = cur.fetchall()
    for i in range(len(columns)):
        columns[i] = columns[i][0]
    return columns


def get_column_info(table, column):
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

def validate_input(value, data_type):
    try:
        if data_type == 'integer':
            int(value)
        elif data_type == 'numeric' or data_type == 'double precision' or data_type == 'real':
            float(value)
        elif data_type == 'boolean':
            if value.lower() not in ['true', 'false']:
                raise ValueError
        elif data_type in ['date', 'timestamp', 'timestamp with time zone', 'timestamp without time zone']:
            import datetime
            datetime.datetime.strptime(value, '%Y-%m-%d' if data_type == 'date' else '%Y-%m-%d %H:%M:%S')
        elif data_type == 'character varying' or data_type == 'text':
            pass
        else:
            pass
        return True
    except ValueError:
        return False

def convert_list_to_str(list, colnames):
    table = PrettyTable()
    table.field_names = colnames
    for row in list:
        table.add_row(row)

    # Отправляем таблицу в Telegram
    table_str = table.get_string()
    return table_str