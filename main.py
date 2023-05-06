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
                response_to_message(text.replace("。", "", 1), from_id) + "\n感谢「礼」「栗栗栗栗子」的赞助~")
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
            await conversation.say(f"当前时间：{strftime}\n毫秒 {microsecond} 对总数 {total} 取余得 {final}\n因此抽取：{final+1}")

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
