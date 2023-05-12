import os

import requests
from revChatGPT.V3 import Chatbot

import config
from log import logger

chatbot = Chatbot(api_key=config.OPENAI_API_KEY, system_prompt="你是一个善于帮助人的朋友。总会简短而精确的回答人们的问题。")


def response_to_message(message: str, conv_id: str) -> str:
    if conv_id in chatbot.conversation:
        while len(chatbot.conversation[conv_id]) > 10:
            chatbot.conversation[conv_id].pop(0)
    os.environ['API_URL'] = "https://api.openai-sb.com/v1/chat/completions"
    logger.info(f"Conv ID: {conv_id}, Message: {message}")
    try:
        resp = chatbot.ask(prompt=message, conv_id=conv_id)
    except Exception as e:
        logger.error(e)
        resp = "出错了，请重试"
    logger.info(f"Response: {resp}")
    return resp


def response_with_google(query: str) -> str:
    logger.info(f"Google Req: {query}")
    try:
        resp = requests.get(f'http://search.aireview.tech/api/search', params={"query": query}).text
    except Exception as e:
        logger.error(e)
        return "联网查询出错了，请重试"
    logger.info(f"Google Response: {resp}")
    if "Text" not in resp:
        return "联网查询出错了，请重试"
    prompt = f"{resp}\n请根据如上的Google搜索结果回答问题:{query}"
    os.environ['API_URL'] = "https://api.openai-sb.com/v1/chat/completions"
    logger.info(f"Message: {prompt}")
    try:
        resp = chatbot.ask(prompt=prompt)
    except Exception as e:
        logger.error(e)
        resp = "联网查询出错了，请重试"
    logger.info(f"Google Response: {resp}")
    return resp


def response_with_bard(prompt: str) -> str:
    try:
        resp = requests.get(f'http://bard.aireview.tech/api/query', params={"prompt": prompt}).text
    except Exception as e:
        logger.error(e)
        return "bard 调用出错了，请重试"
    logger.info(f"Bard Response: {resp}")
    return resp


def reset_conv(conv_id: str, system_prompt: str) -> None:
    chatbot.reset(conv_id, system_prompt=system_prompt)


def get_usage() -> [str, str]:
    response = requests.get(f'https://api.openai-sb.com/sb-api/user/status?api_key={config.OPENAI_API_KEY}')
    return response.json()['data']['credit'], response.json()['data']['use_tokens']
