import logging
from aiogram import Bot, Dispatcher, executor, types
from parcer import get_table
from datetime import date

API_TOKEN = '5320035863:AAEOAA9u84vLGponnf41n9b2zJ49dBlqk7s'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def bot_answer():
    shops = ''
    count = 1
    table = get_table(count)
    while table[0] != date.today():
        count += 1
        table = get_table(count)
    values = table[1:].sort()
    return f'И так, в то время, как курс центробанка составляет {values[0]}'


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Приветствую. Моя единственная функция - выводить курс доллара на китайских торговых \
    площадках. Для ее выполнения, введите слово "Курс" без кавычек')


@dp.message_handler()
async def show(message: types.Message):
    if message.text.lower() == 'курс':
        await message.answer(get_table(1))
    else:
        await message.answer('Это не очень похоже на "Курс". Так я делать ничего не буду')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
