import asyncio
from typing import Optional, Union

from wechaty import (
    Wechaty,
    Contact,
    Room,
    Message, WechatyOptions
)

import config
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
        if text.startswith("。"):
            await conversation.ready()
            await conversation.say(response_to_message(text.replace("。", "", 1), from_id))
        if text == "/reset":
            reset_conv(from_id)
            await conversation.ready()
            await conversation.say("已重置")
        if text == "/query":
            credit, use_tokens = get_usage()
            await conversation.ready()
            await conversation.say(f"当前会话：{self.login_user}\n剩余额度：{credit}\n已用次数：{use_tokens}")

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
