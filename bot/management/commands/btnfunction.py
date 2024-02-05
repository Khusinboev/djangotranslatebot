import os
import django

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.management.commands.function import AuthorizationUser
from bot.models import LangsList, UserLangs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


async def InlineBtnLang(message: types.Message):
    user_id = message.from_user.id
    user_lang = UserLangs.objects.filter(user_id=user_id)
    if len(user_lang) == 0:
        await AuthorizationUser(message)
        user_lang = UserLangs.objects.filter(user_id=user_id)
    langs_data = LangsList.objects.all()
    user_in = user_lang[0].in_lang.lang_in
    user_out = user_lang[0].out_lang.lang_out
    btn_list = []
    for lang_data in langs_data:
        if user_in == lang_data.lang_in:
            inner = InlineKeyboardButton(text=f"✅{lang_data.lang_in}", callback_data=lang_data.lang_in)
        else:
            inner = InlineKeyboardButton(text=lang_data.lang_in, callback_data=lang_data.lang_in)
        if user_out == lang_data.lang_out:
            out = InlineKeyboardButton(text=f"✅{lang_data.lang_out}", callback_data=lang_data.lang_out)
        else:
            out = InlineKeyboardButton(text=lang_data.lang_out, callback_data=lang_data.lang_out)
        btn_list.append([inner, out])

    if user_lang[0].tts is True:
        btn_list.append([InlineKeyboardButton(text="✅TTS", callback_data="TTS")])
    else:
        btn_list.append([InlineKeyboardButton(text="TTS", callback_data="TTS")])

    langs_inline = InlineKeyboardMarkup(row_width=2, inline_keyboard=btn_list)
    langs_inline.inline_keyboard = btn_list
    return langs_inline


async def InsertLang():
    lang1 = ["🇺🇿O'zbek", "🇹🇷Turk", "🇹🇯Tajik", "🇬🇧English", "🇯🇵Japan", "🇮🇹Italian", "🇷🇺Русский", "🇰🇷Korean", "🇸🇦Arabic",
             "🇨🇳Chinese", "🇫🇷French", "🇩🇪German", "🇮🇳Hindi", "🇦🇿Azerbaijan", "🇦🇫Afghan", "🇰🇿Kazakh",
             "🇹🇲Turkmen", "🇰🇬Kyrgyz"]

    lang2 = ["🇺🇿 O'zbek", "🇹🇷 Turk", "🇹🇯 Tajik", "🇬🇧 English", "🇯🇵 Japan", "🇮🇹 Italian", "🇷🇺 Русский", "🇰🇷 Korean",
             "🇸🇦 Arabic", "🇨🇳 Chinese", "🇫🇷 French", "🇩🇪 German", "🇮🇳 Hindi", "🇦🇿 Azerbaijan", "🇦🇫 Afghan", "🇰🇿 Kazakh", "🇹🇲 Turkmen", "🇰🇬 Kyrgyz"]

    codes = ["uz", "tr", "tg", "en", "ja", "it", "ru", "korean", "ar", "zh-CN", "fr", "de", "hi", "az", "af", "kk",
             "tk", "ky"]
    for lang_in, lang_out, code in zip(lang1, lang2, codes):
        LangsList.objects.get_or_create(lang_in=lang_in, lang_out=lang_out, code=code, status=True)
