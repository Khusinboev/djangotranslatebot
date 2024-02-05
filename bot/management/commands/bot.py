import asyncio
import logging
import os
import sys

import django
import multitasking
from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import CallbackQuery
from deep_translator import GoogleTranslator

from bot.management.commands.additionaltext import words
from bot.management.commands.btnfunction import InlineBtnLang, InsertLang
from bot.management.commands.function import AuthorizationUser
from bot.models import LangsList, UserLangs
from config.settings import API_TOKEN


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


dp = Dispatcher()
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)


@multitasking.task
def set_polling():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))


@dp.message(CommandStart())
async def start(message: types.Message):
    await InsertLang()
    await AuthorizationUser(message)
    lang_code = message.from_user.language_code
    send_text = words['welcome_msg']
    if lang_code is None:
        await message.answer(send_text)
    else:
        translator = GoogleTranslator(source='uz', target=lang_code)
        trtext = translator.translate(send_text)
        await message.answer(trtext)


@dp.message(Command("lang"))
@dp.message(Command("help"))
async def command_lang(message: types.Message):
    lang_code = message.from_user.language_code
    if message.text == '/lang':
        text = words['command_lang']
        translator = GoogleTranslator(source='uz', target=lang_code)
        send_text = translator.translate(text)
        await message.answer(send_text, reply_markup=await InlineBtnLang(message))
    else:
        await message.answer(words['command_help'])


class LangFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, call: CallbackQuery) -> bool:
        result_l = []
        ll = LangsList.objects.all()
        for i in ll:
            result_l.append(i.lang_in)
            result_l.append(i.lang_out)
            result_l.append(i.code)
        result_l.append('TTS')
        return call.data in result_l


@dp.callback_query(LangFilter("hello"))
async def choose_lang(call: CallbackQuery):
    await call.answer()
    call_data = call.data
    user_id = call.from_user.id
    get_user = UserLangs.objects.get_or_create(user_id=user_id)

    ll = LangsList.objects.all()
    lang_in, lang_out = [], []
    for i in ll:
        lang_in.append(i.lang_in)
        lang_out.append(i.lang_out)
    if call_data in lang_in:
        update_in = LangsList.objects.get_or_create(lang_in=call_data)[0]
        update = UserLangs.objects.filter(user_id=get_user[0].user_id)[0]
        update.in_lang = update_in
        update.save()
    elif call_data in lang_out:
        update_out = LangsList.objects.get_or_create(lang_in=call_data)[0]
        update = UserLangs.objects.get(user_id=user_id)
        update.out_lang = update_out
        update.save()

    await call.message.edit_text(text="Languages list")
    await call.message.edit_reply_markup(reply_markup=await InlineBtnLang(call.message))
