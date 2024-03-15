from aiogram.types import Message
from aiogram import Bot

async def say_hellow(message: Message, bot: Bot):
    await bot.send_message(text='Привет!\n'
                                'чтобы создать тест - /create_test', chat_id=message.chat.id)