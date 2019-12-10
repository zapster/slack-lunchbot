#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import re

from datetime import date, datetime


class HtmlFormatter(object):
    def format(self, html):
        print("\n".join(x.prettify() for x in html))


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

        def cmp(elm):
            header = elm.find("h2")
            if header:
                text = header.get_text()
                if text.lower().startswith("choice"):
                    # choice last
                    return "XXXX" + text
                return text
            return "ZZZZ"

        def do(html):
            if any(x.get_text() == "M-Cafe" for x in html.find_all("h2")):
                # ignore M-Cafe
                return ""

            # images
            for elm in html.find_all("img"):
                elm.replace_with(icons(elm['alt']))
            # strong
            for elm in html.find_all("strong"):
                elm.replace_with(strong(elm.get_text()))
            for br in html.find_all("br"):
                br.replace_with("\n")
            # headline
            for h in html.find_all('h2'):
                h.replace_with('\n\n\n' + strong(h.get_text()) + '\n\n')
            # remove div
            for h in html.find_all(['div', 'p']):
                h.replace_with(h.get_text() + '\n')
            # prettify
            text = html.get_text()
            text = re.sub(r'  *,', ',', text)
            text = re.sub(r'  *', ' ', text)
            return text
        return str("\n".join([do(x) for x in sorted(html, key=cmp)]))
