from django.urls import path
from album_song_royalti.views import *

app_name = 'album_song_royalti'

urlpatterns = [
    path('royalti/', cek_royalti, name='cek_royalti'),
    path('create-album/', create_album, name='create_album'),
    path('create-song/', create_song, name='create_song'),
    path('list-album-label/', list_album_label, name='list_album_label'),
    path('list-album/', list_album, name='list_album'),
    path('list-song/', list_song, name='list_song'),
    path('delete-song/', delete_song, name='delete_song'),
    path('delete-album-label/', delete_album_label, name='delete_album_label'),
    path('delete-album-user/', delete_album_user, name='delete_album_user'),
    path('song_detail/', song_detail, name='song_detail'),
]
