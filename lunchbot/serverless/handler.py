#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

from datetime import date

# hotfix the path, when this is called as a script by aws
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bot import post
from posters import SlackPoster
from formatters import MarkdownFormatter


def post_menu_to_slack(event, context):
    # avoid posting on weekends since the timezone cron schedule doesn't support specifying weekdays
    # https://github.com/UnitedIncome/serverless-local-schedule/issues/3
    if date.weekday(date.today()) in [5, 6]:
        return {
            "statusCode": 200,
            "body": "Postings on weekends are disabled in lunchbot.serverless.handler.post_menu_to_slack"
        }

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
