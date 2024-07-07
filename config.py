from dotenv import load_dotenv
import telebot
from telebot import types
import psycopg2
import os

load_dotenv(dotenv_path="config.env")

conn = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))

token = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)