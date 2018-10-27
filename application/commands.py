# coding=utf-8
import requests
from bs4 import BeautifulSoup
from application import bot


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['search'])
def search(message):
	#import ipdb; ipdb.set_trace()
	if len(message.text.split('/search')[1]) > 1:
		object_search = message.text.split('/search')[1]
		url = 'https://www.amazon.es/s/ref=nb_sb_noss_1?__mk_es_ES=ÅMÅŽÕÑ&url=search-alias%3Daps&field-keywords=' + object_search.encode('utf-8')
		response = requests.get(url)
		list_response_products = []
		soup = BeautifulSoup(response.content)

		products = soup.find("ul", {"id": "s-results-list-atf"})
		list_products = products.findAll("li")
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

		#bot.reply_to(message, "Precio = " + product_response['price'])
		#bot.reply_to(message, product_response['url'])
