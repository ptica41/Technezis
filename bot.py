import asyncio
import os
from os import environ

from aiogram import types, Dispatcher, Bot
from aiogram.filters.command import Command
import pandas as pd

from db import save_to_db
from keyboards import get_kb_download
from parser import parse_prices

UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TOKEN = environ.get('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def welcome(message: types.Message):
    await message.delete()
    await message.answer('Привет! Нажми кнопку "Загрузить файл", чтобы отправить Excel-файл.', reply_markup=get_kb_download())


@dp.message(lambda message: message.text == 'Загрузить файл')
async def request_file(message: types.Message):
    await message.reply('Пожалуйста, прикрепи Excel-файл с данными для парсинга.')


@dp.message(lambda message: message.document is not None)
async def handle_document(message: types.Message):
    doc = message.document
    await message.delete()
    if doc.mime_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        file_id = doc.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = os.path.join(UPLOAD_FOLDER, doc.file_name)
        await bot.download_file(file_path, downloaded_file)

        try:
            df = pd.read_excel(downloaded_file)
            required_columns = ['title', 'url', 'xpath']
            if all(column in df.columns for column in required_columns):
                await message.answer(f'Данные из файла:\n{df.to_string(index=False)}')

                save_to_db(df)
                results = parse_prices(df)

                for site, avg_price in results.items():
                    await message.answer(f'Средняя цена на {site}: {avg_price}')
            else:
                await message.answer('Файл должен содержать колонки: title, url, xpath.')
        except Exception as e:
            await message.answer(f'Ошибка при обработке файла: {e}')
    else:
        await message.answer('Пожалуйста, отправь Excel-файл.')


@dp.message()
async def handle_other_messages(message: types.Message):
    if message.text and message.text not in ['Загрузить файл', '/start']:
        await message.delete()
        await message.answer('Ошибка: Неизвестная команда. Используйте кнопку "Загрузить файл".')
    elif message.content_type != 'document':
        await message.delete()
        await message.answer('Ошибка: Пожалуйста, отправьте Excel-файл.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
