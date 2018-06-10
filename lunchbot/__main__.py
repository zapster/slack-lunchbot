#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

from .bot import post
from .posters import ConsolePoster, SlackPoster
from .formatters import HtmlFormatter, MarkdownFormatter


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slack', action='store',
                        default=None,
                        metavar='CHANNEL',
                        help='send message to slack channel')
    parser.add_argument('--format', '-f', choices=['html', 'markdown'],
                        default='markdown', help='format of message')
    parser.add_argument('--lets-go', '-t', dest='timeout', metavar='N',
                        type=int, default=0,
                        help='send lets go message after N seconds')
    args = parser.parse_args()

    formatter = MarkdownFormatter() if args.format == 'markdown' \
        else HtmlFormatter()
    poster = SlackPoster(os.environ["SLACK_API_TOKEN"], args.slack) if args.slack \
        else ConsolePoster()
    post(formatter, poster, lets_go_timeout=args.timeout)


if __name__ == "__main__":
    cli()
