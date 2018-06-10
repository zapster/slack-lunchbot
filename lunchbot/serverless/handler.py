#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests

# hotfix the path, when this is called as a script by aws
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bot import post
from posters import ConsolePoster, SlackPoster
from formatters import HtmlFormatter, MarkdownFormatter


def post_menu_to_slack(event, context):
    formatter = MarkdownFormatter()
    poster = SlackPoster(os.environ["SLACK_API_TOKEN"],
                         os.environ["SLACK_CHANNEL"])
    post(formatter, poster)

    body = {
        "message": "Message posted to #{}".format(poster.channel),
        "input": event
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
