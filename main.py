import asyncio
from typing import Optional, Union

import wechaty
from wechaty import (
    FileBox,
    Wechaty,
    Contact,
    Room,
    Message, WechatyOptions
)

import config
from claude import response_to_message
from log import logger


class SimplifierBot(Wechaty):
    def __init__(self, options: Optional[WechatyOptions]):
        self.login_user: Optional[Contact] = None
        super().__init__(options)

    async def on_message(self, msg: Message):
        from_contact: Contact = msg.talker()
        text: str = msg.text()
        room: Optional[Room] = msg.room()
        file_box = None
        if msg.type() in wechaty.user.message.SUPPORTED_MESSAGE_FILE_TYPES:
            file_box: Optional[FileBox] = await msg.to_file_box()
        conversation: Union[Room, Contact] = from_contact if room is None else room
        if text.startswith("。"):
            await conversation.ready()
            await conversation.say(response_to_message(text.replace("。 ", "", 1)))

    async def on_login(self, contact: Contact):
        logger.info('Contact<%s> has logined ...', contact)
        self.login_user = contact


bot: Optional[SimplifierBot] = None


async def main():
    from dotenv import load_dotenv
    load_dotenv()
    global bot
    bot = SimplifierBot(WechatyOptions(token=config.WECHATY_TOKEN))
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
