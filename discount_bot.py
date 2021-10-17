from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import json
import os


# bot = Bot(token="")
bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Кроссовки", "Видеокарты", "Гречка"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer("Товары со скидкой", reply_markup=keyboard)
    
    
@dp.message_handler(Text(equals="Кроссовки"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please waiting...")
    
    collect_data()
    
    with open("result_data.json") as file:
        data = json.load(file)

    for item in data:
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
            f"{hbold('Категория: ')} {item.get('category')}\n" \
            f"{hbold('Прайс: ')} {item.get('price_base')}\n" \
            f"{hbold('Прайс со скидкой: ')} -{item.get('discount_percent')}%: {item.get('price_sale')}🔥"
            
        await message.answer(card)
        

def main():
    executor.start_polling(dp)
    
    
if __name__ == "__main__":
    main()
