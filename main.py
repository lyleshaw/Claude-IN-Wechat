import asyncio
import random
import time
from datetime import datetime
from typing import Optional, Union

from wechaty import (
    Wechaty,
    Contact,
    Room,
    Message, WechatyOptions
)

import config
import openai
from log import logger
from openai import response_to_message, reset_conv, get_usage


class SimplifierBot(Wechaty):
    def __init__(self, options: Optional[WechatyOptions]):
        self.login_user: Optional[Contact] = None
        super().__init__(options)

    async def on_message(self, msg: Message):
        from_contact: Contact = msg.talker()
        text: str = msg.text()
        room: Optional[Room] = msg.room()
        conversation: Union[Room, Contact] = from_contact if room is None else room
        from_id: str = from_contact.contact_id if room is None else room.room_id
        if text.startswith("。") and (not text.startswith("。。")) and len(text) > 1:
            await conversation.ready()
            await conversation.say(
                response_to_message(text.replace("。", "", 1), from_id) + "\n感谢「礼」「栗栗栗栗子」「孙晟禹今天写曲子了吗」的赞助~")
        if text.startswith("/reset"):
            system_prompt = text.replace("/reset ", "", 1)
            reset_conv(from_id, system_prompt)
            await conversation.ready()
            await conversation.say("已重置")
        if text == "/query":
            credit, use_tokens = get_usage()
            await conversation.ready()
            await conversation.say(f"当前会话：{from_id}\n剩余额度：{credit}\n已用次数：{use_tokens}")
        if text.startswith("/set"):
            token = text.replace("/set ", "", 1)
            config.OPENAI_API_KEY = token
            openai.chatbot.api_key = token
            credit, use_tokens = get_usage()
            await conversation.ready()
            await conversation.say(f"已使用新 token\n当前会话：{from_id}\n剩余额度：{credit}\n已用次数：{use_tokens}")
        if text.startswith("/r"):
            total = int(text.replace("/r ", "", 1))
            now = datetime.now()
            microsecond = now.microsecond
            strftime = now.strftime("%H:%M:%S.%f")
            final = microsecond % total
            await conversation.say(f"指令时间：{strftime}\n"
                                   f"抽取编号：{final+1}")
        if text.startswith("/s"):
            query = text.replace("/s ", "", 1)
            await conversation.ready()
            await conversation.say(f"{openai.response_with_google(query)}\n感谢「礼」「栗栗栗栗子」「孙晟禹今天写曲子了吗」的赞助~")
        if text.startswith("/b"):
            query = text.replace("/b ", "", 1)
            await conversation.ready()
            await conversation.say(f"{openai.response_with_bard(query)}\n感谢「礼」「栗栗栗栗子」「孙晟禹今天写曲子了吗」的赞助~")

    async def on_login(self, contact: Contact):
        logger.info('Contact<%s> has logined ...', contact)
        self.login_user = contact


bot: Optional[SimplifierBot] = None


async def main():
    global bot
    bot = SimplifierBot(WechatyOptions(token=config.WECHATY_TOKEN))
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
