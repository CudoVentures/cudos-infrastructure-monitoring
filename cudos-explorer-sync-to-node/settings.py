import os

from dotenv import load_dotenv

import emit

load_dotenv()

# SETTINGS

# Global
SCHEDULE_TIME = 50
MAX_SYNC_TOLERANCE = 20
MIN_AVERAGE = 5
SELF_CHECK_INTERVAL = 3
REMINDER = 5
SILENT_MODE = False  # Do not change manually

# GCLOUD
GCLOUD_SEARCH = "https://console.cloud.google.com/search;q="

# Node
NODE_API = os.getenv("NODE_API")
END_POINT_FOR_LAST_BLOCK = os.getenv("END_POINT_FOR_LAST_BLOCK")

# Slack
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Explorer V1, V2
EXPLORER_V1_HOST = os.getenv("EXPLORER_V1_HOST")
EXPLORER_V2_HOST = os.getenv("EXPLORER_V2_HOST")
HEALTHCHECK_ENDPOINT = os.getenv("HEALTHCHECK_ENDPOINT")


def silent_mode(mode: str = "") -> bool:
    global SILENT_MODE
    if mode == "ON":
        SILENT_MODE = True
        emit.slack(["Status - SILENT"])
    elif mode == "OFF":
        SILENT_MODE = False
        emit.slack(["Status - RESUME"])
    return SILENT_MODE
