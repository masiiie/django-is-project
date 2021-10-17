from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index),
    url(r'([0-9]+)/([0-9]+)/([0-9]+)',index2),
    url(r'^markers/?',markers),
    url(r'^spacselect/?',spacial_selec),
    url(r'^json',json_view),
    url(r'^mijson/([0-9]+)',json_view_id),
]