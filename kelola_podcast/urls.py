from django.urls import path
from kelola_podcast.views import create_podcast, list_podcast, create_episode, daftar_episode

app_name = 'kelola_podcast'

urlpatterns = [
    path('create-podcast/', create_podcast, name='create_podcast'),
    path('list-podcast/', list_podcast, name='list_podcast'),
    path('create-episode/', create_episode, name='create_episode'),
    # path('daftar-episode/', daftar_episode, name='daftar_episode'),
    path('daftar-episode/<uuid:podcast_id>/', daftar_episode, name='daftar_episode'),
]
