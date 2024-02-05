from django.db import models, migrations

from config.constants import TYPES_CHOICES, STATUS_CHOICES


class Accounts(models.Model):
    user_id = models.BigIntegerField(null=False, primary_key=True, blank=True)
    username = models.CharField(max_length=32, null=True)
    lang_code = models.CharField(max_length=5, null=True)


class LangsList(models.Model):
    lang_in = models.CharField(max_length=15, null=False, unique=True)
    lang_out = models.CharField(max_length=15, null=False, unique=True)
    code = models.CharField(max_length=10, null=False, unique=True)
    status = models.BooleanField(null=True, default=True)


class UserLangs(models.Model):
    user_id = models.OneToOneField(Accounts, on_delete=models.CASCADE, primary_key=True, related_name='eeforeign_key')
    in_lang = models.ForeignKey(LangsList, null=False, on_delete=models.CASCADE, to_field='lang_in',
                                related_name='birinci_foreign_key')
    out_lang = models.ForeignKey(LangsList, null=False, on_delete=models.CASCADE, to_field='lang_out',
                                 related_name='ikkinchi_foreign_key')
    tts = models.BooleanField(default=True, null=False)


class UserStatus(models.Model):
    user_id = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, null=False, max_length=20)


# class Channels(models.Model):
#     chat_id = models.BigIntegerField(null=False, unique=True, primary_key=True, max_length=19, blank=True)
#     title = models.CharField(max_length=128, null=True)
#     username = models.CharField(max_length=32, null=True)
#     types = models.CharField(choices=TYPES_CHOICES, null=False, blank=True)
#
#
# class Groups(models.Model):
#     chat_id = models.BigIntegerField(null=False, unique=True, primary_key=True, max_length=20, blank=True)
#     title = models.CharField(max_length=128, null=True)
#     username = models.CharField(max_length=32, null=True)
#     types = models.CharField(choices=TYPES_CHOICES, null=False, blank=True)
#
#
# class GroupsLang(models.Model):
#     chat_id = models.ForeignKey(Groups, primary_key=True, on_delete=models.CASCADE)
#     in_lang = models.CharField(max_length=5, null=False, default='uz')
#     out_lang = models.CharField(max_length=5, null=False, default='en')


# def create_functions_and_triggers():
#     return """
# CREATE OR REPLACE FUNCTION public.user_lang()
#     RETURNS trigger
#     LANGUAGE 'plpgsql'
#     COST 100
#     VOLATILE NOT LEAKPROOF
# AS $BODY$
# begin
# 	insert into user_langs( user_id, in_lang, out_lang )
# 	values( new.user_id, 'uz', 'en' );
# 	return null;
# end
# $BODY$;
# ALTER FUNCTION public.user_lang()
#     OWNER TO postgres;
#
# CREATE OR REPLACE FUNCTION public.user_status()
#     RETURNS trigger
#     LANGUAGE 'plpgsql'
#     COST 100
#     VOLATILE NOT LEAKPROOF
# AS $BODY$
# begin
#     insert into users_status( user_id, date, active_date )
#     values( new.user_id, date( current_date at time zone 'Asia/Tashkent' ), date( current_date at time zone 'Asia/Tashkent' ) );
#     return null;
# end
# $BODY$;
# ALTER FUNCTION public.user_status()
#     OWNER TO postgres;
#
# CREATE OR REPLACE FUNCTION public.user_tts()
#     RETURNS trigger
#     LANGUAGE 'plpgsql'
#     COST 100
#     VOLATILE NOT LEAKPROOF
# AS $BODY$
# begin
#     insert into users_tts( user_id, tts )
#     values( new.user_id, 'false' );
#     return Null;
# end
# $BODY$;
# ALTER FUNCTION public.user_tts()
#     OWNER TO postgres;
#
# CREATE OR REPLACE FUNCTION public.group_lang()
#     RETURNS trigger
#     LANGUAGE 'plpgsql'
#     COST 100
#     VOLATILE NOT LEAKPROOF
# AS $BODY$
# begin
#     insert into group_langs( chat_id, in_lang, out_lang )
#     values( new.chat_id, 'uz', 'en' );
#     return null;
# end
# $BODY$;
# ALTER FUNCTION public.group_lang()
#     OWNER TO postgres;
#
# CREATE OR REPLACE TRIGGER group_lang
# AFTER INSERT
# ON public.groups
# FOR EACH ROW
# EXECUTE FUNCTION public.group_lang();
#
# CREATE OR REPLACE TRIGGER user_lang
# AFTER INSERT
# ON public.accounts
# FOR EACH ROW
# EXECUTE FUNCTION public.user_lang();
#
# CREATE OR REPLACE TRIGGER user_status
# AFTER INSERT
# ON public.accounts
# FOR EACH ROW
# EXECUTE FUNCTION public.user_status();
#
# CREATE TABLE IF NOT EXISTS public.langs_list(
# lang_in character varying(15) NOT NULL,
# lang_out character varying(15) NOT NULL,
# code character varying(10) NOT NULL,
# status boolean NOT NULL DEFAULT true,
# CONSTRAINT langs_list_pkey PRIMARY KEY (lang_in, lang_out, code));
# """
#
#
# class Migration(migrations.Migration):
#     operations = [
#         migrations.RunSQL(
#             sql=create_functions_and_triggers,
#             reverse_sql=migrations.RunSQL.noop
#         ),
#     ]
