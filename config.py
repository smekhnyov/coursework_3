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
    return tables

def get_columns(table):
    cur = conn.cursor()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
    columns = cur.fetchall()
    return columns

def convert_list_to_str(list, cur):
    colnames = [desc[0] for desc in cur.description]

    table = PrettyTable()
    table.field_names = colnames
    for row in list:
        table.add_row(row)

    # Отправляем таблицу в Telegram
    table_str = table.get_string()
    return table_str