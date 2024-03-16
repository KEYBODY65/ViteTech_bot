from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils.state import Create_Test
from bot.utils.func_for_test import api_to_ygpt


async def create_form(message: Message, state: FSMContext):
    await message.answer('Перейдём к созданию теста')
    await message.answer('пожалуйста, напишите текст из которого я сделаю тест')
    await state.set_state(Create_Test.GET_TEXT.state)
    await state.set_state(Create_Test.GET_TEXT.state)


async def test(message: Message, state: FSMContext):
    await state.update_data(msg=message.text)
    await message.answer('Введите кол-во вопросов')
    await state.set_state(Create_Test.NUM_Q.state)


async def num_q(message: Message, state: FSMContext):
    await state.update_data(num=message.text)
    data = await state.get_data()
    num_q = data['num']
    prompt = '"""' + data['msg'] + '"""'
    print(prompt, num_q)
    await message.answer(api_to_ygpt(system_prompt=f'Создайте тест из текста в кавчках, состоящий'
                                                   f' из {num_q} вопросв по тексту. Действуй как школьный учитель. Тест выглядеть примерно так: "Номер вопроса" "Вопрос"'
                                                   "Номер варианта ответа"
                                                   "Вариант ответа"
                                                   f' перед каждым из вариантов ответов ставь цифру от 1 до 4. Вопросы пронумеровать" В конце напиши вартанты ответов на каждый вопрос',
                                     prompt=prompt))
    await state.clear()
