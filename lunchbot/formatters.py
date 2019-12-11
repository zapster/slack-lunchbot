#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import re

from datetime import date, datetime

sections_ignore = ["M-Cafe"]
sections_order = ["Menü Classic 1", "Menü Classic 2", "Tagesteller", "Choice"]


class HtmlFormatter(object):
    def format(self, html):
        print("\n".join(x.prettify() for x in html))


class MarkdownFormatter(object):
    def format(self, html):
        def strong(x):
            return ' *' + x.strip() + '* ' if len(x) > 0 else ''

        def italic(x):
            return ' _' + x.strip() + '_ ' if len(x) > 0 else ''

        def icons(x):
            x_lower = x.lower()
            if x_lower.startswith('vegetarisch'):
                return ' :herb: (vegetarian) '
            elif x_lower.startswith('vegan'):
                return ' :seedling: (vegan) '
            elif x_lower.startswith('fisch'):
                return ' :fish: (fish) '
            return ' (' + x.replace('Icon', '').strip() + ') '

        # date headline
        today = date.today().strftime("%A, %d %B %Y")
        blocks = ["> " + strong(today)]

        for div in html:

            # headline
            ignore = False
            for elm in div.find_all('h2'):
                ignore |= any(e in elm.get_text() for e in sections_ignore)
                elm.replace_with(
                    ":fork_and_knife: " + strong(elm.get_text()) + " :fork_and_knife:" + '\n')

            # drop ignored sections
            if ignore:
                elm.extract()
                continue

            # replace outer paragraphs and image links
            for elm in div.find_all('p') + div.find_all('a'):
                elm.unwrap()

            # br tags to line breaks
            for elm in div.find_all('br'):
                elm.replace_with("\n")

            # images to emojis
            for elm in div.find_all('img'):
                elm.replace_with(icons(elm['alt']))

            # strong to italic
            for elm in div.find_all('strong'):
                elm.replace_with(italic(elm.get_text()))

            text = div.get_text()

            # extract inner menus and visually separate them (assuming that menues are ended by a proper price tag and formatted italic)
            text = re.sub(r'(.+?_€\s?\d{1,2}(?:,\d{1,2})?_)', r' \1\n', text)

            # trim leading and trailing whitespace and double-or-more spaces
            text = re.sub(r'^\s+', '', text)
            text = re.sub(r'\s+$', '', text)
            text = re.sub(r'[^\S\r\n]{2,}', r' ', text)

            blocks.append(text)

        # sort by using the index of where in the order list a phrase has been matched
        def _sorter(txt):
            return next((i for i, key in enumerate(sections_order) if key in txt), -1)

        result = '\n\n'.join(sorted(blocks[1:], key=_sorter))
        result = blocks[0] + '\n\n' + result

        return result
