import datetime

import settings
import err
import query
import re

node_stats = []
recorded_errors_timestamp = ""
recorded_errors = ""


def healthy(node_height: int) -> bool:
    global node_stats
    node_stats.append(node_height)
    if len(node_stats) == settings.SELF_CHECK_INTERVAL:
        try:
            average = abs((sum(node_stats) / len(node_stats)) - node_height)
            if average <= settings.MIN_AVERAGE:
                return False
        finally:
            node_stats = []
    return True


def check_sync() -> list:
    errors = []
    global recorded_errors
    global recorded_errors_timestamp

    # NODE
    address = settings.NODE_API + settings.END_POINT_FOR_LAST_BLOCK
    try:
        node_ip = re.search(r"\b([\d]{1,3}\.){3}[\d]{1,3}\b", address).group()
        instance = f'<{settings.GCLOUD_SEARCH + node_ip}|GCLOUD>'
    except AttributeError:
        instance = settings.NODE_API

    node_height, error = query.height(address)
    if not node_height:
        errors.append(f"{err.getting_height} node deployed @ {instance} @ {datetime.datetime.now()} {error}")
        return errors
    if not healthy(node_height):
        errors.append(f"Node deployed @ {instance} might be stuck on block {node_height} "
                      f"@ {datetime.datetime.now()}")
        return errors

    # Checking height of the two explorers
    for i in range(1, 2):
        explorer_name = f"V{i} Explorer"
        address = settings.EXPLORER_V1_HOST if i == 1 \
            else settings.EXPLORER_V2_HOST
        explorer_height, error = query.height(address + settings.HEALTHCHECK_ENDPOINT)
        if not explorer_height:
            errors.append(f"{err.getting_height} {explorer_name} @ {datetime.datetime.now()} with error {error}")
        elif abs(explorer_height - node_height) >= settings.MAX_SYNC_TOLERANCE:
            errors.append(f"{explorer_name} {err.stuck_behind} {abs(explorer_height - node_height)} blocks "
                          f"@ {datetime.datetime.now()}")

    return errors


def msg_type(msg: str) -> dict:
    status_starting_message = {
        "username": "Sync info",
        "icon_emoji": ":large_green_circle:",
        "attachments": [
            {
                "color": "#32D132",
                "fields": [
                    {
                        "value": f"Monitoring started!\n"
                                 f" - Alive Status:\n"
                                 f"     every {int(settings.SELF_CHECK_INTERVAL) * int(settings.SCHEDULE_TIME)} minutes\n"
                                 f" - Allowed Block Delay:\n"
                                 f"     {settings.MAX_SYNC_TOLERANCE} blocks per {settings.SCHEDULE_TIME} minutes\n"
                                 f" - Node Health Check:\n"
                                 f"     minimum"
                                 f" {int(settings.MIN_AVERAGE) * int(settings.SELF_CHECK_INTERVAL)} blocks per"
                                 f" {int(settings.SELF_CHECK_INTERVAL) * int(settings.SCHEDULE_TIME)} minutes",
                        "short": "false",
                    }
                ]
            }
        ]
    }
    status_ok_message = {
        "username": "Sync info",
        "icon_emoji": ":large_green_circle:",
        "attachments": [
            {
                "color": "#32D132",
                "fields": [
                    {
                        "value": "All synced",
                        "short": "false",
                    }
                ]
            }
        ]
    }
    status_resume_message = {
        "username": "Sync info",
        "icon_emoji": ":large_green_circle:",
        "attachments": [
            {
                "color": "#32D132",
                "fields": [
                    {
                        "value": "Back ONLINE",
                        "short": "false",
                    }
                ]
            }
        ]
    }
    status_silent_message = {
        "username": "Sync info",
        "icon_emoji": ":large_orange_circle:",
        "attachments": [
            {
                "color": "#D1C432",
                "fields": [
                    {
                        "value": "Entering silent mode",
                        "short": "false",
                    }
                ]
            }
        ]
    }
    status_remind_message = {
        "username": "Sync reminder",
        "icon_emoji": ":exclamation:",
        "attachments": [
            {
                "fields": [
                    {
                        "value": "Unresolved error",
                        "short": "true",
                    }
                ]
            }
        ]
    }
    status_timestamp_remind_message = {
        "username": "Sync reminder",
        "icon_emoji": ":exclamation:",
        "attachments": [
            {
                "fields": [
                    {
                        "value": f"Unresolved error from {recorded_errors_timestamp}",
                        "short": "false",
                    }
                ]
            }
        ]
    }
    status_error_remind_message = {
        "username": "Sync reminder",
        "icon_emoji": ":rotating_light:",
        "attachments": [
            {
                "fields": [
                    {
                        "value": f"Unresolved error:\n{recorded_errors}",
                        "short": "false",
                    }
                ]
            }
        ]
    }
    if msg == "Status - OK":
        return status_ok_message
    elif msg == "Status - RESUME":
        return status_resume_message
    elif msg == "Status - SILENT":
        return status_silent_message
    elif msg == "Status - REMIND":
        return status_remind_message
    elif msg == "Start monitoring":
        return status_starting_message
    elif msg == "Status - REMIND with TIMESTAMP" and recorded_errors_timestamp:
        return status_timestamp_remind_message
    elif msg == "Status - REMIND with ERROR" and recorded_errors:
        return status_error_remind_message
    return {
        "username": "Sync alert",
        "icon_emoji": ":red_circle:",
        "attachments": [
            {
                "color": "#FF0000",
                "fields": [
                    {
                        "value": msg,
                        "short": "false",
                    }
                ]
            }
        ]
    }
