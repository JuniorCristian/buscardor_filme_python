import telebot
import telegram
import torrent
import buscaTorrent
import configparser

import redis

from telegram.ext import Updater

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

CHAVE_API = config['DEFAULT']['token']

# # Connecting to Telegram API
# # Updater retrieves information and dispatcher connects commands
# updater = Updater(token=config['DEFAULT']['token'])
# dispatcher = updater.dispatcher
#
# # Connecting to Redis db
# db = redis.StrictRedis(host=config['DB']['host'],
#                        port=config['DB']['port'],
#                        db=config['DB']['db'])

bot = telebot.TeleBot(CHAVE_API)


def atualizacaoStatus(mensagem, texto):
    bot.send_message(mensagem.chat.id, texto)


@bot.message_handler(commands=['baixar_magnet'])
def searchlink(mensagem):
    bot.reply_to(mensagem, "Okay, vou começar a baixar")
    torrent.download(mensagem.text.replace("/baixar_magnet ", ""), "Filme", mensagem)


@bot.message_handler(commands=['baixar_link'])
def searchlink(mensagem):
    if (mensagem != ""):
        buscaTorrent.getlink(mensagem.text.replace("/baixar_link ", ""), mensagem)


@bot.message_handler(commands=['buscar'])
def search(mensagem):
    text = buscaTorrent.getitens(mensagem.text.replace("/buscar ", ""))
    if (text == ""):
        text = "Nenhum resultado encontrado para essa busca"
    bot.reply_to(mensagem, text)


def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha um comando para usar:
    /buscar Verifica se o filme ou série está disponivel para baixar
    /baixar Digite o nome do filme ou série para baixar
    /baixar_link Coloque o link de onde o torrent está armazenado para poder baixar
    /baixar_magnet Coloque o link exato do filme ou série para baixar diretamente(Melhor Opção)
    """
    main_menu_keyboard = [[telegram.KeyboardButton('/buscar')],
                          [telegram.KeyboardButton('/baixar_link')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)
    print(reply_kb_markup)
    bot.reply_to(mensagem, reply_kb_markup)


def polling():
    bot.polling()