# coding=utf-8
from application import bot
import requests
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Bienvenido, ' + message.from_user.first_name + ' !!!')


@bot.message_handler(commands=['search_cheaper'])
def search_cheaper(message):
    if len(message.text.split('/search_cheaper')[1]) > 1:
        object_search = message.text.split('/search_cheaper')[1]
        url = 'https://www.amazon.es/s/ref=sr_st_price-asc-rank?keywords=' + object_search.encode(encoding='utf-8', errors='strict') + '&rh=i%3Aaps%2Ck%3Afundas&__mk_es_ES=%C3%85M%C3%85Z%C3%95%C3%91&qid=1540914465&sort=price-asc-rank'
        response = requests.get(url)
        list_response_products = []
        soup = BeautifulSoup(response.content)

        products = soup.find("ul", {"id": "s-results-list-atf"})
        list_products = products.find_all("li")
        for product in list_products:
            price = product.find("span", {"class": "a-size-base a-color-price s-price a-text-bold"})
            if hasattr(price, 'text'):
                price = price.text
                url = product.find("a", {"a-link-normal a-text-normal"})
                url = url['href']
                list_response_products.append({'url':url, 'price':price})
        html = ''
        for product_response in list_response_products:
            html += ' Precio: %s \n Url: %s ' % (product_response['price'], product_response['url'],)

        bot.send_message(message.chat.id, html, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, 'Por favor, escribe /search_cheaper Producto', parse_mode="HTML")

@bot.message_handler(commands=['search'])
def search(message):
	#import ipdb; ipdb.set_trace()
	if len(message.text.split('/search')[1]) > 1:
		object_search = message.text.split('/search')[1]
		url = 'https://www.amazon.es/s/ref=nb_sb_noss_1?__mk_es_ES=ÅMÅŽÕÑ&url=search-alias%3Daps&field-keywords=' + object_search.encode(encoding='utf-8', errors='strict')
		response = requests.get(url)
		list_response_products = []
		soup = BeautifulSoup(response.content)

		products = soup.find("ul", {"id": "s-results-list-atf"})
		list_products = products.find_all("li")
		for product in list_products:
			price = product.find("span", {"class": "a-size-base a-color-price s-price a-text-bold"})
			if hasattr(price, 'text'):
				price = price.text
				url = product.find("a", {"a-link-normal a-text-normal"})
				url = url['href']
				list_response_products.append({'url':url, 'price':price})
		html = ''
		for product_response in list_response_products:
			html += ' Precio: %s \n Url: %s ' % (product_response['price'], product_response['url'],)

		bot.send_message(message.chat.id, html, parse_mode="HTML")
	else:
		bot.send_message(message.chat.id, 'Por favor, escribe /search Producto', parse_mode="HTML")



@bot.message_handler(commands=['departments'])
def departments(message):
    response = requests.get("https://www.amazon.es/gp/site-directory?ref=nav_shopall_btn", allow_redirects = True)
    soup = BeautifulSoup(response.content)
    categories = soup.findAll("h2",{"class":"popover-category-name"})
    click_kb = InlineKeyboardMarkup()
    list_categories = []
    i = 0
    for category in categories:
        i += 1
        name_category = category.get_text()
        click_button = InlineKeyboardButton(name_category, callback_data='parent_' + name_category)
        list_categories.append(click_button)
        if i % 2 == 0:
            click_kb.row(*list_categories)
            list_categories = []
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
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id
        , text = 'https://www.amazon.es' + href, parse_mode="HTML")
