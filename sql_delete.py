import telebot
from config import *
import re
import MyKeyboards
import Postgres

def start_delete(message):
    delete_menu = types.InlineKeyboardMarkup()
    delete_menu.add(types.InlineKeyboardButton("TABLE", callback_data="delete#table"))
    delete_menu.add(types.InlineKeyboardButton("COLUMN", callback_data="delete#column"))
    delete_menu.add(types.InlineKeyboardButton("ROW", callback_data="delete#row"))
    bot.send_message(message.chat.id, "DELETE", reply_markup=delete_menu)


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete#"))
def call_delete(call):
    if len(call.data.split("@")) == 1 and call.data.startswith("delete#table"):
        tables_key = types.InlineKeyboardMarkup()
        for table in Postgres.get_tables():
            tables_key.add(types.InlineKeyboardButton(table, callback_data=call.data + "@" + table))
        bot.send_message(call.message.chat.id, "TABLE", reply_markup=tables_key)
    elif len(call.data.split("@")) == 2 and call.data.startswith("delete#table"):
        yn_menu = types.InlineKeyboardMarkup()
        yn_menu.add(types.InlineKeyboardButton("YES", callback_data=call.data + "@Y"))
        yn_menu.add(types.InlineKeyboardButton("NO", callback_data=call.data + "@N"))
        msg = bot.send_message(call.message.chat.id, "ARE YOU SURE?", reply_markup=yn_menu)
    elif len(call.data.split("@")) == 3 and call.data.startswith("delete#table") and call.data.split("@")[2] == "Y":
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {call.data.split("@")[1]} CASCADE")
        conn.commit()
        bot.send_message(call.message.chat.id, "DELETED")


    elif len(call.data.split("@")) == 1 and call.data.startswith("delete#column"):
        tables_key = types.InlineKeyboardMarkup()
        for table in Postgres.get_tables():
            tables_key.add(types.InlineKeyboardButton(table, callback_data=call.data + "@" + table))
        bot.send_message(call.message.chat.id, "TABLE", reply_markup=tables_key)
    elif len(call.data.split("@")) == 2 and call.data.startswith("delete#column"):
        columns_key = types.InlineKeyboardMarkup()
        for column in Postgres.get_columns(call.data.split("@")[1]):
            columns_key.add(types.InlineKeyboardButton(column, callback_data=call.data + "@" + column))
        bot.send_message(call.message.chat.id, "COLUMNS", reply_markup=columns_key)
    elif len(call.data.split("@")) == 3 and call.data.startswith("delete#column"):
        yn_menu = types.InlineKeyboardMarkup()
        yn_menu.add(types.InlineKeyboardButton("YES", callback_data=call.data + "@Y"))
        yn_menu.add(types.InlineKeyboardButton("NO", callback_data=call.data + "@N"))
        msg = bot.send_message(call.message.chat.id, "ARE YOU SURE?", reply_markup=yn_menu)
    elif len(call.data.split("@")) == 4 and call.data.startswith("delete#column") and call.data.split("@")[3] == "Y":
        cur = conn.cursor()
        cur.execute(f"ALTER TABLE {call.data.split("@")[1]} DROP COLUMN {call.data.split("@")[2]}")
        conn.commit()
        bot.send_message(call.message.chat.id, "DELETED")


    elif len(call.data.split("@")) == 1 and call.data.startswith("delete#row"):
        tables_key = types.InlineKeyboardMarkup()
        for table in Postgres.get_tables():
            tables_key.add(types.InlineKeyboardButton(table, callback_data=call.data + "@" + table))
        bot.send_message(call.message.chat.id, "TABLE", reply_markup=tables_key)
    elif len(call.data.split("@")) == 2 and call.data.startswith("delete#row"):
        primary_keys_update = types.InlineKeyboardMarkup()
        table = call.data.split("@")[1]
        for key in Postgres.get_data_from_column(table, Postgres.get_primary_keys(table)):
            primary_keys_update.add(types.InlineKeyboardButton(key, callback_data=call.data + "@" + str(key)))
        bot.send_message(call.message.chat.id, "PRIMARY KEY", reply_markup=primary_keys_update)
    elif len(call.data.split("@")) == 3 and call.data.startswith("delete#row"):
        yn_menu = types.InlineKeyboardMarkup()
        yn_menu.add(types.InlineKeyboardButton("YES", callback_data=call.data + "@Y"))
        yn_menu.add(types.InlineKeyboardButton("NO", callback_data=call.data + "@N"))
        msg = bot.send_message(call.message.chat.id, "ARE YOU SURE?", reply_markup=yn_menu)
    elif len(call.data.split("@")) == 4 and call.data.startswith("delete#row") and call.data.split("@")[3] == "Y":
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {call.data.split("@")[1]} WHERE {Postgres.get_primary_keys(call.data.split("@")[1])} = '{call.data.split("@")[2]}'")
        conn.commit()
        bot.send_message(call.message.chat.id, "DELETED")
