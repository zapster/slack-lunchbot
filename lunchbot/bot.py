#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests

from datetime import date
from bs4 import BeautifulSoup

mensa_url = 'http://menu.mensen.at/index/index/locid/1'
ger_weekday = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
lets_go_msg = "let's go for lunch!"
no_food_msg = "No food found! ;-(\n\nVisit " + mensa_url


def _get_mensa_menu():
    r = requests.get(mensa_url)
    soup = BeautifulSoup(r.text.replace('\n', ' '), 'html.parser')
    weekday_num = date.weekday(date.today())
    for x in soup.find_all("div", {'class': "d-md-none"}):
        x.decompose()
    return soup.find_all("div", {'class': "menu-item-{}".format(weekday_num + 1)})


def post(formatter, poster, lets_go_timeout=0):
    html = _get_mensa_menu()

    if html:
        msg = formatter.format(html)
        poster.post(msg)

        # send "let's go" message
        if lets_go_timeout > 0:
            time.sleep(lets_go_timeout)
            poster.post(lets_go_msg)
    else:
        poster.post(no_food_msg)
