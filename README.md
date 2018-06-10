`slack-lunchbot` crawls the [JKU Linz Mensa menu](http://menu.mensen.at/index/index/locid/1) and posts the result to Slack or the command line.

You can deploy this bot on your local machine or in the cloud with [AWS Lambda](https://aws.amazon.com/lambda).

Local installation
==================

    git clone git@github.com:zapster/slack-lunchbot.git
    pip3 install slack-lunchbot

Usage
-----

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
00 12 * * MON-FRI /path/to/python -m lunchbot --slack $SLACK_CHANNEL -t 120
```

Assuming `SLACK_API_TOKEN` and `SLACK_CHANNEL` to be set up.

Cloud installation
==================

You can deploy `slack-lunchbot` easily into [AWS Lambda](https://aws.amazon.com/lambda) using the [serverless](https://serverless.com/) framework.
The free tier of AWS Lambda should cover everything this bot needs.

1. Install the `serverless` framework first with [npm](https://www.npmjs.com/get-npm)

        npm install -g serverless

2. Setup your AWS account and credentials. [Watch this video tutorial.](https://www.youtube.com/watch?v=HSd9uYj2LJA)

3. Add your provider credentials (in a `serverless-lunchbot` profile that will be stored in `~/.aws`)

        serverless config credentials --provider aws --profile serverless-lunchbot \
            --key AKIAIOSFODNN7EXAMPLE \
            --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

4. Clone this repository (if not done already) and install missing dependencies

        git clone git@github.com:zapster/slack-lunchbot.git
        cd slack-lunchbot
        npm install

5. Copy the `config.template.yml` to a `config.production.yml` file and add the Slack API tokens of your bot. Learn more about [bot users in Slack](https://api.slack.com/bot-users#setup).

        cp config.template.yml config.production.yml
        nano config.production.yml

    The configuration options are

    - `SLACK_API_TOKEN` of your [bot user](https://api.slack.com/bot-users#setup)
    - `SLACK_CHANNEL` to be posted, without the hash tag
    - `SCHEDULE` specifies the [schedule events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html), e.g. `cron(00 12 * * MON-FRI)` for a post from Monday - Friday at 12:00

6. Deploy to the cloud

        serverless deploy -v

7. Manually trigger your AWS Lambda function and inspect the log

        serverless invoke -f post_menu_to_slack -l

Contributing
============

If you would like to extend or change the functionality, install the package in `--editable` mode instead.
The package will then reference this local repository instead of copying all the files to your central package store.

    git clone git@github.com:zapster/slack-lunchbot.git
    pip3 install --editable slack-lunchbot
