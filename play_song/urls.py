from django.urls import path
from . import views
from play_song.views import add_to_playlist, song_detail, song_detail_only, add_to_playlist_new

app_name = 'play_song'

urlpatterns = [
   # path('add_lagu/', add_lagu, name='add_lagu'),   
    path('song_detail/<uuid:playlist_id>/<uuid:song_id>/', song_detail, name='song_detail'),
    path('song_detail/<uuid:song_id>/', song_detail_only, name='song_detail_only'),
    path('add_to_playlist/<uuid:playlist_id>/<uuid:song_id>/', add_to_playlist, name='add_to_playlist'),
    path('add_to_playlist/<uuid:song_id>/', add_to_playlist_new, name='add_to_playlist_new'),
    
]