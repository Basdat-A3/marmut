from django.urls import path
from . import views
from kelola_playlist.views import playlist, playlist_detail, tambah_lagu,tambah_playlist, delete_playlist, edit_playlist

app_name = 'kelola_playlist'

urlpatterns = [
    path('playlist/', playlist, name='playlist'),
    path('playlist_detail/<uuid:idPlaylist>/', playlist_detail, name='playlist_detail'),
    path('tambah_lagu/', tambah_lagu, name='tambah_lagu'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('delete_playlist/<uuid:idPlaylist>/', delete_playlist, name='delete_playlist'),
    path('edit_playlist/<uuid:idPlaylist>/', edit_playlist, name='edit_playlist'),
]

