import configparser
import os
import requests
import telegram
from bs4 import BeautifulSoup
import torrent
import redis

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

# Connecting to Redis db
db = redis.StrictRedis(host=config['DB']['host'],
                       port=config['DB']['port'],
                       db=config['DB']['db'])

def getitens(search, bot, update):
    search = str(search).replace("+", "%2B").replace("!", "%21").replace("#", "%23").replace("@", "%40").replace("=",
                                                                                                                 "%3D").replace(
        " ", "+")
    page = requests.get(config['DEFAULT']['url_busca']+'?s='+search)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all(class_='blog-view')

    main_menu_keyboard = []
    for link in links:
        text = link.find("a").get_text()
        print(text)
        img = link.find('img').get('src')
        response = requests.get(img)
        path_img = str(update.message.chat_id)+'.jpg'
        print(path_img)
        f = open(path_img, 'wb')
        f.write(response.content)
        f.close()
        bot.send_photo(chat_id=update.message.chat_id, photo=open(path_img, 'rb'))
        bot.send_message(chat_id=update.message.chat_id, text=text)
        os.remove(path_img)
        main_menu_keyboard.append([telegram.KeyboardButton('/baixar ' + link.find("a").get_text())])
    return main_menu_keyboard


# def getiten(link):


def getlink(url, update, bot):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find('.entry-content.cf').find_all("a")

    main_menu_keyboard = []
    for link in links:
        if str(link.get('href')).find('magnet') >= 0:
            text = link.parent.previous_sibling.find('strong').text
            print(text)
            db.set(text, link.get('href'))
            teste = db.get(text)
            main_menu_keyboard.append([telegram.KeyboardButton(text)])
            # text += link.get('href') + "\n"
            # torrent.download(link.get('href'), "Animes", update, bot)
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                       resize_keyboard=True,
                                                       one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                         text="Selecione uma das opções",
                         reply_markup=reply_kb_markup)


def geturl(update, bot):
    search = str(update.message.text).replace("+", "%2B").replace("!", "%21").replace("#", "%23").replace("@",
                                                                                                          "%40").replace(
        "=",
        "%3D").replace(
        " ", "+")
    return config['DEFAULT']['url_busca']+'?s='+search
