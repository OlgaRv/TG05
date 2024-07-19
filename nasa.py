import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
import datetime
from datetime import timedelta

from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_apod():
    end_date = datetime.datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
    apod = get_random_apod()
    if apod is None:
        await message.answer("Произошла ошибка при получении данных.")
    else:
        photo_url = apod["url"]
        title = apod["title"]
        explanation = apod["explanation"]
        await message.answer_photo(photo=photo_url, caption=f"{title}\n")
        await message.answer(text=f"{explanation}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())