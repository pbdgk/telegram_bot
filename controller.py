import asyncio
import json

from telepot.aio.loop import MessageLoop
from telepot.aio import Bot

from db import PostgresDb
from message_handler import ChatHandler, CallbackHandler


def _get_token(file='config.txt', mode='r'):
    with open(file, mode) as f:
        return json.load(f)

async def on_chat_message(message):
    await ChatHandler(bot, postgres_db, message).handle()


async def on_callback_query(message):
    await CallbackHandler(bot, postgres_db, message).handle()


if __name__ == '__main__':
    TOKEN = _get_token()
    bot = Bot(TOKEN)
    postgres_db = PostgresDb()
    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot, {
                                        'chat': on_chat_message,
                                        'callback_query': on_callback_query
                                       }).run_forever())
    try:
        print('listening...')
        loop.run_forever()
    finally:
        loop.close()
