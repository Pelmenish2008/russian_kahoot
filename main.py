from collections import defaultdict
import telebot
from config import token
from telebot import types


user_responses = {}
points = defaultdict(int)


quiz_questions = [
    {"text": "Завтра в школу?", "answer_id": 0,
     "options": ["Увы, да", "Обязательно", "Нет",]},
    {"text": "Лучший ранг в доте?", "answer_id": 2,
     "options": ["Бомжество", "Титян", "Рекрут"]},
    {"text": "Самый лучший игрок в доту?", "answer_id": 2,
    "options": ["ЯТОГОРОТ","9класс","Я"]}
]

def gen_markup(options):
    markup = types.InlineKeyboardMarkup()
    for index, options in enumerate(options):
        markup.add(types.InlineKeyboardButton(text=options,callback_data=str(index)))
    return markup

bot = telebot.TeleBot(token)


def send_question(chat_id):
    question = quiz_questions[user_responses[chat_id]]
    bot.send_message(chat_id, question["text"], reply_markup=gen_markup(question["options"]))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    selected_option_index = int(call.data)
    question = quiz_questions[user_responses[call.message.chat.id]]
    correct_answer_index = question["answer_id"]

    if selected_option_index == correct_answer_index:
        bot.answer_callback_query(call.id, "Правильно!")
        points[call.message.chat.id] += 1
    else:
        bot.answer_callback_query(call.id, "Неправильно")

    user_responses[call.message.chat.id] += 1

    if user_responses[call.message.chat.id] < len(quiz_questions):
        send_question(call.message.chat.id)
    else:
        bot.send_message(call.message.chat.id, f" Вы набрали {points[call.message.chat.id]} очков")

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in user_responses:
        user_responses[message.chat.id] = 0
        send_question(message.chat.id)



bot.polling(none_stop=True)



