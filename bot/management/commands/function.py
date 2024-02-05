import os
import django

from aiogram import types

from bot.models import Accounts, UserLangs, LangsList


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


async def AuthorizationUser(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    lang_code = message.from_user.language_code
    get_user = Accounts.objects.filter(user_id=user_id)
    if len(get_user) == 0:
        if username:
            if lang_code:
                insert = Accounts(user_id=user_id, username=username, lang_code=lang_code)
                insert.save()
            else:
                insert = Accounts(user_id=user_id, username=username)
                insert.save()
        else:
            insert = Accounts(user_id=user_id)
            insert.save()

        for_you = Accounts.objects.get_or_create(user_id=user_id)[0]
        in_lang = LangsList.objects.get_or_create(code='uz')[0]
        out_lang = LangsList.objects.get_or_create(code='en')[0]
        insert_tts = UserLangs(user_id=for_you, in_lang=in_lang, out_lang=out_lang)
        insert_tts.save()
