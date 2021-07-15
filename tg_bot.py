import json
import time

from confing import token, user_id
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode


bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Все скидки', 'Категории']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer('Скидки магнит', reply_markup=keyboard)


@dp.message_handler(text='Категории')
async def category(message: types.Message):
    category_button = ['Фрукты и овощи', 'Кондитерские изделия',
                       'Красота и здоровье', 'Напитки',
                       'Молочные продукты', 'Бакалея',
                       'Хлеб и выпечка', 'Мясо, рыба, яйца',
                       'Полуфабрикаты', 'Снеки',
                       'Готовые блюда', 'Бытовая химия',
                       'Детям', 'Дом, сад, гараж',
                       'Аптечные товары', 'Алкогольная продукция',
                       'Назад']

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*category_button)

    await message.answer('Скидки по категориям', reply_markup=keyboard)


@dp.message_handler(text='Назад')
async def back(message: types.Message):
    start_button = ['Все скидки', 'Категории']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer('Скидки магнит', reply_markup=keyboard)


@dp.message_handler()
async def bot_message(message: types.Message):
    value = message.text
    if value == 'Фрукты и овощи':
        value = 'fruits_vegetables'
    if value == 'Кондитерские изделия':
        value = 'konditerskye'
    if value == 'Красота и здоровье':
        value = 'krasota'
    if value == 'Напитки':
        value = 'napitki'
    if value == 'Молочные продукты':
        value = 'molochnie_produkty'
    if value == 'Бакалея':
        value = 'bakaleya'
    if value == 'Хлеб и выпечка':
        value = 'hleb'
    if value == 'Мясо, рыба, яйца':
        value = 'myaso_ryba'
    if value == 'Полуфабрикаты':
        value = 'polufabkitaty'
    if value == 'Снеки':
        value = 'sneki'
    if value == 'Готовые блюда':
        value = 'gotovye'
    if value == 'Бытовая химия':
        value = 'byt_chim'
    if value == 'Детям':
        value = 'detyam'
    if value == 'Дом, сад, гараж':
        value = 'dom_sad'
    if value == 'Аптечные товары':
        value = 'apteka'
    if value == 'Алкогольная продукция':
        value = 'alk'
    try:
        with open(f'data/{value}_products_data_list.json', encoding='utf-8') as file:
            value = json.load(file)
            num = 0
            for x in range(0, len(value)):
                action = f"Название товара: {value[num]['Название товара']}\n" \
                         f"Старая цена товара: {value[num]['Старая цена товара']} Руб\n" \
                         f"🔥️Новая Цена товара: {value[num]['Новая цена товара']} Руб🔥️\n" \
                         f"❗️Процент скидки: {value[num]['Процент скидки'] + ' %❗️'}\n" \
                         f"Длительность акции:" \
                         f" {value[num]['Длительность акции']['Начало акции']}" \
                         f" {value[num]['Длительность акции']['Конец акции']}"
                await message.answer(action)
                num += 1
    except FileNotFoundError:
        message_error = 'Нет скидок на данную категорию'
        await bot.send_message(message.from_user.id, message_error)


@dp.message_handler(text='Все скидки')
async def all_action(message: types.Message):
    for item in ['fruits_vegetables', 'konditerskye',
                 'krasota', 'napitki', 'molochnie_produkty',
                 'bakaleya', 'hleb', 'myaso_ryba',
                 'myaso_ryba', 'fruits_vegetables', 'sneki',
                 'gotovye', 'byt_chim', 'detyam',
                 'dom_sad', 'apteka', 'alk']:
        str(item)
        with open(f'data/{item}_products_data_list.json', encoding='utf-8') as file:
            item = json.load(file)
        num = 0
        for x in range(0, len(item)):
            action = f"Название товара: {value[num]['Название товара']}\n" \
                     f"Старая цена товара: {value[num]['Старая цена товара']} Руб\n" \
                     f"🔥️Новая Цена товара: {value[num]['Новая цена товара']} Руб🔥️\n" \
                     f"❗️Процент скидки: {value[num]['Процент скидки'] + ' %❗️'}\n" \
                     f"Длительность акции:" \
                     f" {value[num]['Длительность акции']['Начало акции']}" \
                     f" {value[num]['Длительность акции']['Конец акции']}"
            await message.answer(action)
            num += 1
        time.sleep(10)

if __name__ == '__main__':
    executor.start_polling(dp)