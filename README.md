Requirements
============

Python packages (install via `pip install`):
* `slackclient`
* `bs4`
* `request`

Usage
=====

See `--help` message. In Slack mode the API token is expected in the `SLACK_API_TOKEN` environment variable.

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
18 12 * * MON-FRI path/to/python path/to/bot.py --slack $SLACK_CHANNEL -t 120

```

Assuming `SLACK_API_TOKEN` and `SLACK_CHANNEL` to be set up.
