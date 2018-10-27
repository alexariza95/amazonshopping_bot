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
        click_button = InlineKeyboardButton(name_category, callback_data='parent_' + name_category)
        click_kb.row(click_button)
    bot.send_message(message.chat.id, "<b>Aquí se muestran todos los departamentos de Amazon...</b>",
     parse_mode="HTML", reply_markup=click_kb, disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("parent_"):
        #mandar categorias hijos
        response = requests.get("https://www.amazon.es/gp/site-directory?ref=nav_shopall_btn", allow_redirects = True)
        list_message = call.data.split("parent_")
        name_category = list_message[1]
        soup = BeautifulSoup(response.content)
        category = soup.find("h2", text=name_category)
        parent_div = category.parent()[1]
        subcategories = parent_div.findAll("a", {"class":"nav_a"})
        click_kb = InlineKeyboardMarkup()
        for subcategory in subcategories:
            name_subcategory = subcategory.get_text()
            click_button = InlineKeyboardButton(name_subcategory, callback_data='subcategory_' + name_subcategory)
            click_kb.row(click_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Haz click en lo que desees", reply_markup=click_kb)
        #import ipdb; ipdb.set_trace()

    else:
        response = requests.get("https://www.amazon.es/gp/site-directory?ref=nav_shopall_btn", allow_redirects = True)
        list_message = call.data.split("subcategory_")
        name_category = list_message[1]
        soup = BeautifulSoup(response.content)
        subcategory = soup.find("a", text=name_category)
        href = subcategory['href']
        response = requests.get("https://amazon.es" + href)
        soup = BeautifulSoup(response.content)
