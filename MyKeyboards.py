from telebot import types
import telebot
from config import *

def main():
    main_key = types.ReplyKeyboardMarkup(True, True)
    main_key.row('SELECT')
    main_key.row('INSERT')
    main_key.row('UPDATE')
    main_key.row('DELETE')
    return main_key

def tables(prefix):
    tables_key = types.InlineKeyboardMarkup()
    for table in get_tables():
        tables_key.add(types.InlineKeyboardButton(table, callback_data=prefix + "#" + table))
    return tables_key


def select_columns(prefix, table):
    columns_key = types.InlineKeyboardMarkup()
    for column in get_columns(table):
        columns_key.add(types.InlineKeyboardButton(column, callback_data="select#" + table + "@" + column))
    columns_key.add(types.InlineKeyboardButton("ALL", callback_data="select#" + table + "@*"))
    return columns_key