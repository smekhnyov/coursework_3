from config import *


@bot.message_handler(commands=["start"])
def start(message):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    row = cur.fetchone()
    bot.send_message(message.chat.id, f"{row[1]} {row[2]}")


bot.polling()