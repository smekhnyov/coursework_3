from config import *
import csv
from telebot import types
import MyKeyboards

request_file = '../request.csv'

def one(message, name = False):
    if message.text == "Назад":
        bot.send_message(message.chat.id, "Отменено", reply_markup=MyKeyboards.main())
        return
    request = get(message.text) if name else message.text
    bot.send_message(message.chat.id, execute(request), parse_mode='HTML', reply_markup=MyKeyboards.main())

@bot.callback_query_handler(func = lambda call: call.data.startswith("settings#request"))
def call_settings(call):
    if call.data == "settings#request#new":
        msg = bot.send_message(call.message.chat.id, "Напиши запрос для сохранения.")
        bot.register_next_step_handler(msg, save_name)
    elif call.data == "settings#request#del":
        msg = bot.send_message(call.message.chat.id, "Выбери запрос для удаления.", reply_markup=MyKeyboards.requests(request_file))
        bot.register_next_step_handler(msg, delete_request)
    elif call.data == "settings#request#delall":
        msg = bot.send_message(call.message.chat.id, "Вы уверены? (Y/N)")
        bot.register_next_step_handler(msg, delete_all_request)

def save_name(message):
    msg = bot.send_message(message.chat.id, "Напиши название для удобства. Если не хочешь сохранять запрос, напишите -")
    bot.register_next_step_handler(msg, save_request, message.text)

def save_request(message, request):
    save(request, message.text if message.text != '-' else None)
    bot.send_message(message.chat.id, "Сохранено", reply_markup=MyKeyboards.main())

def delete_request(message):
    if message.text == "Назад":
        bot.send_message(message.chat.id, "Отменено", reply_markup=MyKeyboards.main())
        return
    delete(message.text)
    bot.send_message(message.chat.id, "Удалено", reply_markup=MyKeyboards.main())

def delete_all_request(message):
    if message.text == "Y":
        delete_all()
    bot.send_message(message.chat.id, "Удалено", reply_markup=MyKeyboards.main())

def execute(request):
    try:
        cur = conn.cursor()
        cur.execute(request)
        if "select" not in request.lower():
            conn.commit()
            return "Запрос выполнен успешно."
        else:
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
            table_str = list_to_str(rows, cols)
            return f"Вот результаты вашего запроса:\n\n<pre>{table_str}</pre>"
    except (Exception,psycopg2.DatabaseError) as e:
        return f"Произошла ошибка: {e}"

def save(request, name = None):
    with open(request_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([request, name if name is not None else request])

def get(name):
    with open(request_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == name:
                return row[0]

def get_all():
    rows = {}
    with open(request_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            rows[row[1]] = row[0]

def delete(name):
    with open(request_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            if row[1] != name:
                rows.append(row)
    with open(request_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def delete_all():
    with open(request_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
