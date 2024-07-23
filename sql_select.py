import telebot
from config import *
import re
import MyKeyboards


@bot.callback_query_handler(func=lambda call: call.data.startswith("select#"))
def call_select(call):
    if len(call.data.split("@")) == 1:
        table = call.data.split("#")[1]
        bot.send_message(call.message.chat.id, "Пожалуйста, выберите столбцы для вашего запроса.", reply_markup=MyKeyboards.select_columns(table))
    else:
        table = re.sub("select#", "", call.data).split("@")[0]
        column = re.sub("select#", "", call.data).split("@")[1]

        if bot_settings.get_dist() == 0:
            sql_select(call.message, table, column)
        elif bot_settings.get_dist() == 1:
            sql_select(call.message, table, column, True)
        else:
            msg = bot.send_message(call.message.chat.id, f"Хотите выбрать уникальные значения? (Y/N)")
            bot.register_next_step_handler(msg, dist_select, table, column)

def dist_select(message, table, column):
    if message.text == "Y" or message.text == "y":
        sql_select(message, table, column, True)
    else:
        sql_select(message, table, column)

def sql_select(message, table, column, distinct=False):
    cur = conn.cursor()
    if distinct:
        cur.execute("SELECT DISTINCT " + column + " FROM " + table)
    else:
        cur.execute("SELECT " + column + " FROM " + table)
    rows = cur.fetchall()

    cols = [desc[0] for desc in cur.description]

    if bot_settings.get_save() == 0:
        table_str = list_to_str(rows, cols)
        bot.send_message(message.chat.id, f"Вот результаты вашего запроса:\n\n<pre>{table_str}</pre>", parse_mode='HTML')
    elif bot_settings.get_save() == 1:
        list_to_csv(rows, cols, f"{table}_{column if column != '*' else 'all'}.csv")
        bot.send_document(message.chat.id, open(f"{table}_{column if column != '*' else 'all'}.csv", "rb"))
    else:
        msg = bot.send_message(message.chat.id, "Вывести в сообщении или сохранить в файл? (M/F)")
        bot.register_next_step_handler(msg, save_select, table, column, rows, cols)

def save_select(message, table, column, rows, cols):
    if message.text == "M":
        table_str = list_to_str(rows, cols)
        bot.send_message(message.chat.id, f"Вот результаты вашего запроса:\n\n<pre>{table_str}</pre>", parse_mode='HTML')
    else:
        list_to_csv(rows, cols, f"{table}_{column if column != '*' else 'all'}.csv")
        bot.send_document(message.chat.id, open(f"{table}_{column if column != '*' else 'all'}.csv", "rb"))
