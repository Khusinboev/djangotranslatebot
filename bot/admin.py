from django.contrib import admin

from bot.models import UserLangs, UserStatus, LangsList, Accounts


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'lang_code')
    list_filter = ('user_id', 'username', 'lang_code')


class UserLangsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'in_lang', 'out_lang', 'tts')
    list_filter = ('user_id', 'in_lang', 'out_lang', 'tts')


class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'status')
    list_filter = ('user_id', 'status')


class LangsListAdmin(admin.ModelAdmin):
    list_display = ('lang_in', 'lang_out', 'code', 'status')
    list_filter = ('lang_in', 'lang_out', 'code', 'status')


admin.site.register(Accounts, AccountsAdmin)
admin.site.register(UserLangs, UserLangsAdmin)
admin.site.register(UserStatus, UserStatusAdmin)
admin.site.register(LangsList, LangsListAdmin)
