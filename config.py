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


def validate_input(value, data_type, max_length=None):
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
            if max_length is not None and len(value) > max_length:
                raise ValueError
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