#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os
from slackclient import SlackClient
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time
import re
import argparse

mensa_url = 'http://menu.mensen.at/index/index/locid/1'
ger_weekday = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
lets_go_msg = "let's go for lunch!"
no_food_msg = "No food found! ;-("


def _get_mensa_menu():
    r = requests.get(mensa_url)
    soup = BeautifulSoup(r.text.replace('\n', ' '), 'html.parser')
    weekday = ger_weekday[date.weekday(date.today())]
    content = [dayContent for dayContent in soup.find_all('div', 'day')
               if dayContent.find('span', 'day-of-week').string == weekday]
    if len(content) > 0:
        c = content[0]
        [x.extract() for x in c.find_all('div', {'id': ['category52', 'category15']})]
        return c
    return None


def _to_slackified_markdown(html):
    def strong(x):
        return '*' + x.strip() + '* '

    def icons(x):
        x_lower = x.lower()
        if x_lower.startswith('vegetarisch'):
            return ' :herb: (vegetarian) '
        elif x_lower.startswith('vegan'):
            return ' :seedling: (vegan) '
        elif x_lower.startswith('fisch'):
            return ' :fish: (fish) '
        return ' (' + x.replace('Icon', '').strip() + ') '
    # date
    html.find('span', 'day-of-week').extract()
    raw_date = html.find('span', 'date')
    try:
        d = datetime.strptime(raw_date.get_text(), '%d.%m.%Y').strftime('%A, %d. %B %Y')
        raw_date.extract()
    except object as e:
        raise e

    msg = strong(d)

    # remove
    for elm in html.find_all("div", {'class': ['category-border-div']}):
        elm.extract()
    # images
    for elm in html.find_all("img"):
        elm.replace_with(icons(elm['alt']))
    # strong
    for elm in html.find_all("strong"):
        elm.replace_with('\n' + strong(elm.get_text()))
    for br in html.find_all("br"):
        br.replace_with("\n")
    # headline
    for h in html.find_all('div', 'category-title'):
        h.replace_with('\n\n\n' + strong(h.get_text()) + '\n\n')
    # remove div
    for h in html.find_all(['div', 'p']):
        h.replace_with(h.get_text())
    # prettify
    text = html.get_text()
    text = re.sub(r'  *,', ',', text)
    text = re.sub(r'  *', ' ', text)
    msg += text
    return msg


class SlackPoster(object):
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel

    def post(self, msg):

        sc = SlackClient(self.token)

        result = sc.api_call(
            "chat.postMessage",
            channel=self.channel,
            text=msg,
            as_user=True,
            mrkdwn=True
        )

        if not result["ok"]:
            print(result, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slack', action='store',
                        default=None,
                        metavar='CHANNEL',
                        help='send message to slack channel')
    parser.add_argument('--lets-go', '-t', dest='timeout', metavar='N',
                        type=int, default=0,
                        help='send lets go message after N seconds')
    parser.add_argument('--format', '-f', choices=['html', 'markdown'],
                        default='markdown', help='format of message')
    args = parser.parse_args()

    html = _get_mensa_menu()

    class StdPoster(object):
        def post(self, x):
            print(x)
    poster = SlackPoster(token=os.environ["SLACK_API_TOKEN"], channel=args.slack) if args.slack else StdPoster()

    if html:
        msg = _to_slackified_markdown(html) if args.format == 'markdown' else str(html)
        poster.post(msg)
        time.sleep(args.timeout)
        poster.post(lets_go_msg)
    else:
        poster.post(no_food_msg)


if __name__ == '__main__':
    main()
