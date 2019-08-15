import os, sys, logging, json, time, re, asyncio, discord
from pypresence import Presence
from datetime import datetime, date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



CLIENT_ID = '605777168739598338'
RPC = Presence(CLIENT_ID)
RPC.connect()


clear = lambda: os.system('cls')
clear()


def discord_music_from_yt(url=None):
    if not url:
        url = "https://www.youtube.com/watch?v=PJtRYr0LA1o&list=PLvys12XuukCDtbwQ4rx76gwFz5-mFLiKn"

    options = Options()
    options.add_argument('--enable-sync')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    prev_title = ""
    start_time = int(time.time())
    while True:
        time.sleep(5)
        try:
            source = driver.page_source
            c_url = driver.current_url
            if re.match("http[s]?://(www.)?youtube.com[.]*", c_url):
                soup = BeautifulSoup(source)
                sup = soup.find('div', {'id': 'movie_player'})
                ad_classes = ["ad-showing", "ad-interrupting"]
                p_class = sup.get("class")
                if any(ad_class in p_class for ad_class in ad_classes):
                    continue
                title = sup.find('div', {'class': 'ytp-title-text'}).find('a', {'target': '_blank'}).contents[0]
            elif re.match("http[s]?://(www.)?soundcloud.com[.]*", c_url):
                soup = BeautifulSoup(source)
                title = soup.find('div', {'class': 'playbackSoundBadge__title'}).find('a').get("title", "Unknown song")
            else:
                print("Unknown source")
                continue


            if title != prev_title:
                prev_title = title
                start_time = int(time.time())
            RPC.update(
                details=title,
                start=start_time,
                large_image="ava"
            )
        except:
            pass


if __name__ == "__main__":
    url = input("Input url: ")
    discord_music_from_yt(url)
