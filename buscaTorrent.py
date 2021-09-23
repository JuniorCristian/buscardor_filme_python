import os
import requests
from bs4 import BeautifulSoup
import torrent


def getitens(search):
    search = str(search).replace("+", "%2B").replace("!", "%21").replace("#", "%23").replace("@", "%40").replace("=", "%3D").replace(" ", "+")
    page = requests.get('https://pirate-filmes.org/?s='+search)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all(class_='entry-title')

    text = ""
    for link in links:
        text += link.find("a").get_text()+"\n"
    return text


def getlink(url, update, bot):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all("a")

    text = ""
    for link in links:
        if(str(link.get('href')).find('magnet') >= 0):
            text += link.get('href') + "\n"
            torrent.download(link.get('href'), "Animes", update, bot)
    return text