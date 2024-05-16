from django.urls import path
from . import views
from kelola_playlist.views import playlist, playlist_detail, tambah_lagu,tambah_playlist

app_name = 'kelola_playlist'

urlpatterns = [
    path('playlist/', playlist, name='playlist'),
    path('playlist-detail/', playlist_detail, name='detail_playlist'),
    path('tambah-lagu/', tambah_lagu, name='tambah_lagu'),
    path('tambah-playlist/', tambah_playlist, name='tambah_playlist'),
]

