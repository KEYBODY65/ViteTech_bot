from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import logging
import asyncio
from bot.handlers.basic import say_hellow
from bot.handlers.create_test import *
from bot.settings import get_key


token = get_key('/home/misha/PycharmProjects/ViteTech_bot/KEY').key

async def start_bot(token):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - '  # логирование нужно для отображения результата работы хендлера: is handled / is not handled
                               '%(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    bot = Bot(token=token, parse_mode='HTML')
    dispatcher = Dispatcher()

    dispatcher.message.register(say_hellow, Command(commands=['start', 'help']))
    dispatcher.message.register(create_form, Command(commands=['create_test', 'create_form']))
    dispatcher.message.register(test, Create_Test.GET_TEXT)
    dispatcher.message.register(num_q, Create_Test.NUM_Q)


    try:
        await dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())
    finally:
        await bot.session.close()





if __name__ == '__main__':
    asyncio.run(start_bot(token=token))