import telegram
import configparser
import torrent
import buscaTorrent
import redis
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# from pprint import pprint

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

chat_commands = {}

CHAVE_API = config['DEFAULT']['token']

# Connecting to Telegram API
# Updater retrieves information and dispatcher connects commands
updater = Updater(token=CHAVE_API)
dispatcher = updater.dispatcher

# Connecting to Redis db
db = redis.StrictRedis(host=config['DB']['host'],
                       port=config['DB']['port'],
                       db=config['DB']['db'])


def atualizacaoStatus(bot, update, texto):
    print(bot.get_me())
    bot.send_message(update.message.chat_id, texto)


def mandafoto(bot, update):
    buscaTorrent.geturl(update, bot)


baixar_magnet_handler = CommandHandler('manda_foto', mandafoto)
dispatcher.add_handler(baixar_magnet_handler)


def download(bot, update):

    if update.message.text.replace("/baixar", "") != "":
        torrent.download(update.message.text.replace("/baixar ", ""), "Filme", update.message, bot)
    else:
        chat_commands[update.message.chat_id] = 'baixar'
        bot.reply_to(update.message, "Por favor coloque o link magnético que deseja baixar")


baixar_magnet_handler = CommandHandler('baixar', download)
dispatcher.add_handler(baixar_magnet_handler)


def downloadmagnet(bot, update):
    if update.message.text.replace("/baixar_magnet", "") != "":
        bot.reply_to(update.message, "Okay, vou começar a baixar")
        torrent.download(update.message.text.replace("/baixar_magnet ", ""), "Filme", update.message, bot)
    else:
        chat_commands[update.message.chat_id] = 'baixar_magnet'
        bot.reply_to(update.message, "Por favor coloque o link magnético que deseja baixar")


baixar_magnet_handler = CommandHandler('baixar_magnet', downloadmagnet)
dispatcher.add_handler(baixar_magnet_handler)


def downloadlink(bot, update):
    if update.message.text.replace("/baixar_link", "") != "":
        buscaTorrent.getlink(update.message.text.replace("/baixar_link ", ""), update, bot)
    else:
        chat_commands[update.message.chat_id] = 'baixar_link'
        bot.send_message(chat_id=update.message.chat_id, text="Por favor coloque o link que deseja baixar",
                         reply_to_message_id=update.message.message_id)


baixar_link_handler = CommandHandler('baixar_link', downloadlink)
dispatcher.add_handler(baixar_link_handler)


def search(bot, update):
    if update.message.text.replace("/buscar", "") != "":
        buttons = buscaTorrent.getitens(update.message.text.replace("/buscar ", ""), bot, update)
        if not buttons:
            text = "Nenhum resultado encontrado para essa busca"
        else:
            text = "Selecione uma das opções para baixar"

        reply_kb_markup = telegram.ReplyKeyboardMarkup(buttons,
                                                       resize_keyboard=True,
                                                       one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         reply_to_message_id=update.message.message_id,
                         reply_markup=reply_kb_markup)
    else:
        chat_commands[update.message.chat_id] = 'buscar'
        bot.send_message(chat_id=update.message.chat_id, text="Por favor digite a sua busca",
                         reply_to_message_id=update.message.message_id)


buscar_handler = CommandHandler('buscar', search)
dispatcher.add_handler(buscar_handler)


def verificar():
    return True


def responder(bot, update):
    if chat_commands[update.message.chat_id] == "baixar_link":
        chat_commands[update.message.chat_id] = ''
        downloadlink(bot, update)
    else:
        if chat_commands[update.message.chat_id] == "buscar":
            chat_commands[update.message.chat_id] = ''
            search(bot, update)
        else:
            if chat_commands[update.message.chat_id] == "baixar_magnet":
                print('')
            else:
                if chat_commands[update.message.chat_id] == "baixar":
                    print('')
                else:
                    texto = """
                    Escolha um comando para usar:
                    /buscar Verifica se o filme ou série está disponivel para baixar
                    /baixar Digite o nome do filme ou série para baixar
                    /baixar_link Coloque o link de onde o torrent está armazenado para poder baixar
                    /baixar_magnet Coloque o link exato do filme ou série para baixar diretamente(Melhor Opção)
                    """
                    main_menu_keyboard = [[telegram.KeyboardButton('/buscar')],
                                          [telegram.KeyboardButton('/baixar')],
                                          [telegram.KeyboardButton('/baixar_link')],
                                          [telegram.KeyboardButton('/baixar_magnet')]
                                          ]
                    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                                   resize_keyboard=True,
                                                                   one_time_keyboard=True)
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=texto,
                                     reply_markup=reply_kb_markup)


responder_handler = MessageHandler([Filters.text], responder)
dispatcher.add_handler(responder_handler)

start_handler = CommandHandler('start', responder)
dispatcher.add_handler(start_handler)


def polling():
    updater.start_polling()
