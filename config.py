from dotenv import load_dotenv
import telebot
import psycopg2
import os
from prettytable import PrettyTable
from Settings import Settings
import csv

load_dotenv(dotenv_path="config.env")

conn = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))

token = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)

bot_settings = Settings()

def convert_list_to_str(list, colnames) -> str:
    table = PrettyTable()
    table.field_names = colnames
    for row in list:
        table.add_row(row)

    # Отправляем таблицу в Telegram
    table_str = table.get_string()
    return table_str

def list_to_csv(list, colnames, file_path) -> None:
    # Открытие файла и запись данных в CSV
    with open(f"./{file_path}", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Запись заголовков колонок
        writer.writerow(colnames)
        # Запись данных
        writer.writerows(list)

