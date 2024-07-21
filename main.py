from config import *
import MyKeyboards
import re
import sql_insert
import sql_select
import sql_update

@bot.message_handler(commands=["start"])
def com_start(message):
    bot.send_message(message.chat.id, "Hello", reply_markup=MyKeyboards.main())


@bot.message_handler(content_types=["text"])
def com_text(message):
    if message.text == "SELECT":
        bot.send_message(message.chat.id, "SELECT", reply_markup=MyKeyboards.tables("select"))
    elif message.text == "INSERT":
        bot.send_message(message.chat.id, "INSERT", reply_markup=MyKeyboards.tables("insert"))
    elif message.text == "UPDATE":
        bot.send_message(message.chat.id, "UPDATE", reply_markup=MyKeyboards.tables("update"))
    elif message.text == "DELETE":
        bot.send_message(message.chat.id, "DELETE", reply_markup=MyKeyboards.tables())


bot.polling()