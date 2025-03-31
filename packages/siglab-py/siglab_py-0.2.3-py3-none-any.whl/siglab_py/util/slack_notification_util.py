'''
https://medium.com/@natalia_assad/how-send-a-table-to-slack-using-python-d1a20b08abe0
'''
import sys
from typing import Any, Dict
import json
import requests

from siglab_py.constants import LogLevel

def slack_dispatch_notification(
        title : str,
        message : str,
        footer : str,
        params : Dict[str, Any],
        log_level : LogLevel = LogLevel.INFO
):
    slack_params = params['slack']

    if log_level==LogLevel.INFO or log_level==LogLevel.DEBUG:
        webhook_url = slack_params['info']['webhook_url']
    elif log_level==LogLevel.ERROR or  log_level==LogLevel.CRITICAL:
        webhook_url = slack_params['critical']['webhook_url']
    elif log_level==LogLevel.ERROR or  log_level==LogLevel.CRITICAL:
        webhook_url = slack_params['alert']['webhook_url']
    else:
        webhook_url = slack_params['info']['webhook_url']

    slack_data = {
        "username": "NotificationBot",
        "type": "section",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": footer
                }
            }
        ]
    }

    byte_length = str(sys.getsizeof(slack_data, 2000))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(webhook_url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)