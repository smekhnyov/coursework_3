import telebot
from config import *
import re
import MyKeyboards
import Postgres


@bot.callback_query_handler(func=lambda call: call.data.startswith("update#"))
def call_update(call):
    if len(call.data.split("@")) == 1:
        table = call.data.split("#")[1]
        primary_keys_update = types.InlineKeyboardMarkup()
        for key in Postgres.get_data_from_column(table, Postgres.get_primary_keys(table)):
            primary_keys_update.add(types.InlineKeyboardButton(key, callback_data="update#" + table + "@" + str(key)))
        msg = bot.send_message(call.message.chat.id, "PRIMARY KEY", reply_markup=primary_keys_update)
    elif len(call.data.split("@")) == 2:
        table = re.sub("update#", "", call.data).split("@")[0]
        primary_key = re.sub("update#", "", call.data).split("@")[1]
        bot.send_message(call.message.chat.id, f"COLUMNS", reply_markup=MyKeyboards.update_columns(table, primary_key))
    else:
        table = re.sub("update#", "", call.data).split("@")[0]
        primary_key = re.sub("update#", "", call.data).split("@")[1]
        column = re.sub("update#", "", call.data).split("@")[2]
        msg = bot.send_message(call.message.chat.id, f"SET {column} = {Postgres.get_data_by_key_from_column(table, column, primary_key)}\n\n<pre>{Postgres.get_column_info(table, column)}</pre>", parse_mode='HTML')
        bot.register_next_step_handler(msg, sql_update, table, column, primary_key)

def sql_update(message: telebot.types.Message, table: str, column: str, primary_key: str):
    info = Postgres.get_column_info(table, column)
    new_value = message.text

    # Validate the new value
    if not validate_input(new_value, info['data_type'], info['character_maximum_length']):
        msg = bot.send_message(message.chat.id, "Invalid input. Please enter a new value.")
        bot.register_next_step_handler(msg, sql_update, table, column, primary_key)
        return

    # Add quotes for string types
    if info['data_type'] in ['character varying', 'text', 'date', 'timestamp', 'timestamp with time zone', 'timestamp without time zone']:
        new_value = f"'{new_value}'"

    # Construct the SQL update statement
    cur = conn.cursor()
    primary_key_column = Postgres.get_primary_keys(table)
    update_query = f"""
        UPDATE {table} 
        SET {column} = {new_value} 
        WHERE {primary_key_column} = '{primary_key}';
    """
    cur.execute(update_query)
    conn.commit()
    bot.send_message(message.chat.id, "Updated successfully.")