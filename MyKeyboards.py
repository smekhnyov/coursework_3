from telebot import types
import telebot
from config import *
import Postgres

def main():
    main_key = types.ReplyKeyboardMarkup(True, True)
    main_key.row('SELECT', 'INSERT')
    main_key.row('UPDATE', 'DELETE')
    main_key.row('Выполнить', 'Запросы')
    main_key.row('Настройки', 'Помощь')
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

def settings():
    global set_save, set_dist
    settings_key = types.InlineKeyboardMarkup()
    if bot_settings.get_save():
        settings_key.add(types.InlineKeyboardButton("Вывод: в csv файл", callback_data="settings#save#0"))
    else:
        settings_key.add(types.InlineKeyboardButton("Вывод: текстом в сообщение", callback_data="settings#save#1"))
    if bot_settings.get_dist() == 0:
        settings_key.add(types.InlineKeyboardButton("Все значения", callback_data="settings#dist#1"))
    elif bot_settings.get_dist() == 1:
        settings_key.add(types.InlineKeyboardButton("Уникальные значения", callback_data="settings#dist#2"))
    else:
        settings_key.add(types.InlineKeyboardButton("Спрашивать каждый раз", callback_data="settings#dist#0"))
    return settings_key