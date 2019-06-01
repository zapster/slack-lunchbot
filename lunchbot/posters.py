#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import slack


class SlackPoster(object):
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel

    def post(self, msg):
        client = slack.WebClient(self.token)
        result = client.chat_postMessage(
            channel=self.channel,
            text=msg,
            as_user=True,
            mrkdwn=True
        )

        if not result["ok"]:
            print(result, file=sys.stderr)


class ConsolePoster(object):
    def post(self, msg):
        print(msg)
