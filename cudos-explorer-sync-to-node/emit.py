import json
import sys
import time

import requests
import warnings
import datetime

import settings
import checks


def slack(msgs: list) -> None:

    for message in msgs:
        slack_data = checks.msg_type(message)
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(settings.SLACK_WEBHOOK_URL, data=json.dumps(slack_data), headers=headers)

        # TODO: back up channel might be implemented if Slack fails
        if response.status_code != 200:
            warnings.warn(f"Error sending a sync-alert message to Slack"
                          f"@ {datetime.datetime.now()} containing: {message}")
        time.sleep(5)  # Slack requires at least 3 seconds between messages
