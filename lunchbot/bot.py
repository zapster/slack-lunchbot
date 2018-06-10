#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests

from datetime import date
from bs4 import BeautifulSoup

mensa_url = 'http://menu.mensen.at/index/index/locid/1'
ger_weekday = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
lets_go_msg = "let's go for lunch!"
no_food_msg = "No food found! ;-("


def _get_mensa_menu():
    r = requests.get(mensa_url)
    soup = BeautifulSoup(r.text.replace('\n', ' '), 'html.parser')
    weekday = ger_weekday[date.weekday(date.today())]
    content = [dayContent for dayContent in
               soup.find_all('div', 'day')
               if dayContent.find('span', 'day-of-week').string == weekday]

    if len(content) > 0:
        c = content[0]
        [x.extract() for x in
         c.find_all('div', {'id': ['category52', 'category15']})]
        return c
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
