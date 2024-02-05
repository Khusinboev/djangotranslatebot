"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import asyncio
import logging
import sys

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views import View

from bot.management.commands.bot import set_polling
import tracemalloc
tracemalloc.start()


class NothingView(View):
    def get(self, request):
        return HttpResponse('ok', status=200)


def set_poling(request):
    try:
        set_polling()
    except Exception as e:
        print(e)
    return HttpResponse('ok', status=200)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('set-polling', set_poling),
    path('', NothingView.as_view()),
]
