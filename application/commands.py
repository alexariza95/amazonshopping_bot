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
    response = requests.get("https://www.amazon.es/gp/site-directory?ref=nav_shopall_btn", allow_redirects = True)
    soup = BeautifulSoup(response.content)
    categories = soup.findAll("h2",{"class":"popover-category-name"})
    click_kb = InlineKeyboardMarkup()
    for category in categories:
        name_category = category.get_text()
        click_button = InlineKeyboardButton(name_category, callback_data='clicked')
        click_kb.row(click_button)
    bot.send_message(message.chat.id, "<b>Hey friend...</b>", parse_mode="HTML", reply_markup=click_kb, disable_web_page_preview=True)
