import MyKeyboards
import sql_delete
import sql_insert
import sql_request
import sql_update
import sql_select
from config import *

request_file = '../request.csv'

@bot.message_handler(commands=["start"])
def com_start(message):
    bot.send_message(message.chat.id, "Hello", reply_markup=MyKeyboards.main())

@bot.message_handler(commands=["help"])
def com_help(message):
    bot.send_message(message.chat.id, "<b>Добро пожаловать!</b>\n"
                                      "<i>Этот бот позволяет выполнять различные операции с базой данных PostgreSQL. Вот доступные команды и их возможности:</i>\n"
                                      "\n"
                                      "<b>/start</b>: Начните работу с ботом. Эта команда выводит приветственное сообщение и главное меню.\n"
                                      "<b>/help</b>: Получите список всех доступных команд и их описание.\n"
                                      "\n"
                                      "<b>Основные команды:</b>\n"
                                      "\n"
                                      "1. <b>SELECT</b>:\n"
                                      "   - Выбор и отображение данных из таблиц.\n"
                                      "   - Включает возможность выбора отдельных колонок и использования DISTINCT для удаления дубликатов.\n"
                                      "\n"
                                      "2. <b>CREATE</b>:\n"
                                      "   - Создание новых таблиц в базе данных.\n"
                                      "   - Добавление новых записей в существующие таблицы.\n"
                                      "\n"
                                      "3. <b>INSERT</b>:\n"
                                      "   - Вставка новых данных в таблицы.\n"
                                      "   - Поддержка ввода значений по умолчанию, проверка типов данных и длины значений.\n"
                                      "\n"
                                      "4. <b>UPDATE</b>:\n"
                                      "   - Обновление существующих данных в таблицах.\n"
                                      "   - Возможность выбора таблицы, колонки и строки для обновления.\n"
                                      "   - Проверка на допустимость значений и типов данных.\n"
                                      "\n"
                                      "5. <b>DELETE</b>:\n"
                                      "   - Удаление данных из таблиц.\n"
                                      "   - Возможность удаления целых таблиц, отдельных колонок или строк по первичному ключу.\n"
                                      "   - Подтверждение удаления для предотвращения случайных действий.\n"
                                      "\n"
                                      "<b>Дополнительные функции:</b>\n"
                                      "\n"
                                      "- <b>Валидация данных</b>:\n"
                                      "  - Проверка типов данных и максимальной длины значений для вставки и обновления.\n"
                                      "  - Поддержка различных типов данных, таких как integer, numeric, boolean, date, timestamp и текстовые поля.\n"
                                      "\n"
                                      "- <b>Работа с ключами</b>:\n"
                                      "  - Выбор и использование первичных ключей для операций обновления и удаления.\n"
                                      "  - Автоматическое определение и отображение первичных ключей таблиц.\n"
                                      "\n"
                                      "<b>Пример использования</b>:\n"
                                      "- Введите команду <b>INSERT</b> для начала процесса вставки данных в таблицу.\n"
                                      "- Выберите таблицу и введите значения для каждой колонки по очереди.\n"
                                      "- Бот проверит введенные значения и вставит их в таблицу.\n"
                                      "\n"
                                      "<i>Если у вас возникли вопросы или вам нужна дополнительная помощь, обратитесь к документации или свяжитесь с поддержкой.</i>\n",
                     parse_mode='HTML', reply_markup=MyKeyboards.main())

@bot.message_handler(content_types=["text"])
def com_text(message):
    if message.text == "SELECT":
        bot.send_message(message.chat.id, "Выберите таблицу для выполнения команды SELECT.", reply_markup=MyKeyboards.tables("select"))
    elif message.text == "INSERT":
        bot.send_message(message.chat.id, "Выберите таблицу для вставки данных.", reply_markup=MyKeyboards.tables("insert"))
    elif message.text == "UPDATE":
        bot.send_message(message.chat.id, "Выберите таблицу для обновления данных.", reply_markup=MyKeyboards.tables("update"))
    elif message.text == "DELETE":
        sql_delete.start_delete(message)
    elif message.text == "Выполнить":
        msg = bot.send_message(message.chat.id, "Напиши свой запрос.")
        bot.register_next_step_handler(msg, sql_request.one)
    elif message.text == "Запросы":
        msg = bot.send_message(message.chat.id, "Запросы", reply_markup=MyKeyboards.requests(request_file))
        bot.register_next_step_handler(msg, sql_request.one, True)
    elif message.text == "Настройки":
        com_settings(message)
    elif message.text == "Помощь":
        com_help(message)

def com_settings(message):
    bot.send_message(message.chat.id, "Настройки", reply_markup=MyKeyboards.settings())

@bot.callback_query_handler(func = lambda call: call.data.startswith("settings#save") or call.data.startswith("settings#dist"))
def call_settings(call):
    if call.data == "settings#save#0":
        bot_settings.set_save(0)
    elif call.data == "settings#save#1":
        bot_settings.set_save(1)
    elif call.data == "settings#save#2":
        bot_settings.set_save(2)
    elif call.data == "settings#dist#0":
        bot_settings.set_dist(0)
    elif call.data == "settings#dist#1":
        bot_settings.set_dist(1)
    elif call.data == "settings#dist#2":
        bot_settings.set_dist(2)
    bot.edit_message_text("Настройки", call.message.chat.id, call.message.message_id, reply_markup=MyKeyboards.settings())

bot.polling()