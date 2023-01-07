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


def central_bank():
    day = 1
    table = get_table(day)
    cb_rate = table["ЦБ РФ"]
    add = '.'
    if cb_rate == '':
        while cb_rate == '':
            day += 1
            table = get_table(day)
            cb_rate = table["ЦБ РФ"]
        cb_date = table["Дата"]
        add = f'(последнее обновление за {cb_date}, скорее всего из-за выходных, ведь биржа простаивает)'

    answer = f'Курс центробанка составляет {cb_rate}₽ ' + add
    return answer


def get_shops():
    day = 1
    add = ''
    shops = get_table(day)
    if shops["Дата"] != str(date.today()):
        table = get_table(day + 1)
        add = '(за сегодня данных еще нет)'
        # shops.pop("Дата")
    shops = dict(sorted(shops.items(), key=lambda x: x[1]))
    shops.pop("ЦБ РФ")
    answer = f'И так, на {shops.pop("Дата")} {add}, самый выгодный магазин - <b>{list(shops.keys())[0]}</b> с курсом ' \
             f'<b>{list(shops.values())[0]}</b> ₽. \nНа <b>Aliexpress</b> курс составляет <b> {shops["Aliexpress.ru"]}' \
             f'</b> ₽.\n\n{central_bank()}\n\nВесь список в порядке возрастания курса выглядит следующим образом:\n'
    for k, v in shops.items():
        answer += f"{k}:  {v} ₽\n"
    return answer


def bot_answer():
    return get_shops()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(bot_answer(), parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def show(message: types.Message):
    if message.text.lower() == 'курс':
        await message.answer(get_table(1))
    else:
        await message.answer('Это не очень похоже на "Курс". Так я делать ничего не буду')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
