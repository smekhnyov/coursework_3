from telebot import types
import telebot
from config import *
import Postgres

def main():
    main_key = types.ReplyKeyboardMarkup(True, True)
    main_key.row('SELECT')
    main_key.row('CREATE')
    main_key.row('INSERT')
    main_key.row('UPDATE')
    main_key.row('DELETE')
    main_key.row('Помощь')
    return main_key

def tables(prefix):
    tables_key = types.InlineKeyboardMarkup()
    for table in Postgres.get_tables():
        tables_key.add(types.InlineKeyboardButton(table, callback_data=prefix + "#" + table))
    return tables_key


def select_columns(table):
    columns_key = types.InlineKeyboardMarkup()
    for column in Postgres.get_columns(table):
        columns_key.add(types.InlineKeyboardButton(column, callback_data="select#" + table + "@" + column))
    columns_key.add(types.InlineKeyboardButton("ALL", callback_data="select#" + table + "@*"))
    return columns_key

def update_columns(table, primary_key):
    columns_key = types.InlineKeyboardMarkup()
    for column in Postgres.get_columns(table):
        columns_key.add(types.InlineKeyboardButton(column, callback_data="update#" + table + "@" + primary_key + "@" + column))
    return columns_key