from django.urls import path

from marmut.kelola_playlist.views import *
app_name = 'kelola_playlist'


urlpatterns = [
    path('playlist/', playlist, name='playlist'),
]