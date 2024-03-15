from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import logging
import asyncio
from bot.handlers.basic import say_hellow
import requests
import json


token = '7195842807:AAHJHlXYy9DZQB_3G6mZ842eKYIjcxjYVQA'
async def start_bot(token):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - '  # логирование нужно для отображения результата работы хендлера: is handled / is not handled
                               '%(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    bot = Bot(token=token, parse_mode='HTML')
    dispatcher = Dispatcher()

    dispatcher.message.register(say_hellow, Command(commands=['start', 'help']))

    try:
        await dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())
    finally:
        await bot.session.close()

@dp.message_handler(content_types=['photo', 'document'])
async def photo_or_doc_handler(message: types.Message):
    file_in_io = io.BytesIO()
    if message.content_type == 'photo':
        await message.photo[-1].download(destination_file=file_in_io)
    elif message.content_type == 'document':
        await message.document.download(destination_file=file_in_io)


if __name__ == '__main__':
    asyncio.run(start_bot(token=token))






