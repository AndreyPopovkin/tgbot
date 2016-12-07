# -*- coding: utf-8 -*-
import array
import telebot
from datetime import date, time
import sys
import const
from telebot import types
import logging
import exel

version = sys.version_info[0]

if version == 3:
    import urllib.request as urllib2
else:
    import urllib2

bot = telebot.TeleBot(const.token)  # poluchenie tokena

print (bot.get_me())  # vivod informacii o bote

# настройки для журнала
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('someTestBot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


@bot.message_handler(commands=['start', 'help'])  # privetstvie
def send_welcome(start):
    bot.send_message(start.chat.id, const.helo_text)



@bot.message_handler(commands=["table_offline"])  # Офлайн расписание
def table_offline(message):
    keyboard = types.InlineKeyboardMarkup()
    url = const.url_pic_download
    try:
        urllib2.urlretrieve(url, )
        img = open(const.name_pic_download, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img)
        img.close()
        url_button = types.InlineKeyboardButton(text="Расписание офлайн",
                                                url=const.url_exel)
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Нажми на кнопку и скачай ", reply_markup=keyboard)
    except AttributeError:
        print ("can't download :(")

global relay
relay = ['None', 'None', 'None']

@bot.message_handler(commands=["table"])  # выбокра
def callback_data(message0):
    global relay
    relay = ['None', 'None', 'None']

    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="ВОД", callback_data="ВОД")
    button1 = types.InlineKeyboardButton(text="ПИН", callback_data="ПИН")
    keyboard.add(button, button1)
    bot.send_message(message0.chat.id, "Привет! Нажми на кнопку и... ИДИ НАХУЙ, ПИДР", reply_markup=keyboard)

    keyboard1 = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="2016", callback_data="2016")
    button1 = types.InlineKeyboardButton(text="2015", callback_data="2015")
    keyboard1.add(button, button1)
    bot.send_message(message0.chat.id, "Привет! Нажми на кнопку и... ИДИ НАХУЙ, ПИДР", reply_markup=keyboard1)

    keyboard2 = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="1", callback_data="1")
    button1 = types.InlineKeyboardButton(text="2", callback_data="2")
    keyboard2.add(button, button1)
    bot.send_message(message0.chat.id, "Привет! Нажми на кнопку и... ИДИ НАХУЙ, ПИДР", reply_markup=keyboard2)


@bot.callback_query_handler(func=lambda call: True)
def callback_1(call):
    global relay

    formatted_data = call.data
    print (formatted_data)
    if formatted_data == "ВОД" or formatted_data == "ПИН":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data)
        const.kod = call.data
        relay[0] = call.data
    elif formatted_data == "2016" or formatted_data == "2015":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data)
        const.god = call.data
        relay[1] = formatted_data
    elif formatted_data == "1" or formatted_data == "2":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data)
        const.group = call.data
        relay[2] = formatted_data
    else:
        print ("something unexpected callback")

    if relay[0] != "None" and relay[1] != "None" and relay[2] != "None":
        response = '''Выберите день недели:
                        1. Понедельник
                        2. Вторник
                        3. Среда
                        4. Четверг
                        5. Пятница
                        6. Суббота
                        7. Сегодня
                        8. Завтра
                    '''
        bot.send_message(call.message.chat.id, response)

@bot.message_handler(commands=["lol"])
def sumcod(sum):
    response = (const.kod, const.god, const.group)
    bot.send_message(sum.chat.id, response)

@bot.message_handler(content_types=["text"])
def handle_text(msg):
    if relay[0] != "None" and relay[1] != "None" and relay[2] != "None":
        if "1" <= msg.text <= "8" and len(msg.text) == 1:
            group_name = relay[0] + '-' + relay[1] + '-' + relay[2]
            bot.send_message(msg.chat.id, exel.getTimeTable(group_name, const.name_exel, int(msg.text)))
        else:
            bot.send_message(msg.chat.id, "введен неверный день недели")   
    else:
        bot.send_message(msg.chat.id, "пожалуйста воспользуйтесь одной из предложенных команд (/help)")

if __name__ == '__main__':
    bot.polling(none_stop=True)
