from config import *
import MyKeyboards
import re

@bot.message_handler(commands=["start"])
def com_start(message):
    bot.send_message(message.chat.id, "Hello", reply_markup=MyKeyboards.main())


@bot.message_handler(content_types=["text"])
def com_text(message):
    if message.text == "SELECT":
        bot.send_message(message.chat.id, "SELECT", reply_markup=MyKeyboards.tables())
    elif message.text == "INSERT":
        bot.send_message(message.chat.id, "INSERT", reply_markup=MyKeyboards.tables())
    elif message.text == "UPDATE":
        bot.send_message(message.chat.id, "UPDATE", reply_markup=MyKeyboards.tables())
    elif message.text == "DELETE":
        bot.send_message(message.chat.id, "DELETE", reply_markup=MyKeyboards.tables())

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def call_select(call):
    if len(call.data.split("@")) == 1:
        table = call.data.split("_")[1]
        bot.send_message(call.message.chat.id, "SELECT", reply_markup=MyKeyboards.columns(table))
    else:
        table = re.sub("select_", "", call.data).split("@")[0]
        column = re.sub("select_", "", call.data).split("@")[1]
        cur = conn.cursor()
        cur.execute("SELECT " + column + " FROM " + table)
        rows = cur.fetchall()

        table_str = convert_list_to_str(rows, cur)
        bot.send_message(call.message.chat.id, f"<pre>{table_str}</pre>", parse_mode='HTML')

    # table = call.data.split("_")[1]
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM " + table)
    # rows = cur.fetchall()
    #


bot.polling()