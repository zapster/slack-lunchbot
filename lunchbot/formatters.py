#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import re

from datetime import date, datetime


class HtmlFormatter(object):
    def format(self, html):
        print(html)


class MarkdownFormatter(object):
    def format(self, html):
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
        d = datetime.strptime(raw_date.get_text(),
                              '%d.%m.%Y').strftime('%A, %d. %B %Y')
        raw_date.extract()

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
