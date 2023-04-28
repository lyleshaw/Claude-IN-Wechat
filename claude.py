import time

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import config
from log import logger

SLACK_USER_TOKEN = config.SLACK_USER_TOKEN
client = WebClient(token=SLACK_USER_TOKEN)
BOT_USER_ID = config.BOT_USER_ID

global last_message_timestamp


def send_message(channel, text):
    try:
        return client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        logger.error(f"Error sending message: {e}")


def fetch_messages(channel, last_message_timestamp):
    response = client.conversations_history(channel=channel, oldest=last_message_timestamp)
    return [msg['text'] for msg in response['messages'] if msg['user'] == BOT_USER_ID]


def get_new_messages(channel, last_message_timestamp):
    time.sleep(4)
    while True:
        messages = fetch_messages(channel, last_message_timestamp)
        if messages and not messages[-1].endswith('Typing…_'):
            return messages[-1]


def find_direct_message_channel(user_id):
    try:
        response = client.conversations_open(users=user_id)
        return response['channel']['id']
    except SlackApiError as e:
        logger.error(f"Error opening DM channel: {e}")


dm_channel_id = find_direct_message_channel(BOT_USER_ID)


def response_to_message(message: str):
    global last_message_timestamp
    response = send_message(dm_channel_id, message)
    if response:
        last_message_timestamp = response['ts']
    return get_new_messages(dm_channel_id, last_message_timestamp)
