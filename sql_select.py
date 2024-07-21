import telebot
from config import *
import re
import MyKeyboards


@bot.callback_query_handler(func=lambda call: call.data.startswith("select#"))
def call_select(call):
    if len(call.data.split("@")) == 1:
        table = call.data.split("#")[1]
        bot.send_message(call.message.chat.id, "SELECT", reply_markup=MyKeyboards.select_columns(table))
    else:
        table = re.sub("select#", "", call.data).split("@")[0]
        column = re.sub("select#", "", call.data).split("@")[1]
        msg = bot.send_message(call.message.chat.id, f"DISTINCT? (Y/N)")
        bot.register_next_step_handler(msg, sql_select, table, column)


def sql_select(message: telebot.types.Message, table:str, column:str):
    cur = conn.cursor()
    if message.text == "Y":
        cur.execute("SELECT DISTINCT " + column + " FROM " + table)
    else:
        cur.execute("SELECT " + column + " FROM " + table)
    rows = cur.fetchall()

    cols = [desc[0] for desc in cur.description]
    table_str = convert_list_to_str(rows, cols)
    bot.send_message(message.chat.id, f"<pre>{table_str}</pre>", parse_mode='HTML')

