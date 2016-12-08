# -*- coding: utf-8 -*-
import array
import telebot
from datetime import date, time
import sys
import const
from telebot import types
import logging
import exel
import os
import time
import shutil
import urllib

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

def update_time_table():
    print ("updating local time_table file")
    try:
        print ("last update time", os.path.getmtime(const.name_exel))
        print ("current time", time.time())
        if abs(time.time() - os.path.getmtime(const.name_exel)) < 24 * 60 * 60:
            print ("local file is up to date")
            return 1
        print ("file may be out of date, downloading")
    except FileNotFoundError:
        print ("local file not found, downloading")
    try:
        localFilename, headers = urllib2.urlretrieve(const.url_exel, )
    except urllib.error.HTTPError:
        print ("warning, can't update local copy, it may be non actual")
        return 0
    fromFile = localFilename
    toFile = const.name_exel
    shutil.copy(fromFile, toFile)
    print ("downloading done")
    return 1

@bot.message_handler(commands=["table_offline"])  # Офлайн расписание
def table_offline(message):
    keyboard = types.InlineKeyboardMarkup()
    url = const.url_pic_download
    try:
        localFilename, headers = urllib2.urlretrieve(url, )
        #print (localFilename)
        img = open(localFilename, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img)
        img.close()
        url_button = types.InlineKeyboardButton(text="Расписание офлайн",
                                                url=const.url_exel)
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Нажми на кнопку и скачай ", reply_markup=keyboard)
    except AttributeError:
        print ("can't download :(")

global group_name_
group_name_ = 'None'
global flag
flag = 0

@bot.message_handler(commands=["setGroup"])  # выбокра
def callback_data(message0):
    global flag
    bot.send_message(message0.chat.id, "Введите вашу группу в формате: (сам что-нибудь придумай)")
    flag = 1

@bot.message_handler(content_types=["text"])
def handle_text(msg):
    global flag, group_name_
    #print (flag)
    if flag == 1:
        #print (msg.text)
        if exel.getTimeTable(msg.text, const.name_exel, 0)[1]:
            group_name_ = msg.text
            bot.send_message(msg.chat.id, "ok. Введенная группа найдена")
            bot.send_message(msg.chat.id, "Теперь Вы можете спросить расписание на:\n" + const.timeTableAnons)
        else:
            bot.send_message(msg.chat.id, '\
Группа не найдена в таблице, пожалуйста \
введите верное название -- снова введите команду /setGroup \
или скачайте расписание (/table_offline)\
            ')
        flag = 0
        return
    if group_name_ == "None":
        bot.send_message(msg.chat.id, "Пожалуйста, установите Вашу группу (команда /setGroup)")
        return
    bot.send_message(msg.chat.id, "Ваша группа: " + group_name_)
    if group_name_ != "None":
        if "1" <= msg.text <= "8" and len(msg.text) == 1:
            if not update_time_table():
                bot.send_message(msg.chat.id, '\
                    WARNING: копию расписания на сервере не удалось обновить, \
                    возможно показанная информация не соответствует действительности\
                ')
            bot.send_message(msg.chat.id, exel.getTimeTable(group_name_, const.name_exel, int(msg.text))[0])
        else:
            bot.send_message(msg.chat.id, "введен неверный день недели")   
    else:
        bot.send_message(msg.chat.id, "пожалуйста воспользуйтесь одной из предложенных команд (/help)")

if __name__ == '__main__':
    update_time_table()
    bot.polling(none_stop=True)


"""
ПИН-Б-0-Д-2013-1
ТЕХ-Б-1-Д-2013-1
ВОД-2015-1
"""