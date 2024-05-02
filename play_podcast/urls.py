from django.urls import path
from play_podcast.views import play_podcast

app_name = 'kelola_podcast'

urlpatterns = [
    path('play-podcast/', play_podcast, name='play_podcast'),
]