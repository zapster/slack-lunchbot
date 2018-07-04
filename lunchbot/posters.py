#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

from slackclient import SlackClient


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


class ConsolePoster(object):
    def post(self, msg):
        print(msg)
