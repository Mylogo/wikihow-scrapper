"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
import nltk

from scrap.scrap_manager import scrap_manager
from scrappers.howto.howto_scrapper import HowtoScrapper
from tagging.tagging import tag_tokens
from tokenization.tokenize import tokenize_text
from . import views

def hello(request):
    return HttpResponse(r'asd')


scrap_manager.register_includes_scrapper('wikihow', HowtoScrapper())


urlpatterns = [
    path('', hello),
    path('admin/', admin.site.urls),
    path('tokenize/', views.tokenize),
    path('tag/', views.tag),
    path('parse/', views.parse),
    path('wikihow/', views.parse_wiki_how),
]
