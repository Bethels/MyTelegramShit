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
    shops = get_table(1)
    if shops.pop("Дата") != str(date.today()):
        table = get_table(2)
        shops.pop("Дата")
    shops = dict(sorted(shops.items(), key=lambda x: x[1]))
    print(shops)
    answer = f'И так, в то время, как курс ЦБ РФ составляет {shops.pop("ЦБ РФ")} ₽ за $, ближе всех к нему подобрался \
<b>{list(shops.keys())[0]}</b> с курсом <b>{list(shops.values())[0]}</b> ₽. \nНа <b>Aliexpress</b> курс составляет \
<b>{shops["AliExpress"]}</b> ₽.\n\nВесь список в порядке возрастания курса выглядит следующим образом: \n'
    for k, v in shops.items():
        answer += f"{k}:  {v} ₽\n"

    return answer


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # await message.reply('Приветствую. Моя единственная функция - выводить курс доллара на китайских торговых \
    #     площадках. Для ее выполнения, введите слово "Курс" без кавычек')
    await message.answer(bot_answer(), parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def show(message: types.Message):
    if message.text.lower() == 'курс':
        await message.answer(get_table(1))
    else:
        await message.answer('Это не очень похоже на "Курс". Так я делать ничего не буду')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
