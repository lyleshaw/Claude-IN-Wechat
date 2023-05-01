import os

import requests
from revChatGPT.V3 import Chatbot

import config
from log import logger

chatbot = Chatbot(api_key=config.OPENAI_API_KEY)


def response_to_message(message: str, conv_id: str) -> str:
    os.environ['API_URL'] = "https://api.openai-sb.com/v1/chat/completions"
    logger.info(f"Conv ID: {conv_id}, Message: {message}")
    return chatbot.ask("Hello world")


def reset_conv(conv_id: str) -> None:
    chatbot.reset(conv_id)


def get_usage() -> [str, str]:
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={config.OPENAI_API_KEY}')
    return response.json()['data']['credit'], response.json()['data']['use_tokens']
