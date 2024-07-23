import telebot
from config import *
import re
import MyKeyboards
import Postgres


@bot.callback_query_handler(func=lambda call: call.data.startswith("insert#"))
def call_insert(call):
    sql_insert(call.message, call.data.split("#")[1], [])

def sql_insert(message: telebot.types.Message, table: str, data: list, current_column:str=None):
    columns = Postgres.get_columns(table)

    if current_column is None:
        current_column = columns[0]
    else:
        info = Postgres.get_column_info(table, current_column)
        if not info['is_nullable'] and message.text == 'NULL':
            bot.send_message(message.chat.id, f"Значение для столбца '{current_column}' не может быть NULL. Пожалуйста, введите значение.")
            msg = bot.send_message(message.chat.id, f"INSERT INTO {table} ({current_column})\n\n<pre>{info}</pre>",
                                   parse_mode='HTML')
            bot.register_next_step_handler(msg, sql_insert, table, data, current_column)
            return
        elif not validate_input(message.text, info['data_type'], info['character_maximum_length']) and message.text != 'DEFAULT':
            bot.send_message(message.chat.id,
                             f"Недопустимый тип данных или длина для столбца '{current_column}'. Ожидается {info['data_type']} с максимальной длиной {info['character_maximum_length']}.")
            msg = bot.send_message(message.chat.id, f"INSERT INTO {table} ({current_column})\n\n<pre>{info}</pre>",
                                   parse_mode='HTML')
            bot.register_next_step_handler(msg, sql_insert, table, data, current_column)
            return
        else:
            if message.text == 'DEFAULT' and info['column_default'] is not None:
                data.append("DEFAULT")
            else:
                data.append(message.text)
            cc_index = columns.index(current_column)
            if cc_index < len(columns) - 1:
                current_column = columns[cc_index + 1]
            else:
                return end_insert(message, table, data)

    info = Postgres.get_column_info(table, current_column)
    msg = bot.send_message(message.chat.id, f"Введите значение для столбца '{current_column}':\n\n<pre>{info}</pre>", parse_mode='HTML')
    bot.register_next_step_handler(msg, sql_insert, table, data, current_column)

def end_insert(message, table, data):
    data = tuple(data)
    info = ', '.join([str(i) for i in tuple(Postgres.get_columns(table))])
    values = []
    for item in data:
        if item == 'DEFAULT':
            values.append('DEFAULT')
        else:
            values.append(f"'{item}'")

    values_str = ', '.join(values)
    cur = conn.cursor()
    script = f"INSERT INTO {table} ({info}) VALUES ({values_str})"
    cur.execute(script)
    conn.commit()
    bot.send_message(message.chat.id, "Данные успешно вставлены в таблицу.")
