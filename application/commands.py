# coding=utf-8
from application import bot
import requests
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Bienvenido, ' + message.from_user.first_name + ' !!!')


@bot.message_handler(commands=['departments'])
def departments(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    response = requests.get("https://www.amazon.es/gp/site-directory?ref=nav_shopall_btn", allow_redirects = True)
    soup = BeautifulSoup(response.content)
    categories = soup.findAll("h2",{"class":"popover-category-name"})
    for category in categories:
        name_category = category.get_text()
        callback_name = name_category
        markup.add(InlineKeyboardButton(name_category, callback_data=f"cb_yes"),)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    pass
