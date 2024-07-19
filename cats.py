import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests


from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0]["url"]
    else:
        return None

def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed["name"].lower() == breed_name.lower():
            return breed
    return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я помогу тебе выбрать кота. Введи название породы или команду /cancel для отмены.")

@dp.message(Command(commands=["cancel"]))
async def cancel(message: Message):
    await message.answer("Отменено.")

@dp.message()
async def get_cat(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info is None:
        await message.answer("Такой породы нет. Попробуйте еще.")
    else:
        image_url = get_cat_image_by_breed(breed_info["id"])
        info = (f"Порода - {breed_info['name']}\n"
                f"Вид - {breed_info['temperament']}\n"
                f"Описание - {breed_info['description']}\n"
                f"Продолжительность жизни: {breed_info['life_span']}лет\n")
        await message.answer_photo(photo=image_url, caption=info)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())