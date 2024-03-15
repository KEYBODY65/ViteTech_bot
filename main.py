from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import logging
import asyncio
from bot.handlers.basic import say_hellow
import requests
import json
import time

# Данные для подключения к YaGPT
yandex_cloud_catalog = "b1gmasb9gep76ibr32ga"
yandex_gpt_api_key = "AQVN2kypilSivP_FGODoaobvzAmweoeI4l0LKsks"
yandex_gpt_model = "yandexgpt-lite"

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

# @dp.message_handler(content_types=['photo', 'document'])
# async def photo_or_doc_handler(message: types.Message):
#     file_in_io = io.BytesIO()
#     if message.content_type == 'photo':
#         await message.photo[-1].download(destination_file=file_in_io)
#     elif message.content_type == 'document':
#         await message.document.download(destination_file=file_in_io)


async def обработка полученного сообщения():

    # Для запроса
    system_prompt = """Рассуждай как учитель, которому нужно дать ученикам самостоятельную работу. Ее цель -- проверить, насколько они усвоили материал. На основе текста подбери вопросы, по ответам на которые будет понятно, поняли ли ученики тему. В ответе выведи список вопросов и 4 различных ответов на каждый на новой строке, правильным из которых явлеяется только один. Вывод должен быть в формате теста с латинской буквой -- одной из списка: A, B, C, D -- обозначением к каждому вопросу. В конце отдельно укажи правильный вариант ответа на каждый вопрос(для проверки учителем)."""
    # Сюда материал для составления теста
    material = ЗДЕСЬ ТЕКСТ ПОЛУЧЕННЫЙ ИЗ ФАЙЛА ИЛИ СООБЩЕНИЯ message.text
    answer = send_gpt_request(system_prompt, material)
    await ОТПРАВИТЬ СООБЩЕНИЕ bot.send_message(chat_id=ОТВЕТИТЬ ТОЛЬКО ПОЛЬЗОВАТЕЛЮ, КТО ОТПРАВИЛ СООБЩЕНИЕ effective_chat.id, text=answer)


def send_gpt_request(system_prompt: str, user_prompt: str):
    body = {
        "modelUri": f"gpt://{yandex_cloud_catalog}/{yandex_gpt_model}",
        "completionOptions": {"stream": False, "temperature": 0.8, "maxTokens": "2000"},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": user_prompt},
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_gpt_api_key}",
        "x-folder-id": yandex_cloud_catalog,
    }

    response = requests.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)
    operation_id = response_json["id"]

    url = f"https://llm.api.cloud.yandex.net/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {yandex_gpt_api_key}"}

    done = False
    while not done:
        response = requests.get(url, headers=headers)
        response_json = json.loads(response.text)
        done = response_json["done"]
        time.sleep(0.5)

    answer = response_json["response"]["alternatives"][0]["message"]["text"]
    return(answer)


if __name__ == '__main__':
    asyncio.run(start_bot(token=token))