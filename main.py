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
from POE import set_auth, load_chat_id_map, clear_context, send_message, get_latest_message
# from claude import response_to_message
from log import logger


def response_to_message(message: str):
    set_auth('Quora-Formkey', config.POE_FORMKEY)
    set_auth('Cookie', config.POE_COOKIE)
    bots = {1: 'capybara', 2: 'beaver', 3: 'a2_2', 4: 'a2', 5: 'chinchilla', 6: 'nutria'}
    bot = bots[5]
    chat_id = load_chat_id_map(bot)
    if message == "!clear":
        clear_context(chat_id)
        print("Context is now cleared")
        return "Context is now cleared"
    if message == "!break":
        return "Bye"
    send_message(message, bot, chat_id)
    reply = get_latest_message(bot)
    print(f"{bot} : {reply}")
    return reply


class SimplifierBot(Wechaty):
    def __init__(self, options: Optional[WechatyOptions]):
        self.login_user: Optional[Contact] = None
        super().__init__(options)

    async def on_message(self, msg: Message):
        from_contact: Contact = msg.talker()
        text: str = msg.text()
        room: Optional[Room] = msg.room()
        # file_box = None
        # if msg.type() in wechaty.user.message.SUPPORTED_MESSAGE_FILE_TYPES:
        #     file_box: Optional[FileBox] = await msg.to_file_box()
        conversation: Union[Room, Contact] = from_contact if room is None else room
        if text.startswith("。"):
            await conversation.ready()
            await conversation.say(response_to_message(text.replace("。", "", 1)))

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
