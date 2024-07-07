from config import *


@bot.message_handler(commands=["start"])
def start(message):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    row = cur.fetchone()
    bot.send_message(message.chat.id, f"{row[0]} {row[1]}")


bot.polling()