from config import token
import telebot


bot = telebot.TeleBot(token)


def check(password):
    if len(password) < 8:
        return "Пароль слишком короткий"
    for i in password:
        if i.isdigit() == True:
            return "Пароль надежный"
    return "Нет цифр"

@bot.message_handler(commands=['validate'])
def handle_validate(message):
    mess = str(message)
    password = message.text.split()[1]
    bot.send_message(message.chat.id, password)

bot.polling()
