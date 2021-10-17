from django.contrib import admin
from django.conf.urls import url,include
from .views import *
# from django.urls import path

urlpatterns = [
url('^$', index),
]
