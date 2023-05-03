import os

import requests
from revChatGPT.V3 import Chatbot

import config
from log import logger

chatbot = Chatbot(api_key=config.OPENAI_API_KEY, system_prompt="你是一个善于帮助人的朋友。总会简短而精确的回答人们的问题。")


def response_to_message(message: str, conv_id: str) -> str:
    while len(chatbot.conversation[conv_id]) > 10:
        chatbot.conversation[conv_id].pop(0)
    os.environ['API_URL'] = "https://api.openai-sb.com/v1/chat/completions"
    logger.info(f"Conv ID: {conv_id}, Message: {message}")
    resp = chatbot.ask(prompt=message, conv_id=conv_id)
    logger.info(f"Response: {resp}")
    return resp


def reset_conv(conv_id: str, system_prompt: str) -> None:
    chatbot.reset(conv_id, system_prompt=system_prompt)


def get_usage() -> [str, str]:
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={config.OPENAI_API_KEY}')
    return response.json()['data']['credit'], response.json()['data']['use_tokens']
