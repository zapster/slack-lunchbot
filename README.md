`slack-lunchbot` crawls the [JKU Linz Mensa menu](http://menu.mensen.at/index/index/locid/1) and posts the result to Slack or the command line.

Installation
=====

    git clone git@github.com:zapster/slack-lunchbot.git
    pip3 install slack-lunchbot

Usage
=====

    lunchbot --help

See `--help` message. In Slack mode the API token is expected in the `SLACK_API_TOKEN` environment variable.

If you don't want to install this module to your local system, invoke it like this:

    PYTHONPATH=/path/to/slack-lunchbot /path/to/python -m lunchbot --help

Cron Job Example
----------------

Post in `SLACK_CHANNEL` from Monday-Friday at 12:18 and send "let's got" two minutes later.

```
#┌─────────── minute (0 - 59)
#│  ┌──────── hour (0 - 23)
#│  │ ┌────── day of month (1 - 31)
#│  │ │ ┌──── month (1 - 12)
#│  │ │ │ ┌── day of week (0 - 6 => Sunday - Saturday, or
#│  │ │ │ │                1 - 7 => Monday - Sunday)
#↓  ↓ ↓ ↓ ↓
18 12 * * MON-FRI /path/to/python -m lunchbot --slack $SLACK_CHANNEL -t 120
```

Assuming `SLACK_API_TOKEN` and `SLACK_CHANNEL` to be set up.

Contributing
============

If you would like to extend or change the functionality, install the package in `--editable` mode instead.
The package will then reference this local repository instead of copying all the files to your central package store.

    git clone git@github.com:zapster/slack-lunchbot.git
    pip3 install --editable slack-lunchbot
