#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests

from datetime import date
from bs4 import BeautifulSoup

mensa_url = 'https://www.mensen.at/'
mensa_id = 1  # JKU Linz Mensa

lets_go_msg = "let's go for lunch!"
no_food_msg = "No food found! ;-(\n\nVisit " + mensa_url


def _get_mensa_menu():
    r = requests.get(mensa_url, cookies={'mensenExtLocation': str(mensa_id)})
    soup = BeautifulSoup(r.text.replace('\n', ' '), 'html.parser')
    weekday = date.weekday(date.today()) + 1
    divs = soup.find_all('div', 'menu-item-{}'.format(weekday))

    if len(divs) > 0:

        # clean divs with duplicate content
        menus = {}
        for div in divs:
            if div.get_text() not in menus:
                menus[div.get_text()] = div

        return menus.values() if len(menus.values()) > 0 else None

    return None


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
